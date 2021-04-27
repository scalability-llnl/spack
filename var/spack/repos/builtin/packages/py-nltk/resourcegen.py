#!/bin/env python
#
# Helper script for maintainers to autogenerate resources for py-nltk
#
import hashlib
import urllib.request
import xml.etree.ElementTree


url = 'https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/index.xml'
document = urllib.request.urlopen(url).read()
tree = xml.etree.ElementTree.fromstring(document)
packages = tree.findall('./packages/package')
for package in packages:
    url = package.get('url')
    name = package.get('id')
    subdir = package.get('subdir')
    packagebody = urllib.request.urlopen(url).read()
    meta_checksum = package.get('checksum')
    loaded_checksum = hashlib.md5(packagebody).hexdigest()
    if (meta_checksum == loaded_checksum):
        output_checksum = hashlib.sha256(packagebody).hexdigest()
        print("""
        resource(name='{0}',
        url='{1}',
        when='+data',
        sha256='{2}',
        destination='nltk_data/{3}',
        placement='{0}')""".format(name,
                                   url,
                                   output_checksum,
                                   subdir))
    else:
        print("""bad {0}""".format(url))
