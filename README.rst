
.. contents:: Table of Contents
  :depth: 2

What It Does
------------

Transfroms a file from `reStructuredText <http://docutils.sourceforge.net/rst.html>`_ 
format to HTML and post it to `blogger <http://www.blogger.com>`_ (aka blogspot).


Installation
------------

To install from sources, it's the usual ::

  $ python setup.py install


Features
--------

  * Create or Update a post
  * Publish a post.
  * Preview a post.
  * Upload images in a post to `Picasa Web <http://picasaweb.google.com>`_


Using RestedBlogger
-------------------

First write a post in reStructuredText_ format by editing postA.rst. ::

  My Rested Post
  ==============

  Text is power. I'm using this image to proove it:

  .. image:: proof.jpg


You can preview the post using the `-v` flag ::

  $ restedblogger -v postA.rst

This will open the default browser with the generated html. It will NOT post to
blogger_. 


RestedBlogger can fetch your last post and make it into a template for preview
using the `-t` flag :: 

  $ restedblogger -t

As soon as a communication to blogger_ is required you will be prompted to enter
your email and password. The email will be stored in the configuration file
`./restedblogger.conf`. The password IS NOT stored and will be prompted on each
interaction with the blogger_ site.

Once you're satisfied with the results you can send the post ::

  $ restedblogger postA.rst

This will create a new post in draft mode or update an existing one. Can be
executed many times.


To publish the post::

  $ restedblogger -P postA.rst

This will create or update the post and set off the draft mode. Setting the
draft mode back to on is not implemented.
  





Extensions to reStructuredText
------------------------------

All the features of reStructuredText_ an more...


Source Code Highlighting
~~~~~~~~~~~~~~~~~~~~~~~~

Highlight source code using `Pygments <http://pygments.org>`_ ::

  .. sourcecode:: python
  
    def count(start):
      yield start
      while 1:
        start += 1
        yield start

.. raw:: html

  <pre><span style="color: rgb(0, 128, 0); font-weight: bold;">def</span> <span style="color: rgb(0, 0, 255);">count</span>(start):
    <span style="color: rgb(0, 128, 0); font-weight: bold;">yield</span> start
    <span style="color: rgb(0, 128, 0); font-weight: bold;">while</span> <span style="color: rgb(102, 102, 102);">1</span>:
      start <span style="color: rgb(102, 102, 102);">+=</span> <span style="color: rgb(102, 102, 102);">1</span>
      <span style="color: rgb(0, 128, 0); font-weight: bold;">yield</span> start
  </pre>

The css styles are inlined.

Wikipedia Reference
~~~~~~~~~~~~~~~~~~~

You can reference Wikipedia articles like this: ::

  I played a game of :wkp:`chess` yesterday.

This will put the link to the chess article. 

.. raw:: html
  
  <p>
  I played a game of <a class="reference external" href="http://en.wikipedia.org/wiki/chess">chess</a> yesterday.
  </p>
  
Plotting
~~~~~~~~

To include plots in a post you must install `gnuplot
<http://www.gnuplot.info/>`_ and make it available on your PATH. ::

  .. gnuplot:: sincos.png

    set yrange [-2:2]    
    plot sin(x), cos(x)

This will write the plot to `sincos.png` file and include it in the post.



