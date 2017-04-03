##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import re
import os
import sys
import traceback

from six.moves.urllib.request import urlopen, Request
from six.moves.urllib.error import URLError
from six.moves.urllib.parse import urljoin
import multiprocessing.pool

try:
    # Python 2 had these in the HTMLParser package.
    from HTMLParser import HTMLParser, HTMLParseError
except ImportError:
    # In Python 3, things moved to html.parser
    from html.parser import HTMLParser

    # Also, HTMLParseError is deprecated and never raised.
    class HTMLParseError(Exception):
        pass

import llnl.util.tty as tty

import spack
import spack.error
from spack.util.compression import ALLOWED_ARCHIVE_TYPES

# Timeout in seconds for web requests
TIMEOUT = 10


class LinkParser(HTMLParser):
    """This parser just takes an HTML page and strips out the hrefs on the
       links.  Good enough for a really simple spider. """

    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for attr, val in attrs:
                if attr == 'href':
                    self.links.append(val)


class NonDaemonProcess(multiprocessing.Process):
    """Process tha allows sub-processes, so pools can have sub-pools."""
    def _get_daemon(self):
        return False

    def _set_daemon(self, value):
        pass

    daemon = property(_get_daemon, _set_daemon)


class NonDaemonPool(multiprocessing.pool.Pool):
    """Pool that uses non-daemon processes"""
    Process = NonDaemonProcess


def _spider(url, visited, root, depth, max_depth, raise_on_error):
    """Fetches URL and any pages it links to up to max_depth.

       depth should initially be zero, and max_depth is the max depth of
       links to follow from the root.

       Prints out a warning only if the root can't be fetched; it ignores
       errors with pages that the root links to.

       Returns a tuple of:
       - pages: dict of pages visited (URL) mapped to their full text.
       - links: set of links encountered while visiting the pages.
    """
    pages = {}     # dict from page URL -> text content.
    links = set()  # set of all links seen on visited pages.

    # root may end with index.html -- chop that off.
    if root.endswith('/index.html'):
        root = re.sub('/index.html$', '', root)

    try:
        # Make a HEAD request first to check the content type.  This lets
        # us ignore tarballs and gigantic files.
        # It would be nice to do this with the HTTP Accept header to avoid
        # one round-trip.  However, most servers seem to ignore the header
        # if you ask for a tarball with Accept: text/html.
        req = Request(url)
        req.get_method = lambda: "HEAD"
        resp = urlopen(req, timeout=TIMEOUT)

        if "Content-type" not in resp.headers:
            tty.debug("ignoring page " + url)
            return pages, links

        if not resp.headers["Content-type"].startswith('text/html'):
            tty.debug("ignoring page " + url + " with content type " +
                      resp.headers["Content-type"])
            return pages, links

        # Do the real GET request when we know it's just HTML.
        req.get_method = lambda: "GET"
        response = urlopen(req, timeout=TIMEOUT)
        response_url = response.geturl()

        # Read the page and and stick it in the map we'll return
        page = response.read().decode('utf-8')
        pages[response_url] = page

        # Parse out the links in the page
        link_parser = LinkParser()
        subcalls = []
        link_parser.feed(page)

        while link_parser.links:
            raw_link = link_parser.links.pop()
            abs_link = urljoin(response_url, raw_link.strip())

            links.add(abs_link)

            # Skip stuff that looks like an archive
            if any(raw_link.endswith(suf) for suf in ALLOWED_ARCHIVE_TYPES):
                continue

            # Skip things outside the root directory
            if not abs_link.startswith(root):
                continue

            # Skip already-visited links
            if abs_link in visited:
                continue

            # If we're not at max depth, follow links.
            if depth < max_depth:
                subcalls.append((abs_link, visited, root,
                                 depth + 1, max_depth, raise_on_error))
                visited.add(abs_link)

        if subcalls:
            pool = NonDaemonPool(processes=len(subcalls))
            try:
                results = pool.map(_spider_wrapper, subcalls)

                for sub_pages, sub_links in results:
                    pages.update(sub_pages)
                    links.update(sub_links)

            finally:
                pool.terminate()
                pool.join()

    except URLError as e:
        tty.debug(e)
        if raise_on_error:
            raise spack.error.NoNetworkConnectionError(str(e), url)

    except HTMLParseError as e:
        # This error indicates that Python's HTML parser sucks.
        msg = "Got an error parsing HTML."

        # Pre-2.7.3 Pythons in particular have rather prickly HTML parsing.
        if sys.version_info[:3] < (2, 7, 3):
            msg += " Use Python 2.7.3 or newer for better HTML parsing."

        tty.warn(msg, url, "HTMLParseError: " + str(e))

    except Exception as e:
        # Other types of errors are completely ignored, except in debug mode.
        tty.debug("Error in _spider: %s:%s" % (type(e), e),
                  traceback.format_exc())

    return pages, links


def _spider_wrapper(args):
    """Wrapper for using spider with multiprocessing."""
    return _spider(*args)


def spider(root_url, depth=0):

    """Gets web pages from a root URL.

       If depth is specified (e.g., depth=2), then this will also follow
       up to <depth> levels of links from the root.

       This will spawn processes to fetch the children, for much improved
       performance over a sequential fetch.

    """
    pages, links = _spider(root_url, set(), root_url, 0, depth, False)
    return pages, links


def find_versions_of_archive(archive_urls, list_url=None, list_depth=0):
    """Scrape web pages for new versions of a tarball.

    Arguments:
      archive_urls:
          URL or sequence of URLs for different versions of a
          package. Typically these are just the tarballs from the package
          file itself.  By default, this searches the parent directories
          of archives.

    Keyword Arguments:
      list_url:
          URL for a listing of archives.  Spack wills scrape these
          pages for download links that look like the archive URL.

      list_depth:
          Max depth to follow links on list_url pages. Default 0.

    """
    if not isinstance(archive_urls, (list, tuple)):
        archive_urls = [archive_urls]

    # Generate a list of list_urls based on archive urls and any
    # explicitly listed list_url in the package
    list_urls = set()
    if list_url:
        list_urls.add(list_url)
    for aurl in archive_urls:
        list_urls.add(spack.url.find_list_url(aurl))

    # Grab some web pages to scrape.
    pages = {}
    links = set()
    for lurl in list_urls:
        p, l = spider(lurl, depth=list_depth)
        pages.update(p)
        links.update(l)

    # Scrape them for archive URLs
    regexes = []
    for aurl in archive_urls:
        # This creates a regex from the URL with a capture group for
        # the version part of the URL.  The capture group is converted
        # to a generic wildcard, so we can use this to extract things
        # on a page that look like archive URLs.
        url_regex = spack.url.wildcard_version(aurl)

        # We'll be a bit more liberal and just look for the archive
        # part, not the full path.
        url_regex = os.path.basename(url_regex)

        # We need to add a $ anchor to the end of the regex to prevent
        # Spack from picking up signature files like:
        #   .asc
        #   .md5
        #   .sha256
        #   .sig
        # However, SourceForge downloads still need to end in '/download'.
        regexes.append(url_regex + '(\/download)?$')

    # Build a dict version -> URL from any links that match the wildcards.
    versions = {}
    for url in links:
        if any(re.search(r, url) for r in regexes):
            try:
                ver = spack.url.parse_version(url)
                versions[ver] = url
            except spack.url.UndetectableVersionError:
                continue

    return versions
