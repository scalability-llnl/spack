# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
import os
import re
from six import StringIO
from six.moves.urllib.parse import urlsplit, urlunsplit

import llnl.util.tty as tty
from llnl.util.tty.color import cescape, colorize

import spack.error
import spack.util.compression as comp
from spack.version import Version


#
# Note: We call the input to most of these functions a "path" but the functions
# work on paths and URLs.  There's not a good word for both of these, but
# "path" seemed like the most generic term.
#
def find_list_urls(url):
    r"""Find good list URLs for the supplied URL.

    By default, returns the dirname of the archive path.

    Provides special treatment for the following websites, which have a
    unique list URL different from the dirname of the download URL:

    =========  =======================================================
    GitHub     https://github.com/<repo>/<name>/releases
    GitLab     https://gitlab.\*/<repo>/<name>/tags
    BitBucket  https://bitbucket.org/<repo>/<name>/downloads/?tab=tags
    CRAN       https://\*.r-project.org/src/contrib/Archive/<name>
    =========  =======================================================

    Parameters:
        url (str): The download URL for the package

    Returns:
        set: One or more list URLs for the package
    """

    url_types = [
        # GitHub
        # e.g. https://github.com/llnl/callpath/archive/v1.0.1.tar.gz
        (r'(.*github\.com/[^/]+/[^/]+)',
         lambda m: m.group(1) + '/releases'),

        # GitLab API endpoint
        # e.g. https://gitlab.dkrz.de/api/v4/projects/k202009%2Flibaec/repository/archive.tar.gz?sha=v1.0.2
        (r'(.*gitlab[^/]+)/api/v4/projects/([^/]+)%2F([^/]+)',
         lambda m: m.group(1) + '/' + m.group(2) + '/' + m.group(3) + '/tags'),

        # GitLab non-API endpoint
        # e.g. https://gitlab.dkrz.de/k202009/libaec/uploads/631e85bcf877c2dcaca9b2e6d6526339/libaec-1.0.0.tar.gz
        (r'(.*gitlab[^/]+/(?!api/v4/projects)[^/]+/[^/]+)',
         lambda m: m.group(1) + '/tags'),

        # BitBucket
        # e.g. https://bitbucket.org/eigen/eigen/get/3.3.3.tar.bz2
        (r'(.*bitbucket.org/[^/]+/[^/]+)',
         lambda m: m.group(1) + '/downloads/?tab=tags'),

        # CRAN
        # e.g. https://cran.r-project.org/src/contrib/Rcpp_0.12.9.tar.gz
        # e.g. https://cloud.r-project.org/src/contrib/rgl_0.98.1.tar.gz
        (r'(.*\.r-project\.org/src/contrib)/([^_]+)',
         lambda m: m.group(1) + '/Archive/' + m.group(2)),
    ]

    list_urls = set([os.path.dirname(url)])

    for pattern, fun in url_types:
        match = re.search(pattern, url)
        if match:
            list_urls.add(fun(match))

    return list_urls


def strip_query_and_fragment(path):
    try:
        components = urlsplit(path)
        stripped = components[:3] + (None, None)

        query, frag = components[3:5]
        suffix = ''
        if query:
            suffix += '?' + query
        if frag:
            suffix += '#' + frag

        return (urlunsplit(stripped), suffix)

    except ValueError:
        tty.debug("Got error parsing path %s" % path)
        return (path, '')  # Ignore URL parse errors here


def strip_version_suffixes(path):
    """Some tarballs contain extraneous information after the version:

    * ``bowtie2-2.2.5-source``
    * ``libevent-2.0.21-stable``
    * ``cuda_8.0.44_linux.run``

    These strings are not part of the version number and should be ignored.
    This function strips those suffixes off and returns the remaining string.
    The goal is that the version is always the last thing in ``path``:

    * ``bowtie2-2.2.5``
    * ``libevent-2.0.21``
    * ``cuda_8.0.44``

    Args:
        path (str): The filename or URL for the package

    Returns:
        str: The ``path`` with any extraneous suffixes removed
    """
    # NOTE: This could be done with complicated regexes in parse_version_offset
    # NOTE: The problem is that we would have to add these regexes to the end
    # NOTE: of every single version regex. Easier to just strip them off
    # NOTE: permanently

    suffix_regexes = [
        # Download type
        r'[Ii]nstall',
        r'all',
        r'code',
        r'[Ss]ources?',
        r'file',
        r'full',
        r'single',
        r'with[a-zA-Z_-]+',
        r'rock',
        r'src(_0)?',
        r'public',
        r'bin',
        r'binary',
        r'run',
        r'[Uu]niversal',
        r'jar',
        r'complete',
        r'dynamic',
        r'oss',
        r'gem',
        r'tar',
        r'sh',

        # Download version
        r'release',
        r'bin',
        r'stable',
        r'[Ff]inal',
        r'rel',
        r'orig',
        r'dist',
        r'\+',

        # License
        r'gpl',

        # Arch
        # Needs to come before and after OS, appears in both orders
        r'ia32',
        r'intel',
        r'amd64',
        r'linux64',
        r'x64',
        r'64bit',
        r'x86[_-]64',
        r'i586_64',
        r'x86',
        r'i[36]86',
        r'ppc64(le)?',
        r'armv?(7l|6l|64)',

        # Other
        r'cpp',
        r'gtk',
        r'incubating',

        # OS
        r'[Ll]inux(_64)?',
        r'LINUX',
        r'[Uu]ni?x',
        r'[Ss]un[Oo][Ss]',
        r'[Mm]ac[Oo][Ss][Xx]?',
        r'[Oo][Ss][Xx]',
        r'[Dd]arwin(64)?',
        r'[Aa]pple',
        r'[Ww]indows',
        r'[Ww]in(64|32)?',
        r'[Cc]ygwin(64|32)?',
        r'[Mm]ingw',
        r'centos',

        # Arch
        # Needs to come before and after OS, appears in both orders
        r'ia32',
        r'intel',
        r'amd64',
        r'linux64',
        r'x64',
        r'64bit',
        r'x86[_-]64',
        r'i586_64',
        r'x86',
        r'i[36]86',
        r'ppc64(le)?',
        r'armv?(7l|6l|64)?',

        # PyPI
        r'[._-]py[23].*\.whl',
        r'[._-]cp[23].*\.whl',
        r'[._-]win.*\.exe',
    ]

    for regex in suffix_regexes:
        # Remove the suffix from the end of the path
        # This may be done multiple times
        path = re.sub(r'[._-]?' + regex + '$', '', path)

    return path


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
        r'[._-][rvV]?' + str(version) + '.*',

        # namever
        r'V?' + str(version) + '.*',

        # Download type
        r'install',
        r'[Ss]rc',
        r'(open)?[Ss]ources?',
        r'[._-]open',
        r'[._-]archive',
        r'[._-]std',
        r'[._-]bin',
        r'Software',

        # Download version
        r'release',
        r'snapshot',
        r'distrib',
        r'everywhere',
        r'latest',

        # Arch
        r'Linux(64)?',
        r'x86_64',

        # VCS
        r'0\+bzr',

        # License
        r'gpl',

        # Needs to come before and after gpl, appears in both orders
        r'[._-]x11',
        r'gpl',
    ]

    for regex in suffix_regexes:
        # Remove the suffix from the end of the path
        # This may be done multiple times
        path = re.sub('[._-]?' + regex + '$', '', path)

    return path


def split_url_extension(path):
    """Some URLs have a query string, e.g.:

    1. https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v2.0.7.tgz?raw=true
    2. http://www.apache.org/dyn/closer.cgi?path=/cassandra/1.2.0/apache-cassandra-1.2.0-rc2-bin.tar.gz
    3. https://gitlab.kitware.com/vtk/vtk/repository/archive.tar.bz2?ref=v7.0.0

    In (1), the query string needs to be stripped to get at the
    extension, but in (2) & (3), the filename is IN a single final query
    argument.

    This strips the URL into three pieces: ``prefix``, ``ext``, and ``suffix``.
    The suffix contains anything that was stripped off the URL to
    get at the file extension.  In (1), it will be ``'?raw=true'``, but
    in (2), it will be empty. In (3) the suffix is a parameter that follows
    after the file extension, e.g.:

    1. ``('https://github.com/losalamos/CLAMR/blob/packages/PowerParser_v2.0.7', '.tgz', '?raw=true')``
    2. ``('http://www.apache.org/dyn/closer.cgi?path=/cassandra/1.2.0/apache-cassandra-1.2.0-rc2-bin', '.tar.gz', None)``
    3. ``('https://gitlab.kitware.com/vtk/vtk/repository/archive', '.tar.bz2', '?ref=v7.0.0')``
    """
    prefix, ext, suffix = path, '', ''

    # Strip off sourceforge download suffix.
    # e.g. https://sourceforge.net/projects/glew/files/glew/2.0.0/glew-2.0.0.tgz/download
    match = re.search(r'(.*(?:sourceforge\.net|sf\.net)/.*)(/download)$', path)
    if match:
        prefix, suffix = match.groups()

    ext = comp.extension(prefix)
    if ext is not None:
        prefix = comp.strip_extension(prefix)

    else:
        prefix, suf = strip_query_and_fragment(prefix)
        ext = comp.extension(prefix)
        prefix = comp.strip_extension(prefix)
        suffix = suf + suffix
        if ext is None:
            ext = ''

    return prefix, ext, suffix


def determine_url_file_extension(path):
    """This returns the type of archive a URL refers to.  This is
       sometimes confusing because of URLs like:

       (1) https://github.com/petdance/ack/tarball/1.93_02

       Where the URL doesn't actually contain the filename.  We need
       to know what type it is so that we can appropriately name files
       in mirrors.
    """
    match = re.search(r'github.com/.+/(zip|tar)ball/', path)
    if match:
        if match.group(1) == 'zip':
            return 'zip'
        elif match.group(1) == 'tar':
            return 'tar.gz'

    prefix, ext, suffix = split_url_extension(path)
    return ext


def parse_version_offset(path):
    """Try to extract a version string from a filename or URL.

    Args:
        path (str): The filename or URL for the package

    Returns:
        tuple of (Version, int, int, int, str): A tuple containing:
            version of the package,
            first index of version,
            length of version string,
            the index of the matching regex
            the matching regex

    Raises:
        UndetectableVersionError: If the URL does not match any regexes
    """
    original_path = path

    # path:   The prefix of the URL, everything before the ext and suffix
    # ext:    The file extension
    # suffix: Any kind of query string that begins with a '?'
    path, ext, suffix = split_url_extension(path)

    # stem:   Everything from path after the final '/'
    original_stem = os.path.basename(path)

    # Try to strip off anything after the version number
    stem = strip_version_suffixes(original_stem)

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
        (r'^[a-zA-Z+._-]+[._-]v?(\d[\d._-]*)$', stem),

        # 2nd Pass: Version only
        # Assume version contains no letters

        # ver
        # e.g. 3.2.7, 7.0.2-7, v3.3.0, v1_6_3
        (r'^v?(\d[\d._-]*)$', stem),

        # 3rd Pass: No separator characters are used
        # Assume name contains no digits

        # namever
        # e.g. turbolinux702, nauty26r7
        (r'^[a-zA-Z+]*(\d[\da-zA-Z]*)$', stem),

        # 4th Pass: A single separator character is used
        # Assume name contains no digits

        # name-name-ver-ver
        # e.g. panda-2016-03-07, gts-snapshot-121130, cdd-061a
        (r'^[a-zA-Z+-]*(\d[\da-zA-Z-]*)$', stem),

        # name_name_ver_ver
        # e.g. tinyxml_2_6_2, boost_1_55_0, tbb2017_20161128
        (r'^[a-zA-Z+_]*(\d[\da-zA-Z_]*)$', stem),

        # name.name.ver.ver
        # e.g. prank.source.150803, jpegsrc.v9b, atlas3.11.34, geant4.10.01.p03
        (r'^[a-zA-Z+.]*(\d[\da-zA-Z.]*)$', stem),

        # 5th Pass: Two separator characters are used
        # Name may contain digits, version may contain letters

        # name-name-ver.ver
        # e.g. m4-1.4.17, gmp-6.0.0a, launchmon-v1.0.2
        (r'^[a-zA-Z\d+-]+-v?(\d[\da-zA-Z.]*)$', stem),

        # name-name-ver_ver
        # e.g. icu4c-57_1
        (r'^[a-zA-Z\d+-]+-v?(\d[\da-zA-Z_]*)$', stem),

        # name_name_ver.ver
        # e.g. superlu_dist_4.1, pexsi_v0.9.0
        (r'^[a-zA-Z\d+_]+_v?(\d[\da-zA-Z.]*)$', stem),

        # name_name.ver.ver
        # e.g. fer_source.v696
        (r'^[a-zA-Z\d+_]+\.v?(\d[\da-zA-Z.]*)$', stem),

        # name_ver-ver
        # e.g. Bridger_r2014-12-01
        (r'^[a-zA-Z\d+]+_r?(\d[\da-zA-Z-]*)$', stem),

        # name-name-ver.ver-ver.ver
        # e.g. sowing-1.1.23-p1, bib2xhtml-v3.0-15-gf506, 4.6.3-alpha04
        (r'^(?:[a-zA-Z\d+-]+-)?v?(\d[\da-zA-Z.-]*)$', stem),

        # namever.ver-ver.ver
        # e.g. go1.4-bootstrap-20161024
        (r'^[a-zA-Z+]+v?(\d[\da-zA-Z.-]*)$', stem),

        # 6th Pass: All three separator characters are used
        # Name may contain digits, version may contain letters

        # name_name-ver.ver
        # e.g. the_silver_searcher-0.32.0, sphinx_rtd_theme-0.1.10a0
        (r'^[a-zA-Z\d+_]+-v?(\d[\da-zA-Z.]*)$', stem),

        # name.name_ver.ver-ver.ver
        # e.g. TH.data_1.0-8, XML_3.98-1.4
        (r'^[a-zA-Z\d+.]+_v?(\d[\da-zA-Z.-]*)$', stem),

        # name-name-ver.ver_ver.ver
        # e.g. pypar-2.1.5_108
        (r'^[a-zA-Z\d+-]+-v?(\d[\da-zA-Z._]*)$', stem),

        # name.name_name-ver.ver
        # e.g. tap.py-1.6, backports.ssl_match_hostname-3.5.0.1
        (r'^[a-zA-Z\d+._]+-v?(\d[\da-zA-Z.]*)$', stem),

        # name-namever.ver_ver.ver
        # e.g. STAR-CCM+11.06.010_02
        (r'^[a-zA-Z+-]+(\d[\da-zA-Z._]*)$', stem),

        # name-name_name-ver.ver
        # e.g. PerlIO-utf8_strict-0.002
        (r'^[a-zA-Z\d+_-]+-v?(\d[\da-zA-Z.]*)$', stem),

        # 7th Pass: Specific VCS

        # bazaar
        # e.g. libvterm-0+bzr681
        (r'bzr(\d[\da-zA-Z._-]*)$', stem),

        # 8th Pass: Query strings

        # e.g. https://gitlab.cosma.dur.ac.uk/api/v4/projects/swift%2Fswiftsim/repository/archive.tar.gz?sha=v0.3.0
        # e.g. https://gitlab.kitware.com/api/v4/projects/icet%2Ficet/repository/archive.tar.bz2?sha=IceT-2.1.1
        # e.g. http://gitlab.cosma.dur.ac.uk/swift/swiftsim/repository/archive.tar.gz?ref=v0.3.0
        # e.g. http://apps.fz-juelich.de/jsc/sionlib/download.php?version=1.7.1
        # e.g. https://software.broadinstitute.org/gatk/download/auth?package=GATK-archive&version=3.8-1-0-gf15c1c3ef
        (r'[?&](?:sha|ref|version)=[a-zA-Z\d+-]*[_-]?v?(\d[\da-zA-Z._-]*)$', suffix),  # noqa: E501

        # e.g. http://slepc.upv.es/download/download.php?filename=slepc-3.6.2.tar.gz
        # e.g. http://laws-green.lanl.gov/projects/data/eos/get_file.php?package=eospac&filename=eospac_v6.4.0beta.1_r20171213193219.tgz
        # e.g. https://evtgen.hepforge.org/downloads?f=EvtGen-01.07.00.tar.gz
        # e.g. http://wwwpub.zih.tu-dresden.de/%7Emlieber/dcount/dcount.php?package=otf&get=OTF-1.12.5salmon.tar.gz
        (r'[?&](?:filename|f|get)=[a-zA-Z\d+-]+[_-]v?(\d[\da-zA-Z.]*)', stem),

        # 9th Pass: Version in path

        # github.com/repo/name/releases/download/vver/name
        # e.g. https://github.com/nextflow-io/nextflow/releases/download/v0.20.1/nextflow
        (r'github\.com/[^/]+/[^/]+/releases/download/[a-zA-Z+._-]*v?(\d[\da-zA-Z._-]*)/', path),  # noqa: E501

        # e.g. ftp://ftp.ncbi.nlm.nih.gov/blast/executables/legacy.NOTSUPPORTED/2.2.26/ncbi.tar.gz
        (r'(\d[\da-zA-Z._-]*)/[^/]+$', path),
    ]

    for i, version_regex in enumerate(version_regexes):
        regex, match_string = version_regex
        match = re.search(regex, match_string)
        if match and match.group(1) is not None:
            version = match.group(1)
            start   = match.start(1)

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


def parse_version(path):
    """Try to extract a version string from a filename or URL.

    Args:
        path (str): The filename or URL for the package

    Returns:
        spack.version.Version: The version of the package

    Raises:
        UndetectableVersionError: If the URL does not match any regexes
    """
    version, start, length, i, regex = parse_version_offset(path)
    return Version(version)


def parse_name_offset(path, v=None):
    """Try to determine the name of a package from its filename or URL.

    Args:
        path (str): The filename or URL for the package
        v (str): The version of the package

    Returns:
        tuple of (str, int, int, int, str): A tuple containing:
            name of the package,
            first index of name,
            length of name,
            the index of the matching regex
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
            v = 'unknown'

    # path:   The prefix of the URL, everything before the ext and suffix
    # ext:    The file extension
    # suffix: Any kind of query string that begins with a '?'
    path, ext, suffix = split_url_extension(path)

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
        (r'github\.com/[^/]+/([^/]+)', path),

        # GitLab API endpoint: gitlab.*/api/v4/projects/NAMESPACE%2Fname/
        # e.g. https://gitlab.cosma.dur.ac.uk/api/v4/projects/swift%2Fswiftsim/repository/archive.tar.gz?sha=v0.3.0
        (r'gitlab[^/]+/api/v4/projects/[^/]+%2F([^/]+)', path),

        # GitLab non-API endpoint: gitlab.*/repo/name/
        # e.g. http://gitlab.cosma.dur.ac.uk/swift/swiftsim/repository/archive.tar.gz?ref=v0.3.0
        (r'gitlab[^/]+/(?!api/v4/projects)[^/]+/([^/]+)', path),

        # Bitbucket: bitbucket.org/repo/name/
        # e.g. https://bitbucket.org/glotzer/hoomd-blue/get/v1.3.3.tar.bz2
        (r'bitbucket\.org/[^/]+/([^/]+)', path),

        # PyPI: pypi.(python.org|io)/packages/source/first-letter/name/
        # e.g. https://pypi.python.org/packages/source/m/mpmath/mpmath-all-0.19.tar.gz
        # e.g. https://pypi.io/packages/source/b/backports.ssl_match_hostname/backports.ssl_match_hostname-3.5.0.1.tar.gz
        (r'pypi\.(?:python\.org|io)/packages/source/[A-Za-z\d]/([^/]+)', path),

        # Crates.IO: crates.io/crates/name
        # e.g. https://crates.io/crates/ripgrep
        (r'crates\.io/crates/([^/]+)', path),

        # lib.rs: lib.rs/crates/name
        # e.g. https://lib.rs/crates/ripgrep
        (r'lib\.rs/crates/([^/]+)', path),

        # 2nd Pass: Query strings

        # ?filename=name-ver.ver
        # e.g. http://slepc.upv.es/download/download.php?filename=slepc-3.6.2.tar.gz
        (r'\?filename=([A-Za-z\d+-]+)$', stem),

        # ?f=name-ver.ver
        # e.g. https://evtgen.hepforge.org/downloads?f=EvtGen-01.07.00.tar.gz
        (r'\?f=([A-Za-z\d+-]+)$', stem),

        # ?package=name
        # e.g. http://wwwpub.zih.tu-dresden.de/%7Emlieber/dcount/dcount.php?package=otf&get=OTF-1.12.5salmon.tar.gz
        (r'\?package=([A-Za-z\d+-]+)', stem),

        # ?package=name-version
        (r'\?package=([A-Za-z\d]+)', suffix),

        # download.php
        # e.g. http://apps.fz-juelich.de/jsc/sionlib/download.php?version=1.7.1
        (r'([^/]+)/download.php$', path),

        # 3rd Pass: Name followed by version in archive

        (r'^([A-Za-z\d+\._-]+)$', stem),
    ]

    for i, name_regex in enumerate(name_regexes):
        regex, match_string = name_regex
        match = re.search(regex, match_string)
        if match:
            name  = match.group(1)
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
        tuple of (str, Version)A tuple containing:
            The name of the package
            The version of the package

    Raises:
        UndetectableVersionError: If the URL does not match any regexes
        UndetectableNameError: If the URL does not match any regexes
    """
    ver = parse_version(path)
    name = parse_name(path, ver)
    return (name, ver)


def insensitize(string):
    """Change upper and lowercase letters to be case insensitive in
       the provided string.  e.g., 'a' becomes '[Aa]', 'B' becomes
       '[bB]', etc.  Use for building regexes."""
    def to_ins(match):
        char = match.group(1)
        return '[%s%s]' % (char.lower(), char.upper())
    return re.sub(r'([a-zA-Z])', to_ins, string)


def cumsum(elts, init=0, fn=lambda x: x):
    """Return cumulative sum of result of fn on each element in elts."""
    sums = []
    s = init
    for i, e in enumerate(elts):
        sums.append(s)
        s += fn(e)
    return sums


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
        ver,  vs, vl, vi, vregex = parse_version_offset(path)
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
    ver_offsets  = find_all(ver,  path)

    return (name, ns, nl, name_offsets,
            ver,  vs, vl, ver_offsets)


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
    result = r'(\d.*)'.join(re.escape(vp) for vp in vparts)

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
    (name, ns, nl, noffs,
     ver,  vs, vl, voffs) = substitution_offsets(path)

    new_path = ''
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

    errors = kwargs.get('errors', False)
    subs   = kwargs.get('subs', False)

    (name, ns, nl, noffs,
     ver,  vs, vl, voffs) = substitution_offsets(path)

    nends = [no + nl - 1 for no in noffs]
    vends = [vo + vl - 1 for vo in voffs]

    nerr = verr = 0
    out = StringIO()
    for i in range(len(path)):
        if i == vs:
            out.write('@c')
            verr += 1
        elif i == ns:
            out.write('@r')
            nerr += 1
        elif subs:
            if i in voffs:
                out.write('@g')
            elif i in noffs:
                out.write('@m')

        out.write(path[i])

        if i == vs + vl - 1:
            out.write('@.')
            verr += 1
        elif i == ns + nl - 1:
            out.write('@.')
            nerr += 1
        elif subs:
            if i in vends or i in nends:
                out.write('@.')

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


class UrlParseError(spack.error.SpackError):
    """Raised when the URL module can't parse something correctly."""

    def __init__(self, msg, path):
        super(UrlParseError, self).__init__(msg)
        self.path = path


class UndetectableVersionError(UrlParseError):
    """Raised when we can't parse a version from a string."""

    def __init__(self, path):
        super(UndetectableVersionError, self).__init__(
            "Couldn't detect version in: " + path, path)


class UndetectableNameError(UrlParseError):
    """Raised when we can't parse a package name from a string."""

    def __init__(self, path):
        super(UndetectableNameError, self).__init__(
            "Couldn't parse package name in: " + path, path)
