#!/usr/bin/python
import os
import sys
import getpass
import ConfigParser
import optparse
import string
import webbrowser 
import logging

from restedblogger import rested
from restedblogger.blogger import Blogger

from restedblogger import plugin
plugin.load_plugins()


def getPassword(email):
  """Prompt user for password"""
  password = getpass.getpass("[%s] Password: " % email)
  return password



defaultTemplate = """
<html>
  <head>
    <title>$title</title>
  </head>
  <body>
  <h1>$title</h1>
  $body
  </body>
</html>
"""


def walk_up(path):
  """ Walk up the path and yield each location """
  while True:
    yield path
    up,_ = os.path.split(path)
    if path == up:
      raise StopIteration
    path = up

def locate_base(name='reb.conf',path=os.getcwd()):
  """Walk up the directory tree and look for config
  locate_base() -> base_path or None
  """
  for location in walk_up(path):
    config = os.path.join(path,name)
    if os.path.isfile(config):
      return location
    

def init(configFile):
  email = raw_input("Email Address: ")
  password = getPassword(email) 
  blogger = Blogger(email,password)
  blogs = blogger.blogs
  if len(blogs) == 1:
    blog_id = blogs[0][0]
  else:
    print "---------------------------------"
    for i,(blog_id,title) in enumerate(blogs):
      print "%-3s %s" % (i+1,title)
    print "---------------------------------"
    i = int(raw_input("Choose a Blog: "))-1
    blog_id = blogs[i][0]
  
  config = ConfigParser.ConfigParser()
  config.add_section('blogger')
  config.set('blogger','email',email)
  config.set('blogger','blogid',blog_id)
  configfd = open(configFile,'w+')
  config.write(configfd)
  configfd.close()
  print "Configuration saved to %s" % os.path.abspath(configFile)
  
  return config


def list(email,password,blog_id):
  blogger = Blogger(email,password,blog_id)
  for id,title,updated,content,entry in blogger.query(10):
    print id,updated[0:10],title


def fetch_template(email,password,blog_id,destination):
  blogger = Blogger(email,password,blog_id)
  template = blogger.fetchTemplate()
  ftemplate = open(destination,'w+')
  ftemplate.write(template)
  ftemplate.close()
  logging.info("Saved template as %s" % destination)

def view(parts,template,rstFileName):
  template = string.Template(template)
  htmlFileName = rstFileName + ".html"
  htmlFile = open(htmlFileName,'w+')
  htmlFile.write(template.safe_substitute(
    title=parts['title'],
    body=parts['html_body_no_title']))
  htmlFile.close()
  webbrowser.open("file://" + os.path.abspath(htmlFileName))



def publish(parts,email,password,blog_id,draft=False):
  publish = not draft
  blogger = Blogger(email,password,blog_id)
  # Try to update an existing post based on title.
  for id,title,updated,content,entry in blogger.query():
    if title == parts['title']:
      logging.info("U %s" % parts['title'])
      blogger.updatePost(entry,parts,publish)
      break
  # Or create new post
  else:
    logging.info("A %s" % parts['title'])
    blogger.createPost(parts,publish)


def draft(parts,email,password,blog_id):
  return publish(parts,email,password,blog_id,draft=True)




def main():
  # Parsing command line options
  # ----------------------------
  usage = """usage:
  
reb init
  
  Enable restedblogger in the current folder

reb list

  List the last ten blogs

reb template

  Fetch the last blog post and save it as a template.

reb view FILE

  Preview the FILE with a template. If no template was found use a dummy template.

reb draft FILE

  Publish the FILE to Blogger in a draft mode

reb publish FILE
  
  Publish the FILE to Blogger

  """

  parser = optparse.OptionParser(usage=usage)
   
  parser.add_option("-v","--verbose",dest="verbose",action="store_true",default=False,
                     help="Config File", metavar='CONFIG')

  (options,args) = parser.parse_args()
  

  level = logging.INFO
  if options.verbose:
    level = logging.DEBUG
  logging.basicConfig(format="%(message)s",level=level)


  command = args[0]

  configFile = 'reb.conf'
  
  # reb init
  if command == 'init':
    init(configFile)
    return
  
  
  base = locate_base(configFile)
  parts = None
  rstFileName = None
  if command in ('view','publish','draft'):
    rstFileName =  args[1]
    rstText = open(rstFileName,'r').read()
    parts = rested.publish_blog_parts(rstText)
    

  if not base:
    logging.error("RestedBlogger configuration wasn't found. Please run 'reb init' command")
    return

  logging.debug('Base at %s' % base)

  # reb view FILE
  if command == 'view':
    templateFile = os.path.join(base,'template.html')  
    if os.path.isfile(templateFile):
      tplFile = open('template.html','r')
      template = tplFile.read()
      tplFile.close()
    else:
      logging.debug('Using default template' % base)
      template = defaultTemplate

    view(parts,template,args[1])
    return

  config_path = os.path.join(base,configFile)
  config = ConfigParser.ConfigParser()
  config.read(config_path)
  email = config.get('blogger','email')
  blog_id = config.get('blogger','blogid')
  if config.has_option('blogger','password'):
    password = config.get('blogger','password') or getPassword(email)
  else:
    password = getPassword(email)
   
  # reb template
  if command == 'template':
    destination = os.path.join(base,'template.html')
    fetch_template(email,password,blog_id,destination)
    return

  # reb list
  if command == 'list':
    list(email,password,blog_id)
    return 

  # reb publish FILE
  if command == 'publish':
    publish(parts,email,password,blog_id)
    
  # reb draf FILE
  if command == 'draft':
    draft(parts,email,password,blog_id)
  
if __name__ == '__main__':
  main()




