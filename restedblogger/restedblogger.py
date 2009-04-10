#!/usr/bin/python
import os
import sys
import getpass
import ConfigParser
import optparse
import string
import webbrowser 

import rested
from blogger import Blogger

import plugin
plugin.load_plugins()

def getPassword(email):
  """Prompt user for password"""
  password = getpass.getpass("[%s] Password: " % email)
  return password


# When no configuration is found prompt the user for information about the blog
# and save it in a config file
def createConfigDialog(configFileName='restedblogger.conf'):
  """ Prompt the user for configuration """
  email = raw_input("Email Address: ")
  password = getPassword(email) 
  blogger = Blogger(email,password)
  blogs = list(blogger.blogs)
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
  configFile = open(configFileName,'w+')
  config.write(configFile)
  configFile.close()
  print "Wrote config to %s" % os.path.abspath(configFileName)
  
  # password is not written to the file
  config.set('blogger','password',password)
  
  return config



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


def main():
  # Parsing command line options
  # ----------------------------
  usage = "usage: %prog [options] [restFile]"
  
  parser = optparse.OptionParser(usage=usage)
  
  parser.add_option("-s","--setup",dest="setup",action="store_true",default=False,
                     help="Setup restedblogger config")

  parser.add_option("-c","--config",dest="config",default="restedblogger.conf",
                     help="Config File", metavar='CONFIG')

  parser.add_option("-v","--preview",dest="preview",action="store_true",default=False,
                    help="Preview the content in a browser and will not post the content to blogger.")

  parser.add_option("-P","--publish",dest="publish",action="store_true",default=False,
                    help="Publish an existing draft or a new post")

  parser.add_option("-t","--fetch-template",dest="fetchtemplate",action="store_true",default=False,
                    help="Tries to fetch a template and save it under template.html")

  (options,args) = parser.parse_args()
  

  # Handle Setup
  # ------------
  if options.setup:
    config = createConfigDialog(options.config)
    return

  email = None
  password = None
  blog_id = None

  # Reading the config
  # ------------------
  if not options.preview:
    config = ConfigParser.ConfigParser()
    readFiles = config.read(options.config)
    if not readFiles: 
      config = createConfigDialog(options.config)
  
    email = config.get('blogger','email')
    if config.has_option('blogger','password'):
      password = config.get('blogger','password') or getPassword(email)
    else:
      password = getPassword(email)
    blog_id = config.get('blogger','blogid')

  
  # Upload the post
  # ---------------
  if len(args) >= 1:
    rstFileName =  args[0]
    rstText = open(rstFileName,'r').read()
    rst_title,body = rested.rest2html(rstText)
    
    if options.preview:
      if os.path.isfile('template.html'):
        tplFile = open('template.html','r')
        template = string.Template(tplFile.read())
        tplFile.close()
      else:
        template = string.Template(defaultTemplate)
      htmlFileName = rstFileName + ".html"
      htmlFile = open(htmlFileName,'w+')
      htmlFile.write(template.safe_substitute(title=rst_title,body=body))
      htmlFile.close()
      webbrowser.open("file://" + os.path.abspath(htmlFileName))
    
    else:  
      password = getPassword(config,email) 
      blogger = Blogger(email,password,blog_id)
      # Update an existing post
      for id,title,updated,content,entry in blogger.query():
        if title == rst_title:
          print "U %s" % rst_title
          blogger.updatePost(entry,body,options.publish)
          break
      # Or create new post
      else:
        print "A %s" % rst_title
        blogger.createPost(rst_title,body,options.publish)
        
     
  
  elif options.fetchtemplate:
    print "Fetching Template"
    password = getPassword(config,email) 
    blogger = Blogger(email,password,blog_id)
    template = blogger.fetchTemplate()

    ftemplate = open('template.html','w+')
    ftemplate.write(template)
    ftemplate.close()

  # Or list the last 10 posts
  # ------------------------
  else:
    password = getPassword(config,email)
    blogger = Blogger(email,password,blog_id)
    for id,title,updated,content,entry in blogger.query(10):
      print id,updated[0:10],title





if __name__ == '__main__':
  main()




