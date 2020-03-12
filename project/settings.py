import os

# environment varibales:
DEBUG = os.environ.get('DEBUG', False)
HOST = os.environ.get('HOST', 'localhost')
PORT = os.environ.get('PORT', '8080')
RELOADER = os.environ.get('RELOADER', True)
