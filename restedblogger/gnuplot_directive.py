"""
Gnuplot directive
-----------------

This directive can be used to produce plots using gnuplot::

  .. gnuplot:: sincos.png

    plot sin(x), cos(x)


"""

from docutils import nodes
from docutils.parsers.rst import directives
from subprocess import Popen,PIPE


def gnuplot_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):

  width,height=400,400
  output = arguments[0]
  gnuplot_commands = content
  plot = Popen('gnuplot -persist', shell=True, bufsize=64, stdin=PIPE)
  plot.stdin.write("set term png size %d,%d\n" % (width,height))
  plot.stdin.write("set output '%s'\n" % (output,))
  plot.stdin.write("\n".join(gnuplot_commands))
  plot.stdin.write("\nquit\n")
  plot.stdin.flush()
    
  return [nodes.image(uri=output)]


gnuplot_directive.arguments = (1, 0, 1)
gnuplot_directive.content = 1
gnuplot_directive.options = {'size':'medium',} 


directives.register_directive('gnuplot', gnuplot_directive)
