#!/usr/bin/python
import os
import sys
import getpass
import ConfigParser
import optparse
import string
import webbrowser 

from gdata import service
import gdata
import atom

import urllib2
from BeautifulSoup import BeautifulSoup

import rested

class Blogger(object):
  def __init__(self,email=None,password=None,blog_id=None,account_type='GOOGLE'):
    blogger = service.GDataService(email,password)
    blogger.source = 'restedblogger'
    blogger.service = 'blogger'
    blogger.account_type = account_type
    blogger.server = 'www.blogger.com'
    blogger.ProgrammaticLogin()
    
    self.blogger = blogger
    self._blog_id = blog_id

  def get_blog_id(self):
    if self._blog_id:
      return self._blog_id
    query = service.Query()
    query.feed = '/feeds/default/blogs'
    feed = self.blogger.Get(query.ToUri())
    self._blog_id = feed.entry[0].GetSelfLink().href.split("/")[-1]
    return self._blog_id
  blog_id = property(get_blog_id)

  def query(self,maximum=10):
    query = service.Query()
    query.feed = '/feeds/%s/posts/default/' % self.blog_id
    feed = self.blogger.GetFeed(query.ToUri())
    for entry in feed.entry:
      for link in entry.link:
        if link.rel=='self':
          id = link.href.split('/')[-1]
          break
      else:
        continue
      yield id,entry.title.text,entry.updated.text,entry.content.text,entry

  def get_post(self,post_id):
    query = service.Query()
    query.feed = '/feeds/%s/posts/default/%s' % (self.blog_id,post_id)
    feed = self.blogger.GetFeed(query.ToUri())
    return feed.entry[0]

  def createPost(self, title, content, publish=False):
    entry = gdata.GDataEntry()
    entry.title = atom.Title('xhtml', title)
    entry.content = atom.Content(content_type='html', text=content)
    if not publish:
      # switching the draft mode on
      control = atom.Control()
      control.draft = atom.Draft(text='yes')
      entry.control = control
    return self.blogger.Post(entry, '/feeds/%s/posts/default' % self.blog_id)
  
  def updatePost(self,entry,content,publish=False):
    entry = self.blogger.Get(entry.GetSelfLink().href)
    entry.content = atom.Content(content_type='html', text=content)
    if publish: 
      # switching the draft mode off
      control = atom.Control()
      control.draft = atom.Draft(text='no')
      entry.control = control
    return self.blogger.Put(entry, entry.GetEditLink().href)
  
  def fetchTemplate(self):
    for id,title,updated,content,entry in self.query():
      try:
        url = entry.GetHtmlLink().href
      except:
        continue
      fd = urllib2.urlopen(url)
      lastPost = fd.read()
      fd.close()
      
      soup = BeautifulSoup(lastPost)
      soup.find('h3','post-title entry-title').a.string.\
        replaceWith("$title")
      soup.find('div','post-body entry-content').\
        replaceWith('<div class="post-body entry-conent">$body</div>')
      
      return str(soup)



def createConfigDialog(configFileName='restedblogger.conf'):
  """ Prompt the user for configuration """
  email = raw_input("Email Address:")
  config = ConfigParser.ConfigParser()
  config.add_section('blogger')
  config.set('blogger','email',email)
  configFile = open(configFileName,'w+')
  config.write(configFile)
  configFile.close()
  return config


def getPassword(config,email):
  """Prompt user for password if needed"""
  password = None
  if config.has_option('blogger','password'):
    password = config.get('blogger','password')
  else:
    password = getpass.getpass("password for %s:" % email)
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

def main():
  # Parsing command line options
  # ----------------------------
  usage = "usage: %prog [options] restFile"
  parser = optparse.OptionParser(usage=usage)
  parser.add_option("-c","--config",dest="config",default="restedblogger.conf",
                     help="Config File", metavar='CONFIG')
  parser.add_option("-v","--preview",dest="preview",action="store_true",default=False,
                    help="Preview the content in a browser and will not post the content to blogger.")
  parser.add_option("-P","--publish",dest="publish",action="store_true",default=False,
                    help="Publish an existing draft or a new post")

  parser.add_option("-t","--fetch-template",dest="fetchtemplate",action="store_true",default=False,
                    help="Tries to fetch a template and save it under template.html")

  (options,args) = parser.parse_args()
  
  # Reading the config
  # ------------------
  config = ConfigParser.ConfigParser()
  readFiles = config.read(options.config)
  
  # config is unused if in preview, so no need to bug the user
  if not readFiles and not options.preview:
    config = createConfigDialog(options.config)
  email = options.preview or config.get('blogger','email')

  
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
      blogger = Blogger(email,getPassword(config,email))
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
    blogger = Blogger(email,getPassword(config,email))
    template = blogger.fetchTemplate()

    ftemplate = open('template.html','w+')
    ftemplate.write(template)
    ftemplate.close()

  # Or list the last n posts
  # ------------------------
  else:
    blogger = Blogger(email,getPassword(config,email))
    for id,title,updated,content,entry in blogger.query():
      print id,updated[0:10],title


if __name__ == '__main__':
  main()




