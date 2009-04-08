"""
Lilypond directive
------------------

This directive can be used to produce musical notations::

  .. lilypond:: somechords.png

    \context ChordNames {
       \chordmode {
         f1 g
       }
    }
    \context FretBoards {
      < f, c f a c' f'>1
      < g,\6 b, d g b g'>
    }
    \context Staff {
      \clef "treble_8"
      < f, c f a c' f'>1
      < g, b, d g b' g'>
    }

"""

from docutils import nodes
from docutils.parsers.rst import directives
from subprocess import Popen,PIPE
import os

# PIL dependent

import Image, ImageChops, ImageColor
import sys


def crop(image_file, bgcolor=ImageColor.getrgb("white")):
  image = Image.open(image_file,'r')
  mask = Image.new("RGB", image.size, bgcolor)
  diff = ImageChops.difference(image, mask)
  bbox = diff.getbbox()
  new_image = image.crop(bbox)
  new_image.save(image_file,"png")


if __name__ == '__main__':
  input = sys.argv[1]
  crop = autocrop(Image.open(input),ImageColor.getrgb("white"))
  crop.save('out.png',"PNG")



def lilypond_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):

  
  output = '.'.join(arguments[0].split(".")[0:-1])
  lilypond_src = content
  # there must be a better way to hand the MacOS situation
  if os.path.isfile("/Applications/LilyPond.app/Contents/Resources/bin/lilypond"):
    lilypond_exec = "/Applications/LilyPond.app/Contents/Resources/bin/lilypond"
  else:
    lilypond_exec = "lilypond"
  plot = Popen(lilypond_exec + ' --png --output=%s - ' % output, shell=True, bufsize=64, stdin=PIPE)
  plot.stdin.write("\n".join(lilypond_src))
  plot.stdin.flush()
  plot.stdin.close()

  plot.wait()

  crop(arguments[0])

    
  return [nodes.image(uri=arguments[0])]


lilypond_directive.arguments = (1, 0, 1)
lilypond_directive.content = 1


directives.register_directive('lilypond', lilypond_directive)
