#!/usr/bin/python

from flask import Flask
import logging
import json
import datetime

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
  app.logger.info("Who said: Two vast and trunkless legs of stone")
  app.logger.info("Stand in the desert... near them, on the sand,")
  app.logger.info("Half sunk, a shattered visage lies, whose frown,")
  app.logger.info("And wrinkled lip, and sneer of cold command,")
  app.logger.info("Tell that its sculptor well those passions read")
  app.logger.info("Which yet survive, stamped on these lifeless things,")
  app.logger.info("The hand that mocked them and the heart that fed;")

  app.logger.info("And on the pedestal these words appear:")
  app.logger.error("'My name is Ozymandias, king of kings;")
  app.logger.error("Look on my works, ye Mighty, and despair!'")
  app.logger.info("Nothing beside remains. Round the decay")
  app.logger.info("Of that colossal wreck, boundless and bare")
  app.logger.info("The lone and level sands stretch far away.")

  app.logger.info( { "author": {
                                 "firstName": "PERCY",
                                 "lastName": "SHELLEY"
                               }, 
                     "title": "Ozymandias"
                   } )
  return 'ok'

@app.route('/_ah/health')
def health():
  return 'ok'

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=False)
