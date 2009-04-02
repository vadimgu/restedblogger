from docutils.parsers.rst import roles
from docutils import utils
from docutils import nodes

wikipedia_base_url = 'http://en.wikipedia.org/wiki/'

def wikipedia_reference_role(role, rawtext, text, lineno, inliner,
                       options={}, content=[]):
    wikiterm = text
    wikipedia_page_url = wikipedia_base_url + wikiterm 
    roles.set_classes(options)
    node = nodes.reference(rawtext, utils.unescape(text), refuri=wikipedia_page_url,
                           **options)
    return [node], []

roles.register_local_role('wikipedia-reference', wikipedia_reference_role)
roles.register_local_role('wkp', wikipedia_reference_role)


