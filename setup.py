from setuptools import setup

setup(
    name = 'presidency',
    packages = ['presidency'],
    version = '0.13',
    description = 'A Python wrapper for data on the American Presidency Project (www.presidency.ucsb.edu)',
    author = 'Jay Ravaliya',
    author_email = 'jayrav13@gmail.com',
    url = 'https://github.com/jayrav13/presidency',
    download_url = 'https://github.com/jayrav13/presidency/tarball/0.13',
    keywords = ['wrapper', 'american', 'america', 'presidents', 'president', 'presidency'],
    classifiers = [],
    install_requires = ['lxml', 'requests']
)