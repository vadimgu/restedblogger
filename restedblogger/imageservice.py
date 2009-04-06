import gdata
from gdata import photos
from gdata.photos import service
import atom

class Picasa(object):
  
  content_type = {
    'jpg':'image/jpeg',
    'png':'image/png',
    'gif':'image/gif'
    }
  def __init__(self,email=None,password=None):
    gd_client = gdata.photos.service.PhotosService()
    gd_client.email = email
    gd_client.source = 'restedblogger'
    if password: 
      gd_client.password = password
      gd_client.ProgrammaticLogin()

    self.client = gd_client
  
  def get_albums(self):
    albums = self.client.GetUserFeed()
    return albums.entry
  albums = property(get_albums)

  def add_album(self,name):
    pass
  

  #---------------------------------------------------------------------
  def upload(self,filename,album_title,description=''):
    # 1 Find the album or create new one
    for album in self.albums:
      if album.title.text == album_title:
        album_id = album.gphoto_id.text
        break
    else:
      album = self.client.InsertAlbum(title=album_title,summary=album_title)
      album_id = album.gphoto_id.text
    

    username = 'default'
    ext = filename.split('.')[-1]

    # Try to locate the image by title
    photos_url = '/data/feed/api/user/%s/albumid/%s?kind=photo' % (username, album_id)
    photos = self.client.GetFeed(photos_url)
    for photo in photos.entry:
      if photo.title.text == filename:
        image = photo
        # Update the blob if local image is newer
        #if image.updated > 
        self.client.UpdatePhotoBlob(photo,filename)
        print "U %s" % filename
        break;
    else:
      # Upload the image
      album_url = '/data/feed/api/user/%s/albumid/%s' % (username, album_id)
      photos = self.client.GetFeed(photos_url)
      title = filename
      image = self.client.InsertPhotoSimple(album_url,title,description,filename,
                                                self.content_type[ext])
      print "A %s" % filename

    content = image.content
    links = [(int(image.width.text), int(image.height.text), content.src)]
    for thumb in image.media.thumbnail:
      links.append((int(thumb.width),int(thumb.height),thumb.url))

    return links

  def get_images(self,albumid):
    username = 'default'
    photos_url = '/data/feed/api/user/%s/albumid/%s?kind=photo' % (username, albumid)
    photos = self.client.GetFeed(photos_url)
    return photos.entry
  
  



  

    
        
