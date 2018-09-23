Flask extension for grouped log lines for Google Cloud Logging
==============================================================

Flask extension that allows log lines emitted within a request handler to display/render together.

Normally, when using Google Cloud Logging libraries ( `google-cloud-logging <https://pypi.org/project/google-cloud-logging/>`__ and `CloudLoggingHander <https://googlecloudplatform.github.io/google-cloud-python/latest/logging/handlers.html>`__), each log entry that gets emitted is displayed separately within the Logging UI. However, its desireable to group all logs together that logically belong that way in an HTTP Request. For a given HTTP Request into FLask, this extension displays all the logs 'together' below the parent request.

as in

.. image:: https://raw.githubusercontent.com/salrashid123/flask-gcp-log-groups/master/images/log_entry.png
    :target: https://raw.githubusercontent.com/salrashid123/flask-gcp-log-groups/master/images/log_entry.png

Configuration Parameters
~~~~~~~~~~~~~~~~~~~~~~~~

-  ``GCPHandler``
-  
   -  ``app``: Flask handler
-  
   -  ``parentLogName``: parentLogger name for the 'request (default: request")
-  
   -  ``childLogName``: childLogger name for the 'application logs (default: "application")
-  
   -  ``traceHeaderName``: header name to parse as the trace header. (on GCP, its ``X-Cloud-Trace-Context``)
-  
   -  ``labels``: labels dictionary to apply to all logs (default = None),
-  
   -  ``resource``: Cloud Logging resource to log against (default='global')

.. code:: python

    from flask import Flask
    import logging, json

    from flask_gcp_log_groups import GCPHandler

    app = Flask(__name__)

    g = GCPHandler(app, parentLogName="request",
        childLogName="application",
        traceHeaderName='X-Cloud-Trace-Context',
        labels= {'foo': 'bar', 'baz': 'qux'},
        resource='global')
    g.setLevel(logging.INFO)
    app.logger.addHandler(g)

    @app.route('/')
    def default():
      app.logger.setLevel(logging.INFO)
      app.logger.info("I met a traveller from an antique land,")
      return 'ok'

    if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080, debug=False)

-  with trace only

   ::

       curl -v  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.89 Safari/537.36" \
       -H "X-Cloud-Trace-Context: `python -c "import uuid; print uuid.uuid4()"`" \
       http://localhost:8080/

.. |images/log\_entry.png| image:: images/log_entry.png