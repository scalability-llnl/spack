# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import codecs
import email.message
import errno
import json
import os
import os.path
import re
import shutil
import ssl
import stat
import sys
import traceback
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from typing import IO, Dict, Iterable, List, Optional, Set, Tuple, Union
from urllib.error import HTTPError, URLError
from urllib.request import HTTPSHandler, Request, build_opener

import llnl.url
from llnl.util import lang, tty
from llnl.util.filesystem import mkdirp, rename, working_dir

import spack.config
import spack.error
import spack.util.executable
import spack.util.parallel
import spack.util.path
import spack.util.url as url_util

from .executable import CommandNotFoundError, Executable
from .gcs import GCSBlob, GCSBucket, GCSHandler
from .s3 import UrllibS3Handler, get_s3_session


class DetailedHTTPError(HTTPError):
    def __init__(
        self, req: Request, code: int, msg: str, hdrs: email.message.Message, fp: Optional[IO]
    ) -> None:
        self.req = req
        super().__init__(req.get_full_url(), code, msg, hdrs, fp)

    def __str__(self):
        # Note: HTTPError, is actually a kind of non-seekable response object, so
        # best not to read the response body here (even if it may include a human-readable
        # error message).
        # Note: use self.filename, not self.url, because the latter requires fp to be an
        # IO object, which is not the case after unpickling.
        return f"{self.req.get_method()} {self.filename} returned {self.code}: {self.msg}"

    def __reduce__(self):
        # fp is an IO object and not picklable, the rest should be.
        return DetailedHTTPError, (self.req, self.code, self.msg, self.hdrs, None)


class SpackHTTPDefaultErrorHandler(urllib.request.HTTPDefaultErrorHandler):
    def http_error_default(self, req, fp, code, msg, hdrs):
        raise DetailedHTTPError(req, code, msg, hdrs, fp)


def custom_ssl_certs() -> Optional[Tuple[bool, str]]:
    """Returns a tuple (is_file, path) if custom SSL certifates are configured and valid."""
    ssl_certs = spack.config.get("config:ssl_certs")
    if not ssl_certs:
        return None
    path = spack.util.path.substitute_path_variables(ssl_certs)
    if not os.path.isabs(path):
        tty.debug(f"certs: relative path not allowed: {path}")
        return None
    try:
        st = os.stat(path)
    except OSError as e:
        tty.debug(f"certs: error checking path {path}: {e}")
        return None

    file_type = stat.S_IFMT(st.st_mode)

    if file_type != stat.S_IFREG and file_type != stat.S_IFDIR:
        tty.debug(f"certs: not a file or directory: {path}")
        return None

    return (file_type == stat.S_IFREG, path)


def ssl_create_default_context():
    """Create the default SSL context for urllib with custom certificates if configured."""
    certs = custom_ssl_certs()
    if certs is None:
        return ssl.create_default_context()
    is_file, path = certs
    if is_file:
        tty.debug(f"urllib: certs: using cafile {path}")
        return ssl.create_default_context(cafile=path)
    else:
        tty.debug(f"urllib: certs: using capath {path}")
        return ssl.create_default_context(capath=path)


def set_curl_env_for_ssl_certs(curl: Executable) -> None:
    """configure curl to use custom certs in a file at runtime. See:
    https://curl.se/docs/sslcerts.html item 4"""
    certs = custom_ssl_certs()
    if certs is None:
        return
    is_file, path = certs
    if not is_file:
        tty.debug(f"curl: {path} is not a file: default certs will be used.")
        return
    tty.debug(f"curl: using CURL_CA_BUNDLE={path}")
    curl.add_default_env("CURL_CA_BUNDLE", path)


def _urlopen():
    s3 = UrllibS3Handler()
    gcs = GCSHandler()
    error_handler = SpackHTTPDefaultErrorHandler()

    # One opener with HTTPS ssl enabled
    with_ssl = build_opener(
        s3, gcs, HTTPSHandler(context=ssl_create_default_context()), error_handler
    )

    # One opener with HTTPS ssl disabled
    without_ssl = build_opener(
        s3, gcs, HTTPSHandler(context=ssl._create_unverified_context()), error_handler
    )

    # And dynamically dispatch based on the config:verify_ssl.
    def dispatch_open(fullurl, data=None, timeout=None):
        opener = with_ssl if spack.config.get("config:verify_ssl", True) else without_ssl
        timeout = timeout or spack.config.get("config:connect_timeout", 10)
        return opener.open(fullurl, data, timeout)

    return dispatch_open


#: Dispatches to the correct OpenerDirector.open, based on Spack configuration.
urlopen = lang.Singleton(_urlopen)

#: User-Agent used in Request objects
SPACK_USER_AGENT = "Spackbot/{0}".format(spack.spack_version)


# Also, HTMLParseError is deprecated and never raised.
class HTMLParseError(Exception):
    pass


class LinkParser(HTMLParser):
    """This parser just takes an HTML page and strips out the hrefs on the
    links, as well as some javascript tags used on GitLab servers.
    Good enough for a really simple spider."""

    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.extend(val for key, val in attrs if key == "href")

        # GitLab uses a javascript function to place dropdown links:
        #  <div class="js-source-code-dropdown" ...
        #   data-download-links="[{"path":"/graphviz/graphviz/-/archive/12.0.0/graphviz-12.0.0.zip",...},...]"/>
        if tag == "div" and ("class", "js-source-code-dropdown") in attrs:
            try:
                links_str = next(val for key, val in attrs if key == "data-download-links")
                links = json.loads(links_str)
                self.links.extend(x["path"] for x in links)
            except Exception:
                pass


class ExtractMetadataParser(HTMLParser):
    """This parser takes an HTML page and selects the include-fragments,
    used on GitHub, https://github.github.io/include-fragment-element,
    as well as a possible base url."""

    def __init__(self):
        super().__init__()
        self.fragments = []
        self.base_url = None

    def handle_starttag(self, tag, attrs):
        # <include-fragment src="..." />
        if tag == "include-fragment":
            for attr, val in attrs:
                if attr == "src":
                    self.fragments.append(val)

        # <base href="..." />
        elif tag == "base":
            for attr, val in attrs:
                if attr == "href":
                    self.base_url = val


def read_from_url(url, accept_content_type=None):
    if isinstance(url, str):
        url = urllib.parse.urlparse(url)

    # Timeout in seconds for web requests
    request = Request(url.geturl(), headers={"User-Agent": SPACK_USER_AGENT})

    try:
        response = urlopen(request)
    except (TimeoutError, URLError) as e:
        raise SpackWebError(f"Download of {url.geturl()} failed: {e.__class__.__name__}: {e}")

    if accept_content_type:
        try:
            content_type = get_header(response.headers, "Content-type")
            reject_content_type = not content_type.startswith(accept_content_type)
        except KeyError:
            content_type = None
            reject_content_type = True

        if reject_content_type:
            msg = "ignoring page {}".format(url.geturl())
            if content_type:
                msg += " with content type {}".format(content_type)
            tty.debug(msg)
            return None, None, None

    return response.geturl(), response.headers, response


def push_to_url(local_file_path, remote_path, keep_original=True, extra_args=None):
    remote_url = urllib.parse.urlparse(remote_path)
    if remote_url.scheme == "file":
        remote_file_path = url_util.local_file_path(remote_url)
        mkdirp(os.path.dirname(remote_file_path))
        if keep_original:
            shutil.copy(local_file_path, remote_file_path)
        else:
            try:
                rename(local_file_path, remote_file_path)
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

    elif remote_url.scheme == "s3":
        if extra_args is None:
            extra_args = {}

        remote_path = remote_url.path
        while remote_path.startswith("/"):
            remote_path = remote_path[1:]

        s3 = get_s3_session(remote_url, method="push")
        s3.upload_file(local_file_path, remote_url.netloc, remote_path, ExtraArgs=extra_args)

        if not keep_original:
            os.remove(local_file_path)

    elif remote_url.scheme == "gs":
        gcs = GCSBlob(remote_url)
        gcs.upload_to_blob(local_file_path)
        if not keep_original:
            os.remove(local_file_path)

    else:
        raise NotImplementedError(f"Unrecognized URL scheme: {remote_url.scheme}")


def base_curl_fetch_args(url, timeout=0):
    """Return the basic fetch arguments typically used in calls to curl.

    The arguments include those for ensuring behaviors such as failing on
    errors for codes over 400, printing HTML headers, resolving 3xx redirects,
    status or failure handling, and connection timeouts.

    It also uses the following configuration option to set an additional
    argument as needed:

        * config:connect_timeout (int): connection timeout
        * config:verify_ssl (str): Perform SSL verification

    Arguments:
        url (str): URL whose contents will be fetched
        timeout (int): Connection timeout, which is only used if higher than
            config:connect_timeout

    Returns (list): list of argument strings
    """
    curl_args = [
        "-f",  # fail on >400 errors
        "-D",
        "-",  # "-D -" prints out HTML headers
        "-L",  # resolve 3xx redirects
        url,
    ]
    if not spack.config.get("config:verify_ssl"):
        curl_args.append("-k")

    if sys.stdout.isatty() and tty.msg_enabled():
        curl_args.append("-#")  # status bar when using a tty
    else:
        curl_args.append("-sS")  # show errors if fail

    connect_timeout = spack.config.get("config:connect_timeout", 10)
    if timeout:
        connect_timeout = max(int(connect_timeout), int(timeout))
    if connect_timeout > 0:
        curl_args.extend(["--connect-timeout", str(connect_timeout)])

    return curl_args


def check_curl_code(returncode: int) -> None:
    """Check standard return code failures for provided arguments.

    Arguments:
        returncode: curl return code

    Raises FetchError if the curl returncode indicates failure
    """
    if returncode == 0:
        return
    elif returncode == 22:
        # This is a 404. Curl will print the error.
        raise spack.error.FetchError("URL was not found!")
    elif returncode == 60:
        # This is a certificate error.  Suggest spack -k
        raise spack.error.FetchError(
            "Curl was unable to fetch due to invalid certificate. "
            "This is either an attack, or your cluster's SSL "
            "configuration is bad.  If you believe your SSL "
            "configuration is bad, you can try running spack -k, "
            "which will not check SSL certificates."
            "Use this at your own risk."
        )

    raise spack.error.FetchError(f"Curl failed with error {returncode}")


def require_curl() -> Executable:
    try:
        path = spack.util.executable.which_string("curl", required=True)
    except CommandNotFoundError as e:
        raise spack.error.FetchError(f"curl is required but not found: {e}") from e
    curl = spack.util.executable.Executable(path)
    set_curl_env_for_ssl_certs(curl)
    return curl


def fetch_url_text(url, curl: Optional[Executable] = None, dest_dir="."):
    """Retrieves text-only URL content using the configured fetch method.
    It determines the fetch method from:

        * config:url_fetch_method (str): fetch method to use (e.g., 'curl')

    If the method is `curl`, it also uses the following configuration
    options:

        * config:connect_timeout (int): connection time out
        * config:verify_ssl (str): Perform SSL verification

    Arguments:
        url (str): URL whose contents are to be fetched
        curl (spack.util.executable.Executable or None): (optional) curl
            executable if curl is the configured fetch method
        dest_dir (str): (optional) destination directory for fetched text
            file

    Returns (str or None): path to the fetched file

    Raises FetchError if the curl returncode indicates failure
    """
    if not url:
        raise spack.error.FetchError("A URL is required to fetch its text")

    tty.debug("Fetching text at {0}".format(url))

    filename = os.path.basename(url)
    path = os.path.join(dest_dir, filename)

    fetch_method = spack.config.get("config:url_fetch_method")
    tty.debug("Using '{0}' to fetch {1} into {2}".format(fetch_method, url, path))
    if fetch_method == "curl":
        curl_exe = curl or require_curl()
        curl_args = ["-O"]
        curl_args.extend(base_curl_fetch_args(url))

        # Curl automatically downloads file contents as filename
        with working_dir(dest_dir, create=True):
            _ = curl_exe(*curl_args, fail_on_error=False, output=os.devnull)
            check_curl_code(curl_exe.returncode)

        return path

    else:
        try:
            _, _, response = read_from_url(url)

            returncode = response.getcode()
            if returncode and returncode != 200:
                raise spack.error.FetchError(
                    "Urllib failed with error code {0}".format(returncode)
                )

            output = codecs.getreader("utf-8")(response).read()
            if output:
                with working_dir(dest_dir, create=True):
                    with open(filename, "w") as f:
                        f.write(output)

                return path

        except SpackWebError as err:
            raise spack.error.FetchError("Urllib fetch failed to verify url: {0}".format(str(err)))

    return None


def url_exists(url, curl=None):
    """Determines whether url exists.

    A scheme-specific process is used for Google Storage (`gs`) and Amazon
    Simple Storage Service (`s3`) URLs; otherwise, the configured fetch
    method defined by `config:url_fetch_method` is used.

    Arguments:
        url (str): URL whose existence is being checked
        curl (spack.util.executable.Executable or None): (optional) curl
            executable if curl is the configured fetch method

    Returns (bool): True if it exists; False otherwise.
    """
    tty.debug("Checking existence of {0}".format(url))
    url_result = urllib.parse.urlparse(url)

    # Use curl if configured to do so
    use_curl = spack.config.get(
        "config:url_fetch_method", "urllib"
    ) == "curl" and url_result.scheme not in ("gs", "s3")
    if use_curl:
        curl_exe = curl or require_curl()

        # Telling curl to fetch the first byte (-r 0-0) is supposed to be
        # portable.
        curl_args = ["--stderr", "-", "-s", "-f", "-r", "0-0", url]
        if not spack.config.get("config:verify_ssl"):
            curl_args.append("-k")
        _ = curl_exe(*curl_args, fail_on_error=False, output=os.devnull)
        return curl_exe.returncode == 0

    # Otherwise use urllib.
    try:
        urlopen(
            Request(url, method="HEAD", headers={"User-Agent": SPACK_USER_AGENT}),
            timeout=spack.config.get("config:connect_timeout", 10),
        )
        return True
    except (TimeoutError, URLError) as e:
        tty.debug(f"Failure reading {url}: {e}")
        return False


def _debug_print_delete_results(result):
    if "Deleted" in result:
        for d in result["Deleted"]:
            tty.debug("Deleted {0}".format(d["Key"]))
    if "Errors" in result:
        for e in result["Errors"]:
            tty.debug("Failed to delete {0} ({1})".format(e["Key"], e["Message"]))


def remove_url(url, recursive=False):
    url = urllib.parse.urlparse(url)

    local_path = url_util.local_file_path(url)
    if local_path:
        if recursive:
            shutil.rmtree(local_path)
        else:
            os.remove(local_path)
        return

    if url.scheme == "s3":
        # Try to find a mirror for potential connection information
        s3 = get_s3_session(url, method="push")
        bucket = url.netloc
        if recursive:
            # Because list_objects_v2 can only return up to 1000 items
            # at a time, we have to paginate to make sure we get it all
            prefix = url.path.strip("/")
            paginator = s3.get_paginator("list_objects_v2")
            pages = paginator.paginate(Bucket=bucket, Prefix=prefix)

            delete_request = {"Objects": []}
            for item in pages.search("Contents"):
                if not item:
                    continue

                delete_request["Objects"].append({"Key": item["Key"]})

                # Make sure we do not try to hit S3 with a list of more
                # than 1000 items
                if len(delete_request["Objects"]) >= 1000:
                    r = s3.delete_objects(Bucket=bucket, Delete=delete_request)
                    _debug_print_delete_results(r)
                    delete_request = {"Objects": []}

            # Delete any items that remain
            if len(delete_request["Objects"]):
                r = s3.delete_objects(Bucket=bucket, Delete=delete_request)
                _debug_print_delete_results(r)
        else:
            s3.delete_object(Bucket=bucket, Key=url.path.lstrip("/"))
        return

    elif url.scheme == "gs":
        if recursive:
            bucket = GCSBucket(url)
            bucket.destroy(recursive=recursive)
        else:
            blob = GCSBlob(url)
            blob.delete_blob()
        return

    # Don't even try for other URL schemes.


def _iter_s3_contents(contents, prefix):
    for entry in contents:
        key = entry["Key"]

        if not key.startswith("/"):
            key = "/" + key

        key = os.path.relpath(key, prefix)

        if key == ".":
            continue

        yield key


def _list_s3_objects(client, bucket, prefix, num_entries, start_after=None):
    list_args = dict(Bucket=bucket, Prefix=prefix[1:], MaxKeys=num_entries)

    if start_after is not None:
        list_args["StartAfter"] = start_after

    result = client.list_objects_v2(**list_args)

    last_key = None
    if result["IsTruncated"]:
        last_key = result["Contents"][-1]["Key"]

    iter = _iter_s3_contents(result["Contents"], prefix)

    return iter, last_key


def _iter_s3_prefix(client, url, num_entries=1024):
    key = None
    bucket = url.netloc
    prefix = re.sub(r"^/*", "/", url.path)

    while True:
        contents, key = _list_s3_objects(client, bucket, prefix, num_entries, start_after=key)

        for x in contents:
            yield x

        if not key:
            break


def _iter_local_prefix(path):
    for root, _, files in os.walk(path):
        for f in files:
            yield os.path.relpath(os.path.join(root, f), path)


def list_url(url, recursive=False):
    url = urllib.parse.urlparse(url)
    local_path = url_util.local_file_path(url)

    if local_path:
        if recursive:
            # convert backslash to forward slash as required for URLs
            return [str(PurePosixPath(Path(p))) for p in _iter_local_prefix(local_path)]
        return [
            subpath
            for subpath in os.listdir(local_path)
            if os.path.isfile(os.path.join(local_path, subpath))
        ]

    if url.scheme == "s3":
        s3 = get_s3_session(url, method="fetch")
        if recursive:
            return list(_iter_s3_prefix(s3, url))

        return list(set(key.split("/", 1)[0] for key in _iter_s3_prefix(s3, url)))

    elif url.scheme == "gs":
        gcs = GCSBucket(url)
        return gcs.get_all_blobs(recursive=recursive)


def spider(
    root_urls: Union[str, Iterable[str]], depth: int = 0, concurrency: Optional[int] = None
):
    """Get web pages from root URLs.

    If depth is specified (e.g., depth=2), then this will also follow up to <depth> levels
    of links from each root.

    Args:
        root_urls: root urls used as a starting point for spidering
        depth: level of recursion into links
        concurrency: number of simultaneous requests that can be sent

    Returns:
        A dict of pages visited (URL) mapped to their full text and the set of visited links.
    """
    if isinstance(root_urls, str):
        root_urls = [root_urls]

    current_depth = 0
    pages, links, spider_args = {}, set(), []

    _visited: Set[str] = set()
    go_deeper = current_depth < depth
    for root_str in root_urls:
        root = urllib.parse.urlparse(root_str)
        spider_args.append((root, go_deeper, _visited))

    with spack.util.parallel.make_concurrent_executor(concurrency, require_fork=False) as tp:
        while current_depth <= depth:
            tty.debug(
                f"SPIDER: [depth={current_depth}, max_depth={depth}, urls={len(spider_args)}]"
            )
            results = [tp.submit(_spider, *one_search_args) for one_search_args in spider_args]
            spider_args = []
            go_deeper = current_depth < depth
            for future in results:
                sub_pages, sub_links, sub_spider_args, sub_visited = future.result()
                _visited.update(sub_visited)
                sub_spider_args = [(x, go_deeper, _visited) for x in sub_spider_args]
                pages.update(sub_pages)
                links.update(sub_links)
                spider_args.extend(sub_spider_args)

            current_depth += 1

    return pages, links


def _spider(url: urllib.parse.ParseResult, collect_nested: bool, _visited: Set[str]):
    """Fetches URL and any pages it links to.

    Prints out a warning only if the root can't be fetched; it ignores errors with pages
    that the root links to.

    Args:
        url: url being fetched and searched for links
        collect_nested: whether we want to collect arguments for nested spidering on the
            links found in this url
        _visited: links already visited

    Returns:
        A tuple of:
        - pages: dict of pages visited (URL) mapped to their full text.
        - links: set of links encountered while visiting the pages.
        - spider_args: argument for subsequent call to spider
        - visited: updated set of visited urls
    """
    pages: Dict[str, str] = {}  # dict from page URL -> text content.
    links: Set[str] = set()  # set of all links seen on visited pages.
    subcalls: List[str] = []

    try:
        response_url, _, response = read_from_url(url, "text/html")
        if not response_url or not response:
            return pages, links, subcalls, _visited

        page = codecs.getreader("utf-8")(response).read()
        pages[response_url] = page

        # Parse out the include-fragments in the page
        # https://github.github.io/include-fragment-element
        metadata_parser = ExtractMetadataParser()
        metadata_parser.feed(page)

        # Change of base URL due to <base href="..." /> tag
        response_url = metadata_parser.base_url or response_url

        fragments = set()
        while metadata_parser.fragments:
            raw_link = metadata_parser.fragments.pop()
            abs_link = url_util.join(response_url, raw_link.strip(), resolve_href=True)

            fragment_response_url = None
            try:
                # This seems to be text/html, though text/fragment+html is also used
                fragment_response_url, _, fragment_response = read_from_url(abs_link, "text/html")
            except Exception as e:
                msg = f"Error reading fragment: {(type(e), str(e))}:{traceback.format_exc()}"
                tty.debug(msg)

            if not fragment_response_url or not fragment_response:
                continue

            fragment = codecs.getreader("utf-8")(fragment_response).read()
            fragments.add(fragment)

            pages[fragment_response_url] = fragment

        # Parse out the links in the page and all fragments
        link_parser = LinkParser()
        link_parser.feed(page)
        for fragment in fragments:
            link_parser.feed(fragment)

        while link_parser.links:
            raw_link = link_parser.links.pop()
            abs_link = url_util.join(response_url, raw_link.strip(), resolve_href=True)
            links.add(abs_link)

            # Skip stuff that looks like an archive
            if any(raw_link.endswith(s) for s in llnl.url.ALLOWED_ARCHIVE_TYPES):
                continue

            # Skip already-visited links
            if abs_link in _visited:
                continue

            # If we're not at max depth, follow links.
            if collect_nested:
                subcalls.append(abs_link)
                _visited.add(abs_link)

    except (TimeoutError, URLError) as e:
        tty.debug(f"[SPIDER] Unable to read: {url}")
        tty.debug(str(e), level=2)
        if isinstance(e, URLError) and isinstance(e.reason, ssl.SSLError):
            tty.warn(
                "Spack was unable to fetch url list due to a "
                "certificate verification problem. You can try "
                "running spack -k, which will not check SSL "
                "certificates. Use this at your own risk."
            )

    except HTMLParseError as e:
        # This error indicates that Python's HTML parser sucks.
        msg = "Got an error parsing HTML."
        tty.warn(msg, url, "HTMLParseError: " + str(e))

    except Exception as e:
        # Other types of errors are completely ignored,
        # except in debug mode
        tty.debug(f"Error in _spider: {type(e)}:{str(e)}", traceback.format_exc())

    finally:
        tty.debug(f"SPIDER: [url={url}]")

    return pages, links, subcalls, _visited


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
        return re.sub(r"[ _-]", "", header).lower()

    try:
        return headers[header_name]
    except KeyError:
        unfuzzed_header_name = unfuzz(header_name)
        for header, value in headers.items():
            if unfuzz(header) == unfuzzed_header_name:
                return value
        raise


def parse_etag(header_value):
    """Parse a strong etag from an ETag: <value> header value.
    We don't allow for weakness indicators because it's unclear
    what that means for cache invalidation."""
    if header_value is None:
        return None

    # First follow rfc7232 section 2.3 mostly:
    #  ETag       = entity-tag
    #  entity-tag = [ weak ] opaque-tag
    #  weak       = %x57.2F ; "W/", case-sensitive
    #  opaque-tag = DQUOTE *etagc DQUOTE
    #  etagc      = %x21 / %x23-7E / obs-text
    #             ; VCHAR except double quotes, plus obs-text
    # obs-text    = %x80-FF

    # That means quotes are required.
    valid = re.match(r'"([\x21\x23-\x7e\x80-\xFF]+)"$', header_value)
    if valid:
        return valid.group(1)

    # However, not everybody adheres to the RFC (some servers send
    # wrong etags, but also s3:// is simply a different standard).
    # In that case, it's common that quotes are omitted, everything
    # else stays the same.
    valid = re.match(r"([\x21\x23-\x7e\x80-\xFF]+)$", header_value)

    return valid.group(1) if valid else None


class SpackWebError(spack.error.SpackError):
    """Superclass for Spack web spidering errors."""


class NoNetworkConnectionError(SpackWebError):
    """Raised when an operation can't get an internet connection."""

    def __init__(self, message, url):
        super().__init__("No network connection: " + str(message), "URL was: " + str(url))
        self.url = url
