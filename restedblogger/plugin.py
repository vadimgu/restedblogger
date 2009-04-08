"""
Implementation of the plugin functionality

load_plugins will load all python files from ~/.restedblogger/plugins/

"""
import os
import sys

def load_plugins(path=None):
  plugins = []
  if path is None:
    path = os.path.join(os.path.expanduser('~'),'.restedblogger','plugins')
  if os.path.isdir(path):
    sys.path.append(path)
    for f in os.listdir(path):
      module_name, ext = os.path.splitext(f)
      if ext == '.py':
        module = __import__(module_name)
        plugins.append(module)
  return plugins
