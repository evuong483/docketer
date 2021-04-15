# !/usr/bin/env python
#-----------------------------------------------------------------------------
# server.py
# Author: Erin Vuong
# Server for running app locally
#-----------------------------------------------------------------------------

from sys import argv, exit, stderr
from app import app
import logging

def main(argv):
  if len(argv) != 2:
    print('Usage: ' + argv[0] + 'port', file=stderr)
    exit(1)
  try:
    port = int(argv[1])
  except:
    print('Port must be an integer.', file=stderr)
    exit(1)

  # suppress flask server output
  logger = logging.getLogger('werkzeug')
  handler = logging.FileHandler('server.log')
  logger.addHandler(handler)
  app.logger.addHandler(handler)

  app.run(host='0.0.0.0', port=port, debug=True)

if __name__ == '__main__':
  main(argv)
