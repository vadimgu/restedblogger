import sys

from docutils import core
from docutils import io
from docutils.parsers.rst.directives.html import MetaBody


# Custom Directives and Roles
# ---------------------------
from restedblogger import sourcecode_directive
from restedblogger import wikipedia_reference_role
from restedblogger import gnuplot_directive



 
def publish_blog_parts(source, source_path=None, source_class=io.StringInput,
      destination_path=None,
      reader=None, reader_name='standalone',
      parser=None, parser_name='restructuredtext',
      writer=None, writer_name='html',
      settings=None, settings_spec=None,
      settings_overrides={'input_encoding': 'utf8', 'doctitle_xform': 1,}, 
      config_section=None,
      enable_exit_status=None,
      initial_header_level=4,):
    """
    This is a copy of docutils.core.publish_parts() with additional information
    in the returned parts.
    
      - parts['tags'] : Tags are extracted from the meta directive.
      - parts['body_html_no_title'] : The body_html without the title.

    """
    settings_overrides['initial_header_level'] = initial_header_level

    output, pub = core.publish_programmatically(
        source=source, source_path=source_path, source_class=source_class,
        destination_class=io.StringOutput,
        destination=None, destination_path=destination_path,
        reader=reader, reader_name=reader_name,
        parser=parser, parser_name=parser_name,
        writer=writer, writer_name=writer_name,
        settings=settings, settings_spec=settings_spec,
        settings_overrides=settings_overrides,
        config_section=config_section,
        enable_exit_status=enable_exit_status)
    parts = pub.writer.parts

    # Tags
    parts['tags'] = None
    for meta in pub.document.traverse(MetaBody.meta):
      if meta.get('name') == 'keywords':
        parts['tags'] = meta.get('content')
        break

    # Body without Title
    body = parts['html_body']
    title = parts['html_title']
    parts['html_body_no_title'] = body.replace(title,'')
        
    return parts


if __name__ == '__main__':
  rstFileName =  sys.argv[1]
  parts = publish_blog_parts(open(rstFileName,'r').read())
  




