#!/usr/bin/python
from gdata import service
import gdata
import atom
import os
import urllib2
from BeautifulSoup import BeautifulSoup

from picasa import Picasa

class Blogger(object):
  source='restedblogger'
  service='blogger'
  account_type='GOOGLE'
  server = 'www.blogger.com'

  # Start header from <h4>
  initial_header_level=4

  

  def __init__(self,email=None,password=None,blog_id=None):
    blogger = service.GDataService(email,password)
    blogger.source = self.source
    blogger.service = self.service
    blogger.account_type = self.account_type
    blogger.server = self.server
    if password:
      blogger.ProgrammaticLogin()
    
    self.blogger = blogger
    
    self.email = email
    self.password = password
    self.blog_id = blog_id

  
    

  def get_blogs(self):
    query = service.Query()
    query.feed = '/feeds/default/blogs'
    feed = self.blogger.Get(query.ToUri())
    for entry in feed.entry:
      blog_id = entry.GetSelfLink().href.split("/")[-1]
      title = entry.title.text
      yield blog_id,title

  blogs = property(get_blogs)



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
  

  def upload_images(self,html):
    """Search for local images in the html, upload them and replace image src
    with the uploaded url."""
    soup = BeautifulSoup(html)
    images =  soup.findAll('img',src=os.path.isfile)
    if images:
      picasa = Picasa(self.email,self.password)
      for image in images:
        links = picasa.upload(image['src'],'Blogger')
        #width,height,url = links[0]
        # dealing with blogger limitation on image size.
        links.sort(reverse=True)
        for width,height,url in links:
          if width <= 400 and height <= 400:
            image['src'] = url
            break
              
    return str(soup)
    

  def createPost(self, title, content, publish=False):
    entry = gdata.GDataEntry()
    entry.title = atom.Title('xhtml', title)
    content = self.upload_images(content)
    entry.content = atom.Content(content_type='html', text=content)
    if not publish:
      # switching the draft mode on
      control = atom.Control()
      control.draft = atom.Draft(text='yes')
      entry.control = control
    return self.blogger.Post(entry, '/feeds/%s/posts/default' % self.blog_id)
  
  def updatePost(self,entry,content,publish=False):
    entry = self.blogger.Get(entry.GetSelfLink().href)
    content = self.upload_images(content)
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

