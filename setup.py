from setuptools import setup, find_packages

requirements = [
  'docutils',
  'Pygments',
  'BeautifulSoup',
  'gdata',
]

setup(
  name = "RestedBlogger",
  version = "0.0.2",
  packages = find_packages(),
  install_requires = requirements,
  entry_points = {
    'console_scripts':[
      'restedblogger = restedblogger.blogger:main'
      ]
  },
  author = "Vadim Gubergrits",
  author_email = "vadim.gubergrits@gmail.com",
  description="editing blogs in reStructuredText and posting them to blogger.com",
  license = "BSD",
  keywords="reStructuredText blog blogger.com",
  url="",
)

