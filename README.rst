RestedBlogger
=============

.. contents:: Table of Contents
  :depth: 2

What is RestedBlogger
---------------------

RestedBlogger is a command line application that can transform a
`reStructuredText <http://docutils.sourceforge.net/rst.html>`_ 
file into HTML and post it to `Blogger <http://www.blogger.com>`_ (aka Blogspot).


Installation
------------

To install from sources ::

  $ git clone git://github.com/vadimgu/restedblogger
  $ cd restedblogger
  $ python setup.py install


Features
--------

  * Create or Update a post
  * Publish a post.
  * Preview a post.
  * Automatically upload images in a post to `Picasa Web <http://picasaweb.google.com>`_
  * Set the labels.


Using RestedBlogger
-------------------

First you have to make a folder where you will be editing your posts. ::

  $ mkdir myblog
  $ cd myblog
  $ reb init

The `init` command will ask you your email, your password and will also ask you
to choose a blog, if you have more then one. Then, that information is saved in
`reb.conf` file. The password IS NOT stored and will be prompted on each
interaction with the Blogger_ site.


The next step, is to write a blog post by editing a text file `myPost.rst` ::

  My Rested Post
  ==============

  Text is power. I'm using this image to prove it:

  .. image:: proof.jpg


You can preview the post with the `reb view` command ::

  $ reb view myPost.rst

This will open the default browser with the generated html. It will NOT post to
Blogger_. 


RestedBlogger can fetch your last post and make it into a template for preview :: 

  $ reb template

Once you're satisfied with the results you can send the post ::

  $ reb draft myPost.rst

This will create a new post in draft mode or update an existing one. Can be
executed many times.

.. attention::
  The posts are identified by their titles. If the title of a post is changed
  it will be considered as a new post.


To publish the post::

  $ reb publish myPost.rst

This will create or update the post and set off the draft mode. Setting the
draft mode back to on is not implemented.
  





Extensions to reStructuredText
------------------------------

All the features of reStructuredText_ an more...


Source Code Highlighting
~~~~~~~~~~~~~~~~~~~~~~~~

Highlight source code using `Pygments <http://pygments.org>`_ ::

  .. sourcecode:: python
  
    def count(start=0):
      yield start
      while 1:
        start += 1
        yield start

The css styles are inlined.

Wikipedia Reference
~~~~~~~~~~~~~~~~~~~

You can reference Wikipedia articles like this: ::

  I played a game of :wkp:`chess` yesterday.


  
Plotting
~~~~~~~~

To include plots in a post you must install `gnuplot
<http://www.gnuplot.info/>`_ and make it available on your PATH. ::

  .. gnuplot:: sincos.png

    set yrange [-2:2]    
    plot sin(x), cos(x)

This will write the plot to `sincos.png` file and include it in the post.

Post Labels
~~~~~~~~~~~

To set the post labels use the `meta` directive::

  .. meta::
    :keywords: Text, Power

.. note::
  The `meta` directive is a standard reStructuredText_ directive. 


Plugins
-------

You can write your own plugins. Plugins are python modules extending the
reStructuredText_ functionality. To enable a plugin put it into
`~/.restedblogger/plugins/`. There is an example in the sources
`plugins/lilypond-directive.py`. It allows to write music using `Lilypond
<http://lilypond.org>`_. ::

  $ mkdir -p ~/.restedblogger/plugins
  $ cp restedblogger/plugins/lilypond_directive.py ~/.restedblogger/plugins

This will enable the `lilypond` directive. The dependencies for plugins are not
managed and any additional package used by a plugin must be installed manually.



