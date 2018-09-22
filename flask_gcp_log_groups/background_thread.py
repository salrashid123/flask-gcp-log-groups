
from __future__ import print_function

import atexit
import logging
import sys
import threading
import time
import json
import ast

from six.moves import range
from six.moves import queue

from google.cloud.logging.handlers.transports.base import Transport

_DEFAULT_GRACE_PERIOD = 5.0  # Seconds
_DEFAULT_MAX_BATCH_SIZE = 10
_DEFAULT_MAX_LATENCY = 0  # Seconds
_WORKER_THREAD_NAME = 'google.cloud.logging.Worker'
_WORKER_TERMINATOR = object()
_LOGGER = logging.getLogger(__name__)


def _get_many(queue_, max_items=None, max_latency=0):

    start = time.time()
    # Always return at least one item.
    items = [queue_.get()]
    while max_items is None or len(items) < max_items:
        try:
            elapsed = time.time() - start
            timeout = max(0, max_latency - elapsed)
            items.append(queue_.get(timeout=timeout))
        except queue.Empty:
            break
    return items


class _Worker(object):

    def __init__(self, cloud_logger, grace_period=_DEFAULT_GRACE_PERIOD,
                 max_batch_size=_DEFAULT_MAX_BATCH_SIZE,
                 max_latency=_DEFAULT_MAX_LATENCY):
        self._cloud_logger = cloud_logger
        self._grace_period = grace_period
        self._max_batch_size = max_batch_size
        self._max_latency = max_latency
        self._queue = queue.Queue(0)
        self._operational_lock = threading.Lock()
        self._thread = None

    @property
    def is_alive(self):
        return self._thread is not None and self._thread.is_alive()

    def _safely_commit_batch(self, batch):
        total_logs = len(batch.entries)

        try:
            if total_logs > 0:
                batch.commit()
                _LOGGER.debug('Submitted %d logs', total_logs)
        except Exception:
            _LOGGER.error(
                'Failed to submit %d logs.', total_logs, exc_info=True)

    def _thread_main(self):

        _LOGGER.debug('Background thread started.')

        quit_ = False
        while True:
            batch = self._cloud_logger.batch()
            items = _get_many(
                self._queue, max_items=self._max_batch_size,
                max_latency=self._max_latency)

            for item in items:
                if item is _WORKER_TERMINATOR:
                    quit_ = True
                    # Continue processing items, don't break, try to process
                    # all items we got back before quitting.
                else:
                    if (item['message'] is  None):
                      batch.log_text(None,  timestamp=item['timestamp'], labels=item['labels'], severity=item['severity'], trace=item['trace'], span_id=item['span_id'], http_request=item['http_request']) 
                    else:
                      try:
                          msg=ast.literal_eval(item['message'])
                          batch.log_struct(msg,  timestamp=item['timestamp'], labels=item['labels'], severity=item['severity'], trace=item['trace'], span_id=item['span_id'], http_request=item['http_request'])
                      except Exception as e:
                        #print("Error " + str(e))
                        batch.log_text(item['message'],  timestamp=item['timestamp'], labels=item['labels'], severity=item['severity'], trace=item['trace'], span_id=item['span_id'], http_request=item['http_request']) 

            self._safely_commit_batch(batch)

            for _ in range(len(items)):
                self._queue.task_done()

            if quit_:
                break

        _LOGGER.debug('Background thread exited gracefully.')

    def start(self):
        with self._operational_lock:
            if self.is_alive:
                return

            self._thread = threading.Thread(
                target=self._thread_main,
                name=_WORKER_THREAD_NAME)
            self._thread.daemon = True
            self._thread.start()
            atexit.register(self._main_thread_terminated)

    def stop(self, grace_period=None):
        if not self.is_alive:
            return True

        with self._operational_lock:
            self._queue.put_nowait(_WORKER_TERMINATOR)

            if grace_period is not None:
                print(
                    'Waiting up to %d seconds.' % (grace_period,),
                    file=sys.stderr)

            self._thread.join(timeout=grace_period)
            success = not self.is_alive

            self._thread = None

            return success

    def _main_thread_terminated(self):
        if not self.is_alive:
            return

        if not self._queue.empty():
            print(
                'Program shutting down, attempting to send %d queued log '
                'entries to Stackdriver Logging...' % (self._queue.qsize(),),
                file=sys.stderr)

        if self.stop(self._grace_period):
            print('Sent all pending logs.', file=sys.stderr)
        else:
            print(
                'Failed to send %d pending logs.' % (self._queue.qsize(),),
                file=sys.stderr)

    def enqueue(self, message,timestamp,severity, resource=None, labels=None,
                trace=None, span_id=None,http_request=None):

        self._queue.put_nowait({
            'message': message,
            'timestamp': timestamp,
            'severity': severity,
            'resource': resource,
            'labels': labels,
            'trace': trace,
            'span_id': span_id,
            'http_request': http_request
        })

    def flush(self):
        self._queue.join()


class BackgroundThreadTransport(Transport):

    def __init__(self, client, name, grace_period=_DEFAULT_GRACE_PERIOD,
                 batch_size=_DEFAULT_MAX_BATCH_SIZE,
                 max_latency=_DEFAULT_MAX_LATENCY):
        self.client = client
        logger = self.client.logger(name)
        self.worker = _Worker(logger,
                              grace_period=grace_period,
                              max_batch_size=batch_size,
                              max_latency=max_latency)
        self.worker.start()

    def send(self, message, timestamp, severity="INFO", resource=None, labels=None,
             trace=None, span_id=None,http_request=None):

        self.worker.enqueue(message, timestamp=timestamp,severity=severity,resource=resource, labels=labels,
                            trace=trace, span_id=span_id,http_request=http_request)

    def flush(self):
        self.worker.flush()