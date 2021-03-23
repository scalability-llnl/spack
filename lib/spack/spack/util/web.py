# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import codecs
import errno
import multiprocessing.pool
import os
import os.path
import re
import shutil
import ssl
import sys
import traceback

import six
from six.moves.urllib.error import URLError
from six.moves.urllib.request import urlopen, Request

if sys.version_info < (3, 0):
    # Python 2 had these in the HTMLParser package.
    from HTMLParser import HTMLParser, HTMLParseError  # novm
else:
    # In Python 3, things moved to html.parser
    from html.parser import HTMLParser

    # Also, HTMLParseError is deprecated and never raised.
    class HTMLParseError(Exception):
        pass

from llnl.util.filesystem import mkdirp
import llnl.util.tty as tty

import spack.cmd
import spack.config
import spack.error
import spack.url
import spack.util.crypto
import spack.util.s3 as s3_util
import spack.util.url as url_util
import llnl.util.lang

from spack.util.compression import ALLOWED_ARCHIVE_TYPES


# Timeout in seconds for web requests
_timeout = 10


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


def uses_ssl(parsed_url):
    if parsed_url.scheme == 'https':
        return True

    if parsed_url.scheme == 's3':
        endpoint_url = os.environ.get('S3_ENDPOINT_URL')
        if not endpoint_url:
            return True

        if url_util.parse(endpoint_url, scheme='https').scheme == 'https':
            return True

    return False


__UNABLE_TO_VERIFY_SSL = (
    lambda pyver: (
        (pyver < (2, 7, 9)) or
        ((3,) < pyver < (3, 4, 3))
    ))(sys.version_info)


def read_from_url(url, accept_content_type=None):
    url = url_util.parse(url)
    context = None

    verify_ssl = spack.config.get('config:verify_ssl')

    # Don't even bother with a context unless the URL scheme is one that uses
    # SSL certs.
    if uses_ssl(url):
        if verify_ssl:
            if __UNABLE_TO_VERIFY_SSL:
                # User wants SSL verification, but it cannot be provided.
                warn_no_ssl_cert_checking()
            else:
                # User wants SSL verification, and it *can* be provided.
                context = ssl.create_default_context()  # novm
        else:
            # User has explicitly indicated that they do not want SSL
            # verification.
            context = ssl._create_unverified_context()

    req = Request(url_util.format(url))
    content_type = None
    is_web_url = url.scheme in ('http', 'https')
    if accept_content_type and is_web_url:
        # Make a HEAD request first to check the content type.  This lets
        # us ignore tarballs and gigantic files.
        # It would be nice to do this with the HTTP Accept header to avoid
        # one round-trip.  However, most servers seem to ignore the header
        # if you ask for a tarball with Accept: text/html.
        req.get_method = lambda: "HEAD"
        resp = _urlopen(req, timeout=_timeout, context=context)

        content_type = get_header(resp.headers, 'Content-type')

    # Do the real GET request when we know it's just HTML.
    req.get_method = lambda: "GET"

    try:
        response = _urlopen(req, timeout=_timeout, context=context)
    except URLError as err:
        raise SpackWebError('Download failed: {ERROR}'.format(
            ERROR=str(err)))

    if accept_content_type and not is_web_url:
        content_type = get_header(response.headers, 'Content-type')

    reject_content_type = (
        accept_content_type and (
            content_type is None or
            not content_type.startswith(accept_content_type)))

    if reject_content_type:
        tty.debug("ignoring page {0}{1}{2}".format(
            url_util.format(url),
            " with content type " if content_type is not None else "",
            content_type or ""))

        return None, None, None

    return response.geturl(), response.headers, response


def warn_no_ssl_cert_checking():
    tty.warn("Spack will not check SSL certificates. You need to update "
             "your Python to enable certificate verification.")


def push_to_url(
        local_file_path, remote_path, keep_original=True, extra_args=None):
    remote_url = url_util.parse(remote_path)
    verify_ssl = spack.config.get('config:verify_ssl')

    if __UNABLE_TO_VERIFY_SSL and verify_ssl and uses_ssl(remote_url):
        warn_no_ssl_cert_checking()

    remote_file_path = url_util.local_file_path(remote_url)
    if remote_file_path is not None:
        mkdirp(os.path.dirname(remote_file_path))
        if keep_original:
            shutil.copy(local_file_path, remote_file_path)
        else:
            try:
                os.rename(local_file_path, remote_file_path)
            except OSError as e:
                if e.errno == errno.EXDEV:
                    # NOTE(opadron): The above move failed because it crosses
                    # filesystem boundaries.  Copy the file (plus original
                    # metadata), and then delete the original.  This operation
                    # needs to be done in separate steps.
                    shutil.copy2(local_file_path, remote_file_path)
                    os.remove(local_file_path)
                else:
                    raise

    elif remote_url.scheme == 's3':
        if extra_args is None:
            extra_args = {}

        remote_path = remote_url.path
        while remote_path.startswith('/'):
            remote_path = remote_path[1:]

        s3 = s3_util.create_s3_session(remote_url)
        s3.upload_file(local_file_path, remote_url.netloc,
                       remote_path, ExtraArgs=extra_args)

        if not keep_original:
            os.remove(local_file_path)

    else:
        raise NotImplementedError(
            'Unrecognized URL scheme: {SCHEME}'.format(
                SCHEME=remote_url.scheme))


def url_exists(url):
    url = url_util.parse(url)
    local_path = url_util.local_file_path(url)
    if local_path:
        return os.path.exists(local_path)

    if url.scheme == 's3':
        s3 = s3_util.create_s3_session(url)
        from botocore.exceptions import ClientError
        try:
            s3.get_object(Bucket=url.netloc, Key=url.path)
            return True
        except ClientError as err:
            if err.response['Error']['Code'] == 'NoSuchKey':
                return False
            raise err

    # otherwise, just try to "read" from the URL, and assume that *any*
    # non-throwing response contains the resource represented by the URL
    try:
        read_from_url(url)
        return True
    except (SpackWebError, URLError):
        return False


def _debug_print_delete_results(result):
    if 'Deleted' in result:
        for d in result['Deleted']:
            tty.debug('Deleted {0}'.format(d['Key']))
    if 'Errors' in result:
        for e in result['Errors']:
            tty.debug('Failed to delete {0} ({1})'.format(
                e['Key'], e['Message']))


def remove_url(url, recursive=False):
    url = url_util.parse(url)

    local_path = url_util.local_file_path(url)
    if local_path:
        if recursive:
            shutil.rmtree(local_path)
        else:
            os.remove(local_path)
        return

    if url.scheme == 's3':
        s3 = s3_util.create_s3_session(url)
        bucket = url.netloc
        if recursive:
            # Because list_objects_v2 can only return up to 1000 items
            # at a time, we have to paginate to make sure we get it all
            prefix = url.path.strip('/')
            paginator = s3.get_paginator('list_objects_v2')
            pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

            delete_request = {'Objects': []}
            for item in pages.search('Contents'):
                if not item:
                    continue

                delete_request['Objects'].append({'Key': item['Key']})

                # Make sure we do not try to hit S3 with a list of more
                # than 1000 items
                if len(delete_request['Objects']) >= 1000:
                    r = s3.delete_objects(Bucket=bucket, Delete=delete_request)
                    _debug_print_delete_results(r)
                    delete_request = {'Objects': []}

            # Delete any items that remain
            if len(delete_request['Objects']):
                r = s3.delete_objects(Bucket=bucket, Delete=delete_request)
                _debug_print_delete_results(r)
        else:
            s3.delete_object(Bucket=bucket, Key=url.path)
        return

    # Don't even try for other URL schemes.


def _iter_s3_contents(contents, prefix):
    for entry in contents:
        key = entry['Key']

        if not key.startswith('/'):
            key = '/' + key

        key = os.path.relpath(key, prefix)

        if key == '.':
            continue

        yield key


def _list_s3_objects(client, bucket, prefix, num_entries, start_after=None):
    list_args = dict(
        Bucket=bucket,
        Prefix=prefix[1:],
        MaxKeys=num_entries)

    if start_after is not None:
        list_args['StartAfter'] = start_after

    result = client.list_objects_v2(**list_args)

    last_key = None
    if result['IsTruncated']:
        last_key = result['Contents'][-1]['Key']

    iter = _iter_s3_contents(result['Contents'], prefix)

    return iter, last_key


def _iter_s3_prefix(client, url, num_entries=1024):
    key = None
    bucket = url.netloc
    prefix = re.sub(r'^/*', '/', url.path)

    while True:
        contents, key = _list_s3_objects(
            client, bucket, prefix, num_entries, start_after=key)

        for x in contents:
            yield x

        if not key:
            break


def _iter_local_prefix(path):
    for root, _, files in os.walk(path):
        for f in files:
            yield os.path.relpath(os.path.join(root, f), path)


def list_url(url, recursive=False):
    url = url_util.parse(url)

    local_path = url_util.local_file_path(url)
    if local_path:
        if recursive:
            return list(_iter_local_prefix(local_path))
        return [subpath for subpath in os.listdir(local_path)
                if os.path.isfile(os.path.join(local_path, subpath))]

    if url.scheme == 's3':
        s3 = s3_util.create_s3_session(url)
        if recursive:
            return list(_iter_s3_prefix(s3, url))

        return list(set(
            key.split('/', 1)[0]
            for key in _iter_s3_prefix(s3, url)))


def spider(root_urls, depth=0, concurrency=32):
    """Get web pages from root URLs.

    If depth is specified (e.g., depth=2), then this will also follow
    up to <depth> levels of links from each root.

    Args:
        root_urls (str or list of str): root urls used as a starting point
            for spidering
        depth (int): level of recursion into links
        concurrency (int): number of simultaneous requests that can be sent

    Returns:
        A dict of pages visited (URL) mapped to their full text and the
        set of visited links.
    """
    # Cache of visited links, meant to be captured by the closure below
    _visited = set()

    def _spider(url, collect_nested):
        """Fetches URL and any pages it links to.

        Prints out a warning only if the root can't be fetched; it ignores
        errors with pages that the root links to.

        Args:
            url (str): url being fetched and searched for links
            collect_nested (bool): whether we want to collect arguments
                for nested spidering on the links found in this url

        Returns:
            A tuple of:
            - pages: dict of pages visited (URL) mapped to their full text.
            - links: set of links encountered while visiting the pages.
            - spider_args: argument for subsequent call to spider
        """
        pages = {}  # dict from page URL -> text content.
        links = set()  # set of all links seen on visited pages.
        subcalls = []

        try:
            response_url, _, response = read_from_url(url, 'text/html')
            if not response_url or not response:
                return pages, links, subcalls

            page = codecs.getreader('utf-8')(response).read()
            pages[response_url] = page

            # Parse out the links in the page
            link_parser = LinkParser()
            link_parser.feed(page)

            while link_parser.links:
                raw_link = link_parser.links.pop()
                abs_link = url_util.join(
                    response_url,
                    raw_link.strip(),
                    resolve_href=True)
                links.add(abs_link)

                # Skip stuff that looks like an archive
                if any(raw_link.endswith(s) for s in ALLOWED_ARCHIVE_TYPES):
                    continue

                # Skip already-visited links
                if abs_link in _visited:
                    continue

                # If we're not at max depth, follow links.
                if collect_nested:
                    subcalls.append((abs_link,))
                    _visited.add(abs_link)

        except URLError as e:
            tty.debug(str(e))

            if hasattr(e, 'reason') and isinstance(e.reason, ssl.SSLError):
                tty.warn("Spack was unable to fetch url list due to a "
                         "certificate verification problem. You can try "
                         "running spack -k, which will not check SSL "
                         "certificates. Use this at your own risk.")

        except HTMLParseError as e:
            # This error indicates that Python's HTML parser sucks.
            msg = "Got an error parsing HTML."

            # Pre-2.7.3 Pythons in particular have rather prickly HTML parsing.
            if sys.version_info[:3] < (2, 7, 3):
                msg += " Use Python 2.7.3 or newer for better HTML parsing."

            tty.warn(msg, url, "HTMLParseError: " + str(e))

        except Exception as e:
            # Other types of errors are completely ignored,
            # except in debug mode
            tty.debug("Error in _spider: %s:%s" % (type(e), str(e)),
                      traceback.format_exc())

        finally:
            tty.debug("SPIDER: [url={0}]".format(url))

        return pages, links, subcalls

    if isinstance(root_urls, six.string_types):
        root_urls = [root_urls]

    # Clear the local cache of visited pages before starting the search
    _visited.clear()

    current_depth = 0
    pages, links, spider_args = {}, set(), []

    collect = current_depth < depth
    for root in root_urls:
        root = url_util.parse(root)
        spider_args.append((root, collect))

    tp = multiprocessing.pool.ThreadPool(processes=concurrency)
    try:
        while current_depth <= depth:
            tty.debug("SPIDER: [depth={0}, max_depth={1}, urls={2}]".format(
                current_depth, depth, len(spider_args))
            )
            results = tp.map(llnl.util.lang.star(_spider), spider_args)
            spider_args = []
            collect = current_depth < depth
            for sub_pages, sub_links, sub_spider_args in results:
                sub_spider_args = [x + (collect,) for x in sub_spider_args]
                pages.update(sub_pages)
                links.update(sub_links)
                spider_args.extend(sub_spider_args)

            current_depth += 1
    finally:
        tp.terminate()
        tp.join()

    return pages, links


def _urlopen(req, *args, **kwargs):
    """Wrapper for compatibility with old versions of Python."""
    url = req
    try:
        url = url.get_full_url()
    except AttributeError:
        pass

    # We don't pass 'context' parameter because it was only introduced starting
    # with versions 2.7.9 and 3.4.3 of Python.
    if 'context' in kwargs:
        del kwargs['context']

    opener = urlopen
    if url_util.parse(url).scheme == 's3':
        import spack.s3_handler
        opener = spack.s3_handler.open

    return opener(req, *args, **kwargs)


def find_versions_of_archive(
        archive_urls, list_url=None, list_depth=0, concurrency=32
):
    """Scrape web pages for new versions of a tarball.

    Args:
        archive_urls (str or list or tuple): URL or sequence of URLs for
            different versions of a package. Typically these are just the
            tarballs from the package file itself. By default, this searches
            the parent directories of archives.
        list_url (str or None): URL for a listing of archives.
            Spack will scrape these pages for download links that look
            like the archive URL.
        list_depth (int): max depth to follow links on list_url pages.
            Defaults to 0.
        concurrency (int): maximum number of concurrent requests
    """
    if not isinstance(archive_urls, (list, tuple)):
        archive_urls = [archive_urls]

    # Generate a list of list_urls based on archive urls and any
    # explicitly listed list_url in the package
    list_urls = set()
    if list_url is not None:
        list_urls.add(list_url)
    for aurl in archive_urls:
        list_urls |= spack.url.find_list_urls(aurl)

    # Add '/' to the end of the URL. Some web servers require this.
    additional_list_urls = set()
    for lurl in list_urls:
        if not lurl.endswith('/'):
            additional_list_urls.add(lurl + '/')
    list_urls |= additional_list_urls

    # Grab some web pages to scrape.
    pages, links = spider(list_urls, depth=list_depth, concurrency=concurrency)

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

        # We need to add a / to the beginning of the regex to prevent
        # Spack from picking up similarly named packages like:
        #   https://cran.r-project.org/src/contrib/pls_2.6-0.tar.gz
        #   https://cran.r-project.org/src/contrib/enpls_5.7.tar.gz
        #   https://cran.r-project.org/src/contrib/autopls_1.3.tar.gz
        #   https://cran.r-project.org/src/contrib/matrixpls_1.0.4.tar.gz
        url_regex = '/' + url_regex

        # We need to add a $ anchor to the end of the regex to prevent
        # Spack from picking up signature files like:
        #   .asc
        #   .md5
        #   .sha256
        #   .sig
        # However, SourceForge downloads still need to end in '/download'.
        url_regex += r'(\/download)?'
        # PyPI adds #sha256=... to the end of the URL
        url_regex += '(#sha256=.*)?'
        url_regex += '$'

        regexes.append(url_regex)

    # Build a dict version -> URL from any links that match the wildcards.
    # Walk through archive_url links first.
    # Any conflicting versions will be overwritten by the list_url links.
    versions = {}
    for url in archive_urls + sorted(links):
        if any(re.search(r, url) for r in regexes):
            try:
                ver = spack.url.parse_version(url)
                versions[ver] = url
            except spack.url.UndetectableVersionError:
                continue

    return versions


def get_header(headers, header_name):
    """Looks up a dict of headers for the given header value.

    Looks up a dict of headers, [headers], for a header value given by
    [header_name].  Returns headers[header_name] if header_name is in headers.
    Otherwise, the first fuzzy match is returned, if any.

    This fuzzy matching is performed by discarding word separators and
    capitalization, so that for example, "Content-length", "content_length",
    "conTENtLength", etc., all match.  In the case of multiple fuzzy-matches,
    the returned value is the "first" such match given the underlying mapping's
    ordering, or unspecified if no such ordering is defined.

    If header_name is not in headers, and no such fuzzy match exists, then a
    KeyError is raised.
    """

    def unfuzz(header):
        return re.sub(r'[ _-]', '', header).lower()

    try:
        return headers[header_name]
    except KeyError:
        unfuzzed_header_name = unfuzz(header_name)
        for header, value in headers.items():
            if unfuzz(header) == unfuzzed_header_name:
                return value
        raise


class SpackWebError(spack.error.SpackError):
    """Superclass for Spack web spidering errors."""


class NoNetworkConnectionError(SpackWebError):
    """Raised when an operation can't get an internet connection."""
    def __init__(self, message, url):
        super(NoNetworkConnectionError, self).__init__(
            "No network connection: " + str(message),
            "URL was: " + str(url))
        self.url = url
