import sys

from docutils import core

# Custom Directives and Roles
# ---------------------------
import sourcecode_directive
import wikipedia_reference_role
import gnuplot_directive


def rest2html(source,initial_header_level=4):
  overrides = {'input_encoding': 'utf8',
               'doctitle_xform': 1,
               'initial_header_level': initial_header_level}
  parts = core.publish_parts(source,
    writer_name='html', 
    settings_overrides=overrides)

  body_html = parts['html_body']
  title_html = parts['html_title']
  body = body_html.replace(title_html,'')
  title = parts['title']
  return title,body

if __name__ == '__main__':
  rstFileName =  sys.argv[1]
  title,body = rest2html(open(rstFileName,'r').read())
  print title
  print body




