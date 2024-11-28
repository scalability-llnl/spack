# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module has methods for parsing names and versions of packages from URLs.
The idea is to allow package creators to supply nothing more than the
download location of the package, and figure out version and name information
from there.

**Example:** when spack is given the following URL:

    https://www.hdfgroup.org/ftp/HDF/releases/HDF4.2.12/src/hdf-4.2.12.tar.gz

It can figure out that the package name is ``hdf``, and that it is at version
``4.2.12``. This is useful for making the creation of packages simple: a user
just supplies a URL and skeleton code is generated automatically.

Spack can also figure out that it can most likely download 4.2.6 at this URL:

    https://www.hdfgroup.org/ftp/HDF/releases/HDF4.2.6/src/hdf-4.2.6.tar.gz

This is useful if a user asks for a package at a particular version number;
spack doesn't need anyone to tell it where to get the tarball even though
it's never been told about that version before.
"""
import io
import os
import pathlib
import re
from typing import Any, Dict, Optional, Sequence, Union

import llnl.url
from llnl.path import convert_to_posix_path
from llnl.util.tty.color import cescape, colorize

import spack.error
import spack.util.web
import spack.version

#
# Note: We call the input to most of these functions a "path" but the functions
# work on paths and URLs.  There's not a good word for both of these, but
# "path" seemed like the most generic term.
#


def strip_name_suffixes(path, version):
    """Most tarballs contain a package name followed by a version number.
    However, some also contain extraneous information in-between the name
    and version:

    * ``rgb-1.0.6``
    * ``converge_install_2.3.16``
    * ``jpegsrc.v9b``

    These strings are not part of the package name and should be ignored.
    This function strips the version number and any extraneous suffixes
    off and returns the remaining string. The goal is that the name is
    always the last thing in ``path``:

    * ``rgb``
    * ``converge``
    * ``jpeg``

    Args:
        path (str): The filename or URL for the package
        version (str): The version detected for this URL

    Returns:
        str: The ``path`` with any extraneous suffixes removed
    """
    # NOTE: This could be done with complicated regexes in parse_name_offset
    # NOTE: The problem is that we would have to add these regexes to every
    # NOTE: single name regex. Easier to just strip them off permanently

    suffix_regexes = [
        # Strip off the version and anything after it
        # name-ver
        # name_ver
        # name.ver
        r"[._-][rvV]?" + str(version) + ".*",
        # namever
        r"V?" + str(version) + ".*",
        # Download type
        r"install",
        r"[Ss]rc",
        r"(open)?[Ss]ources?",
        r"[._-]open",
        r"[._-]archive",
        r"[._-]std",
        r"[._-]bin",
        r"Software",
        # Download version
        r"release",
        r"snapshot",
        r"distrib",
        r"everywhere",
        r"latest",
        # Arch
        r"Linux(64)?",
        r"x86_64",
        # VCS
        r"0\+bzr",
        # License
        r"gpl",
        # Needs to come before and after gpl, appears in both orders
        r"[._-]x11",
        r"gpl",
    ]

    for regex in suffix_regexes:
        # Remove the suffix from the end of the path
        # This may be done multiple times
        path = re.sub("[._-]?" + regex + "$", "", path)

    return path


def parse_version_offset(path):
    """Try to extract a version string from a filename or URL.

    Args:
        path (str): The filename or URL for the package

    Returns:
        tuple: A tuple containing:
            version of the package,
            first index of version,
            length of version string,
            the index of the matching regex,
            the matching regex

    Raises:
        UndetectableVersionError: If the URL does not match any regexes
    """
    original_path = path

    # path:   The prefix of the URL, everything before the ext and suffix
    # ext:    The file extension
    # suffix: Any kind of query string that begins with a '?'
    path, ext, suffix = llnl.url.split_url_extension(path)

    # stem:   Everything from path after the final '/'
    original_stem = os.path.basename(path)

    # Try to strip off anything after the version number
    stem = llnl.url.strip_version_suffixes(original_stem)

    # Assumptions:
    #
    # 1. version always comes after the name
    # 2. separators include '-', '_', and '.'
    # 3. names can contain A-Z, a-z, 0-9, '+', separators
    # 4. versions can contain A-Z, a-z, 0-9, separators
    # 5. versions always start with a digit
    # 6. versions are often prefixed by a 'v' or 'r' character
    # 7. separators are most reliable to determine name/version boundaries

    # List of the following format:
    #
    # [
    #     (regex, string),
    #     ...
    # ]
    #
    # The first regex that matches string will be used to determine
    # the version of the package. Thefore, hyperspecific regexes should
    # come first while generic, catch-all regexes should come last.
    # With that said, regular expressions are slow, so if possible, put
    # ones that only catch one or two URLs at the bottom.
    version_regexes = [
        # 1st Pass: Simplest case
        # Assume name contains no digits and version contains no letters
        # e.g. libpng-1.6.27
        (r"^[a-zA-Z+._-]+[._-]v?(\d[\d._-]*)$", stem),
        # 2nd Pass: Version only
        # Assume version contains no letters
        # ver
        # e.g. 3.2.7, 7.0.2-7, v3.3.0, v1_6_3
        (r"^v?(\d[\d._-]*)$", stem),
        # 3rd Pass: No separator characters are used
        # Assume name contains no digits
        # namever
        # e.g. turbolinux702, nauty26r7
        (r"^[a-zA-Z+]*(\d[\da-zA-Z]*)$", stem),
        # 4th Pass: A single separator character is used
        # Assume name contains no digits
        # name-name-ver-ver
        # e.g. panda-2016-03-07, gts-snapshot-121130, cdd-061a
        (r"^[a-zA-Z+-]*(\d[\da-zA-Z-]*)$", stem),
        # name_name_ver_ver
        # e.g. tinyxml_2_6_2, boost_1_55_0, tbb2017_20161128
        (r"^[a-zA-Z+_]*(\d[\da-zA-Z_]*)$", stem),
        # name.name.ver.ver
        # e.g. prank.source.150803, jpegsrc.v9b, atlas3.11.34, geant4.10.01.p03
        (r"^[a-zA-Z+.]*(\d[\da-zA-Z.]*)$", stem),
        # 5th Pass: Two separator characters are used
        # Name may contain digits, version may contain letters
        # name-name-ver.ver
        # e.g. m4-1.4.17, gmp-6.0.0a, launchmon-v1.0.2
        (r"^[a-zA-Z\d+-]+-v?(\d[\da-zA-Z.]*)$", stem),
        # name-name-ver_ver
        # e.g. icu4c-57_1
        (r"^[a-zA-Z\d+-]+-v?(\d[\da-zA-Z_]*)$", stem),
        # name_name_ver.ver
        # e.g. superlu_dist_4.1, pexsi_v0.9.0
        (r"^[a-zA-Z\d+_]+_v?(\d[\da-zA-Z.]*)$", stem),
        # name_name.ver.ver
        # e.g. fer_source.v696
        (r"^[a-zA-Z\d+_]+\.v?(\d[\da-zA-Z.]*)$", stem),
        # name_ver-ver
        # e.g. Bridger_r2014-12-01
        (r"^[a-zA-Z\d+]+_r?(\d[\da-zA-Z-]*)$", stem),
        # name-name-ver.ver-ver.ver
        # e.g. sowing-1.1.23-p1, bib2xhtml-v3.0-15-gf506, 4.6.3-alpha04
        (r"^(?:[a-zA-Z\d+-]+-)?v?(\d[\da-zA-Z.-]*)$", stem),
        # namever.ver-ver.ver
        # e.g. go1.4-bootstrap-20161024
        (r"^[a-zA-Z+]+v?(\d[\da-zA-Z.-]*)$", stem),
        # 6th Pass: All three separator characters are used
        # Name may contain digits, version may contain letters
        # name_name-ver.ver
        # e.g. the_silver_searcher-0.32.0, sphinx_rtd_theme-0.1.10a0
        (r"^[a-zA-Z\d+_]+-v?(\d[\da-zA-Z.]*)$", stem),
        # name.name_ver.ver-ver.ver
        # e.g. TH.data_1.0-8, XML_3.98-1.4
        (r"^[a-zA-Z\d+.]+_v?(\d[\da-zA-Z.-]*)$", stem),
        # name-name-ver.ver_ver.ver
        # e.g. pypar-2.1.5_108
        (r"^[a-zA-Z\d+-]+-v?(\d[\da-zA-Z._]*)$", stem),
        # name.name_name-ver.ver
        # e.g. tap.py-1.6, backports.ssl_match_hostname-3.5.0.1
        (r"^[a-zA-Z\d+._]+-v?(\d[\da-zA-Z.]*)$", stem),
        # name-namever.ver_ver.ver
        # e.g. STAR-CCM+11.06.010_02
        (r"^[a-zA-Z+-]+(\d[\da-zA-Z._]*)$", stem),
        # name-name_name-ver.ver
        # e.g. PerlIO-utf8_strict-0.002
        (r"^[a-zA-Z\d+_-]+-v?(\d[\da-zA-Z.]*)$", stem),
        # 7th Pass: Specific VCS
        # bazaar
        # e.g. libvterm-0+bzr681
        (r"bzr(\d[\da-zA-Z._-]*)$", stem),
        # 8th Pass: Query strings
        # e.g. https://gitlab.cosma.dur.ac.uk/api/v4/projects/swift%2Fswiftsim/repository/archive.tar.gz?sha=v0.3.0
        # e.g. https://gitlab.kitware.com/api/v4/projects/icet%2Ficet/repository/archive.tar.bz2?sha=IceT-2.1.1
        # e.g. http://gitlab.cosma.dur.ac.uk/swift/swiftsim/repository/archive.tar.gz?ref=v0.3.0
        # e.g. http://apps.fz-juelich.de/jsc/sionlib/download.php?version=1.7.1
        # e.g. https://software.broadinstitute.org/gatk/download/auth?package=GATK-archive&version=3.8-1-0-gf15c1c3ef
        (r"[?&](?:sha|ref|version)=[a-zA-Z\d+-]*[_-]?v?(\d[\da-zA-Z._-]*)$", suffix),
        # e.g. http://slepc.upv.es/download/download.php?filename=slepc-3.6.2.tar.gz
        # e.g. http://laws-green.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0beta.1_r20171213193219.tgz
        # e.g. https://evtgen.hepforge.org/downloads?f=EvtGen-01.07.00.tar.gz
        # e.g. http://wwwpub.zih.tu-dresden.de/%7Emlieber/dcount/dcount.php?package=otf&get=OTF-1.12.5salmon.tar.gz
        (r"[?&](?:filename|f|get)=[a-zA-Z\d+-]+[_-]v?(\d[\da-zA-Z.]*)", stem),
        # 9th Pass: Version in path
        # github.com/repo/name/releases/download/vver/name
        # e.g. https://github.com/nextflow-io/nextflow/releases/download/v0.20.1/nextflow
        # e.g. https://gitlab.com/hpctoolkit/hpcviewer/-/releases/2024.02/downloads/hpcviewer.tgz
        (r"github\.com/[^/]+/[^/]+/releases/download/[a-zA-Z+._-]*v?(\d[\da-zA-Z._-]*)/", path),
        (r"gitlab\.com/[^/]+/.+/-/releases/[a-zA-Z+._-]*v?(\d[\da-zA-Z._-]*)/downloads/", path),
        # e.g. ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/2.2.26/ncbi.tar.gz
        (r"(\d[\da-zA-Z._-]*)/[^/]+$", path),
    ]

    for i, version_regex in enumerate(version_regexes):
        regex, match_string = version_regex
        match = re.search(regex, match_string)
        if match and match.group(1) is not None:
            version = match.group(1)
            start = match.start(1)

            # If we matched from the stem or suffix, we need to add offset
            offset = 0
            if match_string is stem:
                offset = len(path) - len(original_stem)
            elif match_string is suffix:
                offset = len(path)
                if ext:
                    offset += len(ext) + 1  # .tar.gz is converted to tar.gz
            start += offset

            return version, start, len(version), i, regex

    raise UndetectableVersionError(original_path)


def parse_version(path: str) -> spack.version.StandardVersion:
    """Try to extract a version string from a filename or URL.

    Args:
        path: The filename or URL for the package

    Returns: The version of the package

    Raises:
        UndetectableVersionError: If the URL does not match any regexes
    """
    version, start, length, i, regex = parse_version_offset(path)
    return spack.version.StandardVersion.from_string(version)


def parse_name_offset(path, v=None):
    """Try to determine the name of a package from its filename or URL.

    Args:
        path (str): The filename or URL for the package
        v (str): The version of the package

    Returns:
        tuple: A tuple containing:
            name of the package,
            first index of name,
            length of name,
            the index of the matching regex,
            the matching regex

    Raises:
        UndetectableNameError: If the URL does not match any regexes
    """
    original_path = path

    # We really need to know the version of the package
    # This helps us prevent collisions between the name and version
    if v is None:
        try:
            v = parse_version(path)
        except UndetectableVersionError:
            # Not all URLs contain a version. We still want to be able
            # to determine a name if possible.
            v = "unknown"

    # path:   The prefix of the URL, everything before the ext and suffix
    # ext:    The file extension
    # suffix: Any kind of query string that begins with a '?'
    path, ext, suffix = llnl.url.split_url_extension(path)

    # stem:   Everything from path after the final '/'
    original_stem = os.path.basename(path)

    # Try to strip off anything after the package name
    stem = strip_name_suffixes(original_stem, v)

    # List of the following format:
    #
    # [
    #     (regex, string),
    #     ...
    # ]
    #
    # The first regex that matches string will be used to determine
    # the name of the package. Thefore, hyperspecific regexes should
    # come first while generic, catch-all regexes should come last.
    # With that said, regular expressions are slow, so if possible, put
    # ones that only catch one or two URLs at the bottom.
    name_regexes = [
        # 1st Pass: Common repositories
        # GitHub: github.com/repo/name/
        # e.g. https://github.com/nco/nco/archive/4.6.2.tar.gz
        (r"github\.com/[^/]+/([^/]+)", path),
        # GitLab API endpoint: gitlab.*/api/v4/projects/NAMESPACE%2Fname/
        # e.g. https://gitlab.cosma.dur.ac.uk/api/v4/projects/swift%2Fswiftsim/repository/archive.tar.gz?sha=v0.3.0
        (r"gitlab[^/]+/api/v4/projects/[^/]+%2F([^/]+)", path),
        # GitLab non-API endpoint: gitlab.*/repo/name/
        # e.g. http://gitlab.cosma.dur.ac.uk/swift/swiftsim/repository/archive.tar.gz?ref=v0.3.0
        (r"gitlab[^/]+/(?!api/v4/projects)[^/]+/([^/]+)", path),
        # Bitbucket: bitbucket.org/repo/name/
        # e.g. https://bitbucket.org/glotzer/hoomd-blue/get/v1.3.3.tar.bz2
        (r"bitbucket\.org/[^/]+/([^/]+)", path),
        # PyPI: pypi.(python.org|io)/packages/source/first-letter/name/
        # e.g. https://pypi.python.org/packages/source/m/mpmath/mpmath-all-0.19.tar.gz
        # e.g. https://pypi.io/packages/source/b/backports.ssl_match_hostname/backports.ssl_match_hostname-3.5.0.1.tar.gz
        (r"pypi\.(?:python\.org|io)/packages/source/[A-Za-z\d]/([^/]+)", path),
        # 2nd Pass: Query strings
        # ?filename=name-ver.ver
        # e.g. http://slepc.upv.es/download/download.php?filename=slepc-3.6.2.tar.gz
        (r"\?filename=([A-Za-z\d+-]+)$", stem),
        # ?f=name-ver.ver
        # e.g. https://evtgen.hepforge.org/downloads?f=EvtGen-01.07.00.tar.gz
        (r"\?f=([A-Za-z\d+-]+)$", stem),
        # ?package=name
        # e.g. http://wwwpub.zih.tu-dresden.de/%7Emlieber/dcount/dcount.php?package=otf&get=OTF-1.12.5salmon.tar.gz
        (r"\?package=([A-Za-z\d+-]+)", stem),
        # ?package=name-version
        (r"\?package=([A-Za-z\d]+)", suffix),
        # download.php
        # e.g. http://apps.fz-juelich.de/jsc/sionlib/download.php?version=1.7.1
        (r"([^/]+)/download.php$", path),
        # 3rd Pass: Name followed by version in archive
        (r"^([A-Za-z\d+\._-]+)$", stem),
    ]

    for i, name_regex in enumerate(name_regexes):
        regex, match_string = name_regex
        match = re.search(regex, match_string)
        if match:
            name = match.group(1)
            start = match.start(1)

            # If we matched from the stem or suffix, we need to add offset
            offset = 0
            if match_string is stem:
                offset = len(path) - len(original_stem)
            elif match_string is suffix:
                offset = len(path)
                if ext:
                    offset += len(ext) + 1  # .tar.gz is converted to tar.gz
            start += offset

            return name, start, len(name), i, regex

    raise UndetectableNameError(original_path)


def parse_name(path, ver=None):
    """Try to determine the name of a package from its filename or URL.

    Args:
        path (str): The filename or URL for the package
        ver (str): The version of the package

    Returns:
        str: The name of the package

    Raises:
        UndetectableNameError: If the URL does not match any regexes
    """
    name, start, length, i, regex = parse_name_offset(path, ver)
    return name


def parse_name_and_version(path):
    """Try to determine the name of a package and extract its version
    from its filename or URL.

    Args:
        path (str): The filename or URL for the package

    Returns:
        tuple: a tuple containing the package (name, version)

    Raises:
        UndetectableVersionError: If the URL does not match any regexes
        UndetectableNameError: If the URL does not match any regexes
    """
    ver = parse_version(path)
    name = parse_name(path, ver)
    return (name, ver)


def find_all(substring, string):
    """Returns a list containing the indices of
    every occurrence of substring in string."""

    occurrences = []
    index = 0
    while index < len(string):
        index = string.find(substring, index)
        if index == -1:
            break
        occurrences.append(index)
        index += len(substring)

    return occurrences


def substitution_offsets(path):
    """This returns offsets for substituting versions and names in the
    provided path.  It is a helper for :func:`substitute_version`.
    """
    # Get name and version offsets
    try:
        ver, vs, vl, vi, vregex = parse_version_offset(path)
        name, ns, nl, ni, nregex = parse_name_offset(path, ver)
    except UndetectableNameError:
        return (None, -1, -1, (), ver, vs, vl, (vs,))
    except UndetectableVersionError:
        try:
            name, ns, nl, ni, nregex = parse_name_offset(path)
            return (name, ns, nl, (ns,), None, -1, -1, ())
        except UndetectableNameError:
            return (None, -1, -1, (), None, -1, -1, ())

    # Find the index of every occurrence of name and ver in path
    name_offsets = find_all(name, path)
    ver_offsets = find_all(ver, path)

    return (name, ns, nl, name_offsets, ver, vs, vl, ver_offsets)


def wildcard_version(path):
    """Find the version in the supplied path, and return a regular expression
    that will match this path with any version in its place.
    """
    # Get version so we can replace it with a wildcard
    version = parse_version(path)

    # Split path by versions
    vparts = path.split(str(version))

    # Replace each version with a generic capture group to find versions
    # and escape everything else so it's not interpreted as a regex
    result = r"(\d.*)".join(re.escape(vp) for vp in vparts)

    return result


def substitute_version(path, new_version):
    """Given a URL or archive name, find the version in the path and
    substitute the new version for it.  Replace all occurrences of
    the version *if* they don't overlap with the package name.

    Simple example:

    .. code-block:: python

       substitute_version('http://www.mr511.de/software/libelf-0.8.13.tar.gz', '2.9.3')
       >>> 'http://www.mr511.de/software/libelf-2.9.3.tar.gz'

    Complex example:

    .. code-block:: python

       substitute_version('https://www.hdfgroup.org/ftp/HDF/releases/HDF4.2.12/src/hdf-4.2.12.tar.gz', '2.3')
       >>> 'https://www.hdfgroup.org/ftp/HDF/releases/HDF2.3/src/hdf-2.3.tar.gz'
    """
    (name, ns, nl, noffs, ver, vs, vl, voffs) = substitution_offsets(path)

    new_path = ""
    last = 0
    for vo in voffs:
        new_path += path[last:vo]
        new_path += str(new_version)
        last = vo + vl

    new_path += path[last:]
    return new_path


def color_url(path, **kwargs):
    """Color the parts of the url according to Spack's parsing.

    Colors are:
       | Cyan: The version found by :func:`parse_version_offset`.
       | Red:  The name found by :func:`parse_name_offset`.

       | Green:   Instances of version string from :func:`substitute_version`.
       | Magenta: Instances of the name (protected from substitution).

    Args:
        path (str): The filename or URL for the package
        errors (bool): Append parse errors at end of string.
        subs (bool): Color substitutions as well as parsed name/version.
    """
    # Allow URLs containing @ and }
    path = cescape(path)

    errors = kwargs.get("errors", False)
    subs = kwargs.get("subs", False)

    (name, ns, nl, noffs, ver, vs, vl, voffs) = substitution_offsets(path)

    nends = [no + nl - 1 for no in noffs]
    vends = [vo + vl - 1 for vo in voffs]

    nerr = verr = 0
    out = io.StringIO()
    for i in range(len(path)):
        if i == vs:
            out.write("@c")
            verr += 1
        elif i == ns:
            out.write("@r")
            nerr += 1
        elif subs:
            if i in voffs:
                out.write("@g")
            elif i in noffs:
                out.write("@m")

        out.write(path[i])

        if i == vs + vl - 1:
            out.write("@.")
            verr += 1
        elif i == ns + nl - 1:
            out.write("@.")
            nerr += 1
        elif subs:
            if i in vends or i in nends:
                out.write("@.")

    if errors:
        if nerr == 0:
            out.write(" @r{[no name]}")
        if verr == 0:
            out.write(" @r{[no version]}")
        if nerr == 1:
            out.write(" @r{[incomplete name]}")
        if verr == 1:
            out.write(" @r{[incomplete version]}")

    return colorize(out.getvalue())


def find_versions_of_archive(
    archive_urls: Union[str, Sequence[str]],
    list_url: Optional[str] = None,
    list_depth: int = 0,
    concurrency: Optional[int] = 32,
    reference_package: Optional[Any] = None,
) -> Dict[spack.version.StandardVersion, str]:
    """Scrape web pages for new versions of a tarball. This function prefers URLs in the
    following order: links found on the scraped page that match a url generated by the
    reference package, found and in the archive_urls list, found and derived from those
    in the archive_urls list, and if none are found for a version then the item in the
    archive_urls list is included for the version.

    Args:
        archive_urls: URL or sequence of URLs for different versions of a package. Typically these
            are just the tarballs from the package file itself. By default, this searches the
            parent directories of archives.
        list_url: URL for a listing of archives. Spack will scrape these pages for download links
            that look like the archive URL.
        list_depth: max depth to follow links on list_url pages. Defaults to 0.
        concurrency: maximum number of concurrent requests
        reference_package: a spack package used as a reference for url detection. Uses the
            url_for_version method on the package to produce reference urls which, if found, are
            preferred.
    """
    if isinstance(archive_urls, str):
        archive_urls = [archive_urls]

    # Generate a list of list_urls based on archive urls and any
    # explicitly listed list_url in the package
    list_urls = set()
    if list_url is not None:
        list_urls.add(list_url)
    for aurl in archive_urls:
        list_urls |= llnl.url.find_list_urls(aurl)

    # Add '/' to the end of the URL. Some web servers require this.
    additional_list_urls = set()
    for lurl in list_urls:
        if not lurl.endswith("/"):
            additional_list_urls.add(lurl + "/")
    list_urls |= additional_list_urls

    # Grab some web pages to scrape.
    _, links = spack.util.web.spider(list_urls, depth=list_depth, concurrency=concurrency)

    # Scrape them for archive URLs
    regexes = []
    for aurl in archive_urls:
        # This creates a regex from the URL with a capture group for
        # the version part of the URL.  The capture group is converted
        # to a generic wildcard, so we can use this to extract things
        # on a page that look like archive URLs.
        url_regex = wildcard_version(aurl)

        # We'll be a bit more liberal and just look for the archive
        # part, not the full path.
        # this is a URL so it is a posixpath even on Windows
        url_regex = pathlib.PurePosixPath(url_regex).name

        # We need to add a / to the beginning of the regex to prevent
        # Spack from picking up similarly named packages like:
        #   https://cran.r-project.org/src/contrib/pls_2.6-0.tar.gz
        #   https://cran.r-project.org/src/contrib/enpls_5.7.tar.gz
        #   https://cran.r-project.org/src/contrib/autopls_1.3.tar.gz
        #   https://cran.r-project.org/src/contrib/matrixpls_1.0.4.tar.gz
        url_regex = "/" + url_regex

        # We need to add a $ anchor to the end of the regex to prevent
        # Spack from picking up signature files like:
        #   .asc
        #   .md5
        #   .sha256
        #   .sig
        # However, SourceForge downloads still need to end in '/download'.
        url_regex += r"(\/download)?"
        # PyPI adds #sha256=... to the end of the URL
        url_regex += "(#sha256=.*)?"
        url_regex += "$"

        regexes.append(url_regex)

    regexes = [re.compile(r) for r in regexes]
    # Build a dict version -> URL from any links that match the wildcards.
    # Walk through archive_url links first.
    # Any conflicting versions will be overwritten by the list_url links.
    versions: Dict[spack.version.StandardVersion, str] = {}
    matched = set()
    for url in sorted(links):
        url = convert_to_posix_path(url)
        if any(r.search(url) for r in regexes):
            try:
                ver = parse_version(url)
                if ver in matched:
                    continue
                versions[ver] = url
                # prevent this version from getting overwritten
                if reference_package is not None:
                    if url == reference_package.url_for_version(ver):
                        matched.add(ver)
                else:
                    extrapolated_urls = [substitute_version(u, ver) for u in archive_urls]
                    if url in extrapolated_urls:
                        matched.add(ver)
            except UndetectableVersionError:
                continue

    for url in archive_urls:
        url = convert_to_posix_path(url)
        ver = parse_version(url)
        if ver not in versions:
            versions[ver] = url

    return versions


class UrlParseError(spack.error.SpackError):
    """Raised when the URL module can't parse something correctly."""

    def __init__(self, msg, path):
        super().__init__(msg)
        self.path = path


class UndetectableVersionError(UrlParseError):
    """Raised when we can't parse a version from a string."""

    def __init__(self, path):
        super().__init__("Couldn't detect version in: " + path, path)


class UndetectableNameError(UrlParseError):
    """Raised when we can't parse a package name from a string."""

    def __init__(self, path):
        super().__init__("Couldn't parse package name in: " + path, path)
