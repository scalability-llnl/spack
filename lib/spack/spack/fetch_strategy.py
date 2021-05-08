# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
Fetch strategies are used to download source code into a staging area
in order to build it.  They need to define the following methods:

    * fetch()
        This should attempt to download/check out source from somewhere.
    * check()
        Apply a checksum to the downloaded source code, e.g. for an archive.
        May not do anything if the fetch method was safe to begin with.
    * expand()
        Expand (e.g., an archive) downloaded file to source, with the
        standard stage source path as the destination directory.
    * reset()
        Restore original state of downloaded code.  Used by clean commands.
        This may just remove the expanded source and re-expand an archive,
        or it may run something like git reset --hard.
    * archive()
        Archive a source directory, e.g. for creating a mirror.
"""
import copy
import functools
import os
import os.path
import re
import shutil
import sys
import uuid
from textwrap import dedent
from typing import ClassVar, Iterator, List, Optional, Tuple  # novm

import six
import six.moves.urllib.parse as urllib_parse

import llnl.util.tty as tty
from llnl.util.filesystem import (
    working_dir, mkdirp, temp_rename, temp_cwd, get_single_file)
from llnl.util.lang import memoized

import spack.config
import spack.error
import spack.util.crypto as crypto
import spack.util.pattern as pattern
import spack.util.url as url_util
import spack.util.web as web_util
from spack.util.compression import decompressor_for, extension
from spack.util.executable import which, CommandNotFoundError, Executable, ProcessError
from spack.util.string import comma_and, quote
from spack.version import Version

#: List of all fetch strategies, created by FetchStrategy metaclass.
all_strategies = []

CONTENT_TYPE_MISMATCH_WARNING_TEMPLATE = (
    "The contents of {subject} look like {content_type}.  Either the URL"
    " you are trying to use does not exist or you have an internet gateway"
    " issue.  You can remove the bad archive using 'spack clean"
    " <package>', then try again using the correct URL.")


def warn_content_type_mismatch(subject, content_type='HTML'):
    tty.warn(CONTENT_TYPE_MISMATCH_WARNING_TEMPLATE.format(
        subject=subject, content_type=content_type))


def _needs_stage(fun):
    """Many methods on fetch strategies require a stage to be set
       using set_stage().  This decorator adds a check for self.stage."""

    @functools.wraps(fun)
    def wrapper(self, *args, **kwargs):
        if not self.stage:
            raise NoStageError(fun)
        return fun(self, *args, **kwargs)

    return wrapper


def _ensure_one_stage_entry(stage_path):
    """Ensure there is only one stage entry in the stage path."""
    stage_entries = os.listdir(stage_path)
    assert len(stage_entries) == 1
    return os.path.join(stage_path, stage_entries[0])


def fetcher(cls):
    """Decorator used to register fetch strategies."""
    all_strategies.append(cls)
    return cls


class FetchStrategy(object):
    """Superclass of all fetch strategies."""
    #: The URL attribute must be specified either at the package class
    #: level, or as a keyword argument to ``version()``.  It is used to
    #: distinguish fetchers for different versions in the package DSL.
    url_attr = None  # type: Optional[str]

    #: Optional attributes can be used to distinguish fetchers when :
    #: classes have multiple ``url_attrs`` at the top-level.
    # optional attributes in version() args.
    optional_attrs = []  # type: List[str]

    def __init__(self, **kwargs):
        # The stage is initialized late, so that fetch strategies can be
        # constructed at package construction time.  This is where things
        # will be fetched.
        self.stage = None
        # Enable or disable caching for this strategy based on
        # 'no_cache' option from version directive.
        self.cache_enabled = not kwargs.pop('no_cache', False)

    # Subclasses need to implement these methods
    def fetch(self):
        """Fetch source code archive or repo.

        Returns:
            bool: True on success, False on failure.
        """

    def check(self):
        """Checksum the archive fetched by this FetchStrategy."""

    def expand(self):
        """Expand the downloaded archive into the stage source path."""

    def reset(self):
        """Revert to freshly downloaded state.

        For archive files, this may just re-expand the archive.
        """

    def archive(self, destination):
        """Create an archive of the downloaded data for a mirror.

        For downloaded files, this should preserve the checksum of the
        original file. For repositories, it should just create an
        expandable tarball out of the downloaded repository.
        """

    @property
    def cachable(self):
        """Whether fetcher is capable of caching the resource it retrieves.

        This generally is determined by whether the resource is
        identifiably associated with a specific package version.

        Returns:
            bool: True if can cache, False otherwise.
        """

    def source_id(self):
        """A unique ID for the source.

        It is intended that a human could easily generate this themselves using
        the information available to them in the Spack package.

        The returned value is added to the content which determines the full
        hash for a package using `str()`.
        """
        raise NotImplementedError

    def mirror_id(self):
        """This is a unique ID for a source that is intended to help identify
        reuse of resources across packages.

        It is unique like source-id, but it does not include the package name
        and is not necessarily easy for a human to create themselves.
        """
        raise NotImplementedError

    def __str__(self):  # Should be human readable URL.
        return "FetchStrategy.__str___"

    @classmethod
    def matches(cls, args):
        """Predicate that matches fetch strategies to arguments of
        the version directive.

        Args:
            args: arguments of the version directive
        """
        return cls.url_attr in args


@fetcher
class BundleFetchStrategy(FetchStrategy):
    """
    Fetch strategy associated with bundle, or no-code, packages.

    Having a basic fetch strategy is a requirement for executing post-install
    hooks.  Consequently, this class provides the API but does little more
    than log messages.

    TODO: Remove this class by refactoring resource handling and the link
    between composite stages and composite fetch strategies (see #11981).
    """
    #: There is no associated URL keyword in ``version()`` for no-code
    #: packages but this property is required for some strategy-related
    #: functions (e.g., check_pkg_attributes).
    url_attr = ''

    def fetch(self):
        """Simply report success -- there is no code to fetch."""
        return True

    @property
    def cachable(self):
        """Report False as there is no code to cache."""
        return False

    def source_id(self):
        """BundlePackages don't have a source id."""
        return ''

    def mirror_id(self):
        """BundlePackages don't have a mirror id."""


class FetchStrategyComposite(pattern.Composite):
    """Composite for a FetchStrategy object.
    """
    matches = FetchStrategy.matches

    def __init__(self):
        super(FetchStrategyComposite, self).__init__([
            'fetch', 'check', 'expand', 'reset', 'archive', 'cachable',
            'mirror_id'
        ])

    def source_id(self):
        component_ids = tuple(i.source_id() for i in self)
        if all(component_ids):
            return component_ids


@fetcher
class URLFetchStrategy(FetchStrategy):
    """URLFetchStrategy pulls source code from a URL for an archive, check the
    archive against a checksum, and decompresses the archive.

    The destination for the resulting file(s) is the standard stage path.
    """
    url_attr = 'url'

    # these are checksum types. The generic 'checksum' is deprecated for
    # specific hash names, but we need it for backward compatibility
    optional_attrs = list(crypto.hashes.keys()) + ['checksum']

    def __init__(self, url=None, checksum=None, **kwargs):
        super(URLFetchStrategy, self).__init__(**kwargs)

        # Prefer values in kwargs to the positionals.
        self.url = kwargs.get('url', url)
        self.mirrors = kwargs.get('mirrors', [])

        # digest can be set as the first argument, or from an explicit
        # kwarg by the hash name.
        self.digest = kwargs.get('checksum', checksum)
        for h in self.optional_attrs:
            if h in kwargs:
                self.digest = kwargs[h]

        self.expand_archive = kwargs.get('expand', True)
        self.extra_options = kwargs.get('fetch_options', {})
        self._curl = None

        self.extension = kwargs.get('extension', None)

        if not self.url:
            raise ValueError("URLFetchStrategy requires a url for fetching.")

    @property
    def curl(self):
        if not self._curl:
            try:
                self._curl = which('curl', required=True)
            except CommandNotFoundError as exc:
                tty.error(str(exc))
        return self._curl

    def source_id(self):
        return self.digest

    def mirror_id(self):
        if not self.digest:
            return None
        # The filename is the digest. A directory is also created based on
        # truncating the digest to avoid creating a directory with too many
        # entries
        return os.path.sep.join(
            ['archive', self.digest[:2], self.digest])

    @property
    def candidate_urls(self):
        return [self.url] + (self.mirrors or [])

    @_needs_stage
    def fetch(self):
        if self.archive_file:
            tty.debug('Already downloaded {0}'.format(self.archive_file))
            return

        url = None
        errors = []
        for url in self.candidate_urls:
            if not self._existing_url(url):
                continue

            try:
                partial_file, save_file = self._fetch_from_url(url)
                if save_file:
                    os.rename(partial_file, save_file)
                break
            except FetchError as e:
                errors.append(str(e))

        for msg in errors:
            tty.debug(msg)

        if not self.archive_file:
            raise FailedDownloadError(url)

    def _existing_url(self, url):
        tty.debug('Checking existence of {0}'.format(url))
        curl = self.curl
        # Telling curl to fetch the first byte (-r 0-0) is supposed to be
        # portable.
        curl_args = ['--stderr', '-', '-s', '-f', '-r', '0-0', url]
        if not spack.config.get('config:verify_ssl'):
            curl_args.append('-k')
        _ = curl(*curl_args, fail_on_error=False, output=os.devnull)
        return curl.returncode == 0

    def _fetch_from_url(self, url):
        save_file = None
        partial_file = None
        if self.stage.save_filename:
            save_file = self.stage.save_filename
            partial_file = self.stage.save_filename + '.part'
        tty.msg('Fetching {0}'.format(url))
        if partial_file:
            save_args = ['-C',
                         '-',  # continue partial downloads
                         '-o',
                         partial_file]  # use a .part file
        else:
            save_args = ['-O']

        curl_args = save_args + [
            '-f',  # fail on >400 errors
            '-D',
            '-',  # print out HTML headers
            '-L',  # resolve 3xx redirects
            url,
        ]

        if not spack.config.get('config:verify_ssl'):
            curl_args.append('-k')

        if sys.stdout.isatty() and tty.msg_enabled():
            curl_args.append('-#')  # status bar when using a tty
        else:
            curl_args.append('-sS')  # show errors if fail

        connect_timeout = spack.config.get('config:connect_timeout', 10)

        if self.extra_options:
            cookie = self.extra_options.get('cookie')
            if cookie:
                curl_args.append('-j')  # junk cookies
                curl_args.append('-b')  # specify cookie
                curl_args.append(cookie)

            timeout = self.extra_options.get('timeout')
            if timeout:
                connect_timeout = max(connect_timeout, int(timeout))

        if connect_timeout > 0:
            # Timeout if can't establish a connection after n sec.
            curl_args.extend(['--connect-timeout', str(connect_timeout)])

        # Run curl but grab the mime type from the http headers
        curl = self.curl
        with working_dir(self.stage.path):
            headers = curl(*curl_args, output=str, fail_on_error=False)

        if curl.returncode != 0:
            # clean up archive on failure.
            if self.archive_file:
                os.remove(self.archive_file)

            if partial_file and os.path.exists(partial_file):
                os.remove(partial_file)

            if curl.returncode == 22:
                # This is a 404.  Curl will print the error.
                raise FailedDownloadError(
                    url, "URL %s was not found!" % url)

            elif curl.returncode == 60:
                # This is a certificate error.  Suggest spack -k
                raise FailedDownloadError(
                    url,
                    "Curl was unable to fetch due to invalid certificate. "
                    "This is either an attack, or your cluster's SSL "
                    "configuration is bad.  If you believe your SSL "
                    "configuration is bad, you can try running spack -k, "
                    "which will not check SSL certificates."
                    "Use this at your own risk.")

            else:
                # This is some other curl error.  Curl will print the
                # error, but print a spack message too
                raise FailedDownloadError(
                    url,
                    "Curl failed with error %d" % curl.returncode)

        # Check if we somehow got an HTML file rather than the archive we
        # asked for.  We only look at the last content type, to handle
        # redirects properly.
        content_types = re.findall(r'Content-Type:[^\r\n]+', headers,
                                   flags=re.IGNORECASE)
        if content_types and 'text/html' in content_types[-1]:
            warn_content_type_mismatch(self.archive_file or "the archive")
        return partial_file, save_file

    @property  # type: ignore # decorated properties unsupported in mypy
    @_needs_stage
    def archive_file(self):
        """Path to the source archive within this stage directory."""
        return self.stage.archive_file

    @property
    def cachable(self):
        return self.cache_enabled and bool(self.digest)

    @_needs_stage
    def expand(self):
        if not self.expand_archive:
            tty.debug('Staging unexpanded archive {0} in {1}'
                      .format(self.archive_file, self.stage.source_path))
            if not self.stage.expanded:
                mkdirp(self.stage.source_path)
            dest = os.path.join(self.stage.source_path,
                                os.path.basename(self.archive_file))
            shutil.move(self.archive_file, dest)
            return

        tty.debug('Staging archive: {0}'.format(self.archive_file))

        if not self.archive_file:
            raise NoArchiveFileError(
                "Couldn't find archive file",
                "Failed on expand() for URL %s" % self.url)

        if not self.extension:
            self.extension = extension(self.archive_file)

        if self.stage.expanded:
            tty.debug('Source already staged to %s' % self.stage.source_path)
            return

        decompress = decompressor_for(self.archive_file, self.extension)

        # Expand all tarballs in their own directory to contain
        # exploding tarballs.
        tarball_container = os.path.join(self.stage.path,
                                         "spack-expanded-archive")

        # Below we assume that the command to decompress expand the
        # archive in the current working directory
        mkdirp(tarball_container)
        with working_dir(tarball_container):
            decompress(self.archive_file)

        # Check for an exploding tarball, i.e. one that doesn't expand to
        # a single directory.  If the tarball *didn't* explode, move its
        # contents to the staging source directory & remove the container
        # directory.  If the tarball did explode, just rename the tarball
        # directory to the staging source directory.
        #
        # NOTE: The tar program on Mac OS X will encode HFS metadata in
        # hidden files, which can end up *alongside* a single top-level
        # directory.  We initially ignore presence of hidden files to
        # accomodate these "semi-exploding" tarballs but ensure the files
        # are copied to the source directory.
        files = os.listdir(tarball_container)
        non_hidden = [f for f in files if not f.startswith('.')]
        if len(non_hidden) == 1:
            src = os.path.join(tarball_container, non_hidden[0])
            if os.path.isdir(src):
                self.stage.srcdir = non_hidden[0]
                shutil.move(src, self.stage.source_path)
                if len(files) > 1:
                    files.remove(non_hidden[0])
                    for f in files:
                        src = os.path.join(tarball_container, f)
                        dest = os.path.join(self.stage.path, f)
                        shutil.move(src, dest)
                os.rmdir(tarball_container)
            else:
                # This is a non-directory entry (e.g., a patch file) so simply
                # rename the tarball container to be the source path.
                shutil.move(tarball_container, self.stage.source_path)

        else:
            shutil.move(tarball_container, self.stage.source_path)

    def archive(self, destination):
        """Just moves this archive to the destination."""
        if not self.archive_file:
            raise NoArchiveFileError("Cannot call archive() before fetching.")

        web_util.push_to_url(
            self.archive_file,
            destination,
            keep_original=True)

    @_needs_stage
    def check(self):
        """Check the downloaded archive against a checksum digest.
           No-op if this stage checks code out of a repository."""
        if not self.digest:
            raise NoDigestError(
                "Attempt to check URLFetchStrategy with no digest.")

        checker = crypto.Checker(self.digest)
        if not checker.check(self.archive_file):
            raise ChecksumError(
                "%s checksum failed for %s" %
                (checker.hash_name, self.archive_file),
                "Expected %s but got %s" % (self.digest, checker.sum))

    @_needs_stage
    def reset(self):
        """
        Removes the source path if it exists, then re-expands the archive.
        """
        if not self.archive_file:
            raise NoArchiveFileError(
                "Tried to reset URLFetchStrategy before fetching",
                "Failed on reset() for URL %s" % self.url)

        # Remove everything but the archive from the stage
        for filename in os.listdir(self.stage.path):
            abspath = os.path.join(self.stage.path, filename)
            if abspath != self.archive_file:
                shutil.rmtree(abspath, ignore_errors=True)

        # Expand the archive again
        self.expand()

    def __repr__(self):
        url = self.url if self.url else "no url"
        return "%s<%s>" % (self.__class__.__name__, url)

    def __str__(self):
        if self.url:
            return self.url
        else:
            return "[no url]"


@fetcher
class CacheURLFetchStrategy(URLFetchStrategy):
    """The resource associated with a cache URL may be out of date."""

    @_needs_stage
    def fetch(self):
        path = re.sub('^file://', '', self.url)

        # check whether the cache file exists.
        if not os.path.isfile(path):
            raise NoCacheError('No cache of %s' % path)

        # remove old symlink if one is there.
        filename = self.stage.save_filename
        if os.path.exists(filename):
            os.remove(filename)

        # Symlink to local cached archive.
        os.symlink(path, filename)

        # Remove link if checksum fails, or subsequent fetchers
        # will assume they don't need to download.
        if self.digest:
            try:
                self.check()
            except ChecksumError:
                os.remove(self.archive_file)
                raise

        # Notify the user how we fetched.
        tty.msg('Using cached archive: {0}'.format(path))


class VCSFetchStrategy(FetchStrategy):
    """Superclass for version control system fetch strategies.

    Like all fetchers, VCS fetchers are identified by the attributes
    passed to the ``version`` directive.  The optional_attrs for a VCS
    fetch strategy represent types of revisions, e.g. tags, branches,
    commits, etc.

    The required attributes (git, svn, etc.) are used to specify the URL
    and to distinguish a VCS fetch strategy from a URL fetch strategy.

    """

    def __init__(self, **kwargs):
        super(VCSFetchStrategy, self).__init__(**kwargs)

        # Set a URL based on the type of fetch strategy.
        self.url = kwargs.get(self.url_attr, None)
        if not self.url:
            raise ValueError(
                "%s requires %s argument." % (self.__class__, self.url_attr))

        for attr in self.optional_attrs:
            setattr(self, attr, kwargs.get(attr, None))

    @_needs_stage
    def check(self):
        tty.debug('No checksum needed when fetching with {0}'
                  .format(self.url_attr))

    @_needs_stage
    def expand(self):
        tty.debug(
            "Source fetched with %s is already expanded." % self.url_attr)

    @_needs_stage
    def archive(self, destination, **kwargs):
        assert (extension(destination) == 'tar.gz')
        assert (self.stage.source_path.startswith(self.stage.path))

        tar = which('tar', required=True)

        patterns = kwargs.get('exclude', None)
        if patterns is not None:
            if isinstance(patterns, six.string_types):
                patterns = [patterns]
            for p in patterns:
                tar.add_default_arg('--exclude=%s' % p)

        with working_dir(self.stage.path):
            if self.stage.srcdir:
                # Here we create an archive with the default repository name.
                # The 'tar' command has options for changing the name of a
                # directory that is included in the archive, but they differ
                # based on OS, so we temporarily rename the repo
                with temp_rename(self.stage.source_path, self.stage.srcdir):
                    tar('-czf', destination, self.stage.srcdir)
            else:
                tar('-czf', destination,
                    os.path.basename(self.stage.source_path))

    def __str__(self):
        return "VCS: %s" % self.url

    def __repr__(self):
        return "%s<%s>" % (self.__class__, self.url)


@fetcher
class GoFetchStrategy(VCSFetchStrategy):
    """Fetch strategy that employs the `go get` infrastructure.

    Use like this in a package:

       version('name',
               go='github.com/monochromegane/the_platinum_searcher/...')

    Go get does not natively support versions, they can be faked with git.

    The fetched source will be moved to the standard stage sourcepath directory
    during the expand step.
    """
    url_attr = 'go'

    def __init__(self, **kwargs):
        # Discards the keywords in kwargs that may conflict with the next
        # call to __init__
        forwarded_args = copy.copy(kwargs)
        forwarded_args.pop('name', None)
        super(GoFetchStrategy, self).__init__(**forwarded_args)

        self._go = None

    @property
    def go_version(self):
        vstring = self.go('version', output=str).split(' ')[2]
        return Version(vstring)

    @property
    def go(self):
        if not self._go:
            self._go = which('go', required=True)
        return self._go

    @_needs_stage
    def fetch(self):
        tty.debug('Getting go resource: {0}'.format(self.url))

        with working_dir(self.stage.path):
            try:
                os.mkdir('go')
            except OSError:
                pass
            env = dict(os.environ)
            env['GOPATH'] = os.path.join(os.getcwd(), 'go')
            self.go('get', '-v', '-d', self.url, env=env)

    def archive(self, destination):
        super(GoFetchStrategy, self).archive(destination, exclude='.git')

    @_needs_stage
    def expand(self):
        tty.debug(
            "Source fetched with %s is already expanded." % self.url_attr)

        # Move the directory to the well-known stage source path
        repo_root = _ensure_one_stage_entry(self.stage.path)
        shutil.move(repo_root, self.stage.source_path)

    @_needs_stage
    def reset(self):
        with working_dir(self.stage.source_path):
            self.go('clean')

    def __str__(self):
        return "[go] %s" % self.url


class GitRef(object):
    """A wrapper that knows how to format git refspecs in multiple contexts."""
    _known_types = ['branch', 'commit', 'tag']  # type: ClassVar[List[str]]
    _ref_type = None                            # type: str
    _ref = None                                 # type: str

    def __init__(self, ref_type, ref):
        # type: (str, str) -> None
        if ref_type not in self._known_types:
            # This is made a TypeError and not an InvalidGitRef because it cannot arise
            # from invalid user input.
            raise TypeError('GitRef can only have the types {0}, but was given {1}'
                            .format(self._known_types, ref_type))
        self._ref_type = ref_type
        if not isinstance(ref, six.string_types):
            # This case can arise from user error when editing package.py files, so we
            # want to catch this and handle it specially to provide more context.
            raise InvalidGitRef('git reference was not a string: {0}'.format(ref))
        self._ref = ref

    def __repr__(self):
        return '{0}(ref_type={1!r}, ref={2!r})'.format(type(self).__name__,
                                                       self._ref_type, self._ref)

    def __str__(self):
        return '<{0}>'.format(self.repo_info_for_reference())

    # Matches any 10-40 character hexadecimal string.
    _commit_rx = re.compile(r'^[0-9a-f]{10,40}$', flags=re.IGNORECASE)

    @classmethod
    def commit(cls, ref):
        # type: (str) -> GitRef
        if not isinstance(ref, six.string_types):
            # The exception message from `re.match()` does not print the value when
            # a non-string argument is provided, so we special-case that check here.
            raise InvalidGitRef('git reference was not a string: {0}'.format(ref))
        if not cls._commit_rx.match(ref):
            raise InvalidGitRef(dedent("""\
            Spack requires that references to individual git commits be specified via
            a 10-40 character hexadecimal string, but received the string '{0}' instead.

            A valid commit hash case-insensitively matches the regular expression '{1}'.
            10 hex characters is the size printed out by `git log --format='%h'`, while
            40 hex characters is the size printed out by `git log --format='%H'`.
            """.format(ref, cls._commit_rx.pattern)))
        return cls('commit', ref)

    @classmethod
    def tag(cls, ref):
        # type: (str) -> GitRef
        return cls('tag', ref)

    @classmethod
    def branch(cls, ref):
        # type: (str) -> GitRef
        return cls('branch', ref)

    @classmethod
    def from_directive(cls, commit, tag, branch, version_name):
        # type: (Optional[str], Optional[str], Optional[str], Optional[str]) -> GitRef
        num_specified = len(list(filter(None, [commit, tag, branch])))
        # If no explicit git ref arguments are provided, assume that the version string
        # is to be used as the branch.
        if (num_specified == 0) and version_name is not None:
            return cls.branch(version_name)
        # Otherwise, error if we have ambiguous ref arguments, or no ref arguments
        # at all.
        if num_specified != 1:
            raise InvalidGitRef(dedent("""\
            Exactly one of commit, tag, or branch must be specified for a git url.
            Given:
            commit={0}
            tag={1}
            branch={2}
            """).format(commit, tag, branch))
        if commit is not None:
            return cls.commit(commit)
        if tag is not None:
            return cls.tag(tag)
        assert branch is not None, (commit, tag, branch, version_name)
        return cls.branch(branch)

    def refspec(self):
        # type: () -> str
        """Return a string which unambiguously identifies this ref to git."""
        if self._ref_type == 'commit':
            return self._ref
        if self._ref_type == 'tag':
            return 'refs/tags/{0}'.format(self._ref)
        assert self._ref_type == 'branch', self
        return 'refs/heads/{0}'.format(self._ref)

    def fetch_spec(self):
        # type: () -> str
        """Return an argument to update a local ref from the remote, if applicable."""
        if self._ref_type == 'commit':
            # Commits cannot be updated and do not require any special syntax to fetch.
            return self.refspec()
        # Otherwise, we use the syntax to update the local ref from a remote ref of
        # the same name, fetching updates if available/applicable.
        assert self._ref_type in ['tag', 'branch'], self
        maybe_mutating_prefix = '+' if self.is_mutable() else ''
        return '{0}{1}:{1}'.format(maybe_mutating_prefix, self.refspec())

    def is_mutable(self):
        # type: () -> bool
        """Whether this type of git ref should check for updates to that ref."""
        if self._ref_type == 'branch':
            return True
        assert self._ref_type in ['tag', 'commit'], self
        return False

    def repo_info_for_reference(self):
        # type: () -> str
        if self._ref_type == 'commit':
            return 'at commit {0}'.format(self._ref)
        if self._ref_type == 'tag':
            return 'at tag {0}'.format(self._ref)
        assert self._ref_type == 'branch', self
        return 'on branch {0}'.format(self._ref)


class ConfiguredGit(object):
    """Caches the version for the `git` executable, and adds compatibility args.

    Use the `.from_executable()` method to perform this checking:

        from spack.fetch_strategy import ConfiguredGit
        from spack.util.Executable import which

        git = ConfiguredGit.from_executable(which('git', required=True))
        assert git.version == '2.31.1'

    And note that the `__call__` method delegates to the inner executable from `which`:

        assert git('--version', output=str) == 'git version 2.31.1'
    """
    git = None                 # type: Executable
    version = None             # type: Version

    def __init__(self, git, version):
        # type: (Executable, Version) -> None
        self.git = git
        self.version = version

    def __repr__(self):
        return '{0}(git={1!r}, version={2!r})'.format(
            type(self).__name__, self.git, self.version)

    def __call__(self, *args, **kwargs):
        return self.git(*args, **kwargs)

    @staticmethod
    def _get_git_version(git):
        # type: (Executable) -> Version
        vstring = git('--version', output=str).lstrip('git version ')
        return Version(vstring)

    @classmethod
    @memoized
    def from_executable(cls, git):
        # type: (Executable) -> ConfiguredGit
        """Extract the version from a git executable and add defaults for compatibility.

        This method being `@memoized` means that with the current implementation of
        `Executable.__eq__`, any two `Executable` instances pointing to the same
        executable file path will return a cached result from this method.
        """
        version = cls._get_git_version(git)

        # Disable advice for a quieter fetch
        # https://github.com/git/git/blob/master/Documentation/RelNotes/1.7.2.txt
        if version >= Version('1.7.2'):
            git.add_default_arg('-c')
            git.add_default_arg('advice.detachedHead=false')

        # If the user asked for insecure fetching, make that work
        # with git as well.
        if not spack.config.get('config:verify_ssl'):
            git.add_default_env('GIT_SSL_NO_VERIFY', 'true')

        return cls(git, version)


class GitRepo(object):
    """An instance of `ConfiguredGit`, confined to a specific repo.

    This class removes the chance of running a git command in the wrong repo by wrapping
    invocations of `__call__` and setting the working directory to the provided
    repo path.
    """
    git = None                  # type: ConfiguredGit
    repo_path = None            # type: str

    def __init__(self, git, repo_path):
        # type: (ConfiguredGit, str) -> None
        self.git = git
        self.repo_path = repo_path

    def __repr__(self):
        return '{0}(git={1!r}, repo_path={2!r})'.format(
            type(self).__name__, self.git, self.repo_path)

    def __call__(self, *args, **kwargs):
        with working_dir(self.repo_path):
            return self.git(*args, **kwargs)

    def _iter_branches(self):
        # type: () -> Iterator[Tuple[bool, GitRef]]
        """Iterate over the names of all branches in this git repository.

        The first element of the yielded tuples corresponds to whether the branch was
        HEAD, and the second element is the branch itself."""
        for line in (self('branch', '--format=%(refname)%(HEAD)', output=str)
                     .splitlines()):
            if line.startswith('refs/heads/'):
                ref = GitRef.branch(re.sub(r'^refs/heads/', '', line[:-1]))
                if line.endswith('*'):
                    yield True, ref
                else:
                    assert line.endswith(' '), line
                    yield False, ref

    def head_branch(self):
        # type: () -> Optional[GitRef]
        for is_head, branch in self._iter_branches():
            if is_head:
                return branch
        return None

    def branches_for(self):
        # type: () -> List[GitRef]
        return [branch for _, branch in self._iter_branches()]

    def expand_commit_hash(self, ref):
        # type: (GitRef) -> Optional[str]
        """Expands a ref into its full commit hash, or None if it does not exist."""
        check_commit_pattern = ref.refspec() + '^{commit}'
        try:
            return (self('rev-parse', '--verify', check_commit_pattern, output=str)
                    .strip())
        except ProcessError:
            return None

    def fetch(self, remote_url, ref, submodules, get_full_repo, verbose):
        # type: (str, GitRef, bool, bool, bool) -> None
        """Fetch the specified ref from the specified remote into the current repo."""
        args = (
            'fetch',
            '--verbose' if verbose else '--quiet',
            '--recurse-submodules={0}'.format('on-demand' if submodules else 'no'),
        )

        # If `get_full_repo=True`, first try to pull all new content down from the
        # remote without force-updating anything, and swallow any errors.
        if get_full_repo:
            try:
                # The refspec will fetch all branches from the remote, while
                # '--tags' will fetch tags pointing into any of those branches.
                full_args = args + ('--tags', remote_url, 'refs/heads/*:refs/heads/*')
                self(*full_args)
            except ProcessError:
                # If a branch was force-updated so it can't be fast-forwarded, or if
                # a tag was modified at all upstream, then this `git fetch` call will
                # exit nonzero, but still do as much useful work as it can.
                pass

        # Run `git fetch` again, ensuring that branches are updated from the remote even
        # if they cannot be fast-forwarded. Changing any tags upstream at all will raise
        # a FailedGitFetch.
        try:
            fetch_args = args + (remote_url, ref.fetch_spec())
            self(*fetch_args)
        except ProcessError as e:
            raise FailedGitFetch(remote_url, ref, self, e)

    def add_worktree(self, worktree_path, refspec, prune=True):
        # type: (str, str, bool) -> GitRepo
        # If the worktree directory already exists, assume it was already expanded.
        if os.path.isdir(worktree_path):
            return GitRepo(self.git, worktree_path)

        mkdirp(worktree_path)

        # `git worktree add -f` is necessary if the stage directory gets wiped, but
        # this leaves metadata around in the git repo pointing to missing worktrees.
        # `git worktree prune` avoids this.
        if prune:
            self('worktree', 'prune')

        # Create a new worktree at the given ref, within the empty worktree directory.
        self('worktree', 'add', worktree_path, refspec)

        return GitRepo(self.git, worktree_path)

    def _verbosity_args(self, verbose):
        # type: (bool) -> Tuple[str, ...]
        return () if verbose else ('--quiet',)

    def update_submodules(self, verbose=False):
        # type: (bool) -> None
        args = ('submodule',) + self._verbosity_args(verbose=verbose) + (
            'update', '--init', '--recursive',
        )
        self(*args)

    def delete_submodule(self, submodule_path, verbose=False):
        # type: (str, bool) -> None
        args = ('rm',) + self._verbosity_args(verbose=verbose) + (submodule_path,)
        self(*args)

    @staticmethod
    def _ensure_repo_exists(git, repo_path):
        # type: (ConfiguredGit, str) -> None
        """Initialize a git repository at the given `repo_path` if it does not exist."""
        # Check whether the directory exists.
        if not os.path.isdir(repo_path):
            mkdirp(repo_path)
            tty.debug('Created directory at {0}'.format(repo_path))
        # If the '.git' directory does not exist, run `git init`.
        if os.path.isdir(os.path.join(repo_path, '.git')):
            tty.debug('Already initialized git repo at {0}'.format(repo_path))
        else:
            with working_dir(repo_path):
                git('init')
            tty.debug('Newly initialized git repo at {0}'.format(repo_path))

    def _ensure_any_branch_exists(self):
        # type: () -> None
        if self.branches_for():
            return
        # `git branch` will only produce empty output immediately after `git
        # init` is run. In this case, we need to create a single ref guaranteed not to
        # collide with any branch name the user might want to check out, so we generate
        # a random UUID.
        self('checkout', '-b', 'spack-internal-{0}'.format(uuid.uuid4()))
        # Creating a ref requires making a commit.
        self('commit', '--allow-empty', '--allow-empty-message', '-m', '')

    @classmethod
    def initialize_idempotently(cls, git, repo_path):
        # type: (ConfiguredGit, str) -> GitRepo
        cls._ensure_repo_exists(git, repo_path)
        ret = cls(git, repo_path)
        ret._ensure_any_branch_exists()
        return ret


@fetcher
class GitFetchStrategy(VCSFetchStrategy):
    """Fetch strategy that gets source code from a git repository.

    Use like this in a package:

        version('name', git='https://github.com/project/repo.git')

    Optionally, you can provide a branch, or commit to check out, e.g.:

        version('1.1', git='https://github.com/project/repo.git', tag='v1.1')

    You can use these three optional attributes in addition to ``git``:

        * ``branch``: Particular branch to build from (default is the
                      repository's default branch)
        * ``tag``: Particular tag to check out
        * ``commit``: Particular commit hash in the repo

    Repositories are cloned into the standard stage source path directory.
    """
    url_attr = 'git'
    optional_attrs = ['tag', 'branch', 'commit', 'version_name',
                      'submodules', 'get_full_repo', 'submodules_delete']

    # Instance properties:
    submodules = None           # type: bool
    submodules_delete = None    # type: List[str]
    get_full_repo = None        # type: bool
    commit = None               # type: Optional[str]
    tag = None                  # type: Optional[str]
    branch = None               # type: Optional[str]
    # This argument is produced in the processing of git version() directives.
    version_name = None         # type: Optional[str]
    ref = None                  # type: GitRef

    def __init__(self, **kwargs):
        # Discards the keywords in kwargs that may conflict with the next call
        # to __init__.
        kwargs.pop('name', None)
        super(GitFetchStrategy, self).__init__(**kwargs)

        self.submodules = kwargs.pop('submodules', False)
        self.submodules_delete = kwargs.pop('submodules_delete', False)
        self.get_full_repo = kwargs.pop('get_full_repo', False)

        # Interpret the specific ref from the `version()` directive arguments. Error if
        # there's any ambiguity.
        try:
            self.ref = GitRef.from_directive(
                commit=self.commit,
                tag=self.tag,
                branch=self.branch,
                version_name=self.version_name)
        except InvalidGitRef as e:
            raise FetcherConflict(
                'Failed to identity an unambiguous refspec (commit, tag, or branch) '
                'from the version() arguments {0}:\n\n{1}'.format(kwargs, e))

    @property                   # type: ignore[misc]
    @memoized
    def canonical_git_repo(self):
        # type: () -> GitRepo
        """Lazily instantiate a GitRepo in the cache dir for this fetcher."""
        # Ensure git exists and configure it.
        git_exe = which('git', required=True)
        configured_git = ConfiguredGit.from_executable(git_exe)
        # Calculate the path to cache the git repo at.
        cache_path = spack.caches.fetch_cache.persistent_cache_dir_for(self)
        # Initialize the cached git repo.
        return GitRepo.initialize_idempotently(configured_git, cache_path)

    @property
    def cachable(self):
        # type: () -> bool
        return self.cache_enabled and not self.ref.is_mutable()

    def source_id(self):
        # type: () -> Optional[str]
        """Return the current refspec, when it points to an immutable object.

        A source id is supposed to be a reproducible source reference, which we can't
        have in the case of a branch."""
        if self.ref.is_mutable():
            return None
        return self.ref.refspec()

    def mirror_id(self):
        # type: () -> str
        repo_path = url_util.parse(self.url).path
        return os.path.sep.join(['git', repo_path, self.ref.refspec()])

    def _repo_info(self):
        # type: () -> str
        return '{0} {1}'.format(self.url, self.ref.repo_info_for_reference())

    def _maybe_expand_ref(self):
        # type: () -> Optional[str]
        """Return the full git hash for the current ref, if the ref exists locally."""
        return self.canonical_git_repo.expand_commit_hash(self.ref)

    def _do_fetch(self):
        # type: () -> str
        """Fetch the ref from the remote into the cache, then return the full git hash.

        This method checks that the ref successfully exists locally after fetching
        before returning.
        """
        verbose = bool(spack.config.get('config:debug'))
        self.canonical_git_repo.fetch(self.url, self.ref,
                                      self.submodules, self.get_full_repo,
                                      verbose=verbose)
        new_ref = self._maybe_expand_ref()
        assert new_ref is not None, (self.ref, self.canonical_git_repo)
        return new_ref

    def _ensure_local_ref(self):
        # type: () -> str
        """Fetch the ref specified by self.ref, and return its full git commit SHA."""
        current_expanded_ref = self._maybe_expand_ref()
        if current_expanded_ref is None:
            # We do not have the ref locally. Fetch it and check that it exists
            # after fetching.
            current_expanded_ref = self._do_fetch()
            tty.msg('Ref {0} -> {1} was newly downloaded from {2}.'
                    .format(self.ref, current_expanded_ref, self.url))
            return current_expanded_ref
        # We have the ref locally, and will not check for any updates.
        if not self.ref.is_mutable():
            tty.msg('Ref {0} -> {1} was already downloaded from {2}.'
                    .format(self.ref, current_expanded_ref, self.url))
            return current_expanded_ref

        # For branches which we have a previous copy of locally, we want to *attempt* to
        # fetch a newer version from the remote. If that fails, we continue to use the
        # locally-cached version.
        try:
            maybe_new_ref = self._do_fetch()
        except ProcessError as e:
            tty.warn(
                'Ref {0} -> {1} failed to update from {2} -- using local copy. '
                'The error was: {3}'
                .format(self.ref, current_expanded_ref, self.url, e))
            return current_expanded_ref
        # If we successfully fetched, print a nice message summarizing what kind of
        # update occurred, if any.
        if maybe_new_ref == current_expanded_ref:
            tty.msg('Ref {0} -> {1} did not have any updates from {2}.'
                    .format(self.ref, current_expanded_ref, self.url))
            return current_expanded_ref
        tty.msg('Ref {0} -> {1} was updated from previous value {2} at {3}.'
                .format(self.ref, maybe_new_ref, current_expanded_ref, self.url))
        return maybe_new_ref

    def _add_worktree(self, refspec):
        # type: (str) -> GitRepo
        """Checkout a worktree at `refspec` into the stage to form a `GitRepo`."""
        worktree_repo = self.canonical_git_repo.add_worktree(
            self.stage.source_path, refspec,
            prune=True)

        verbose = bool(spack.config.get('config:debug'))

        if self.submodules:
            # We decided whether to fetch submodule info earlier, but this command
            # actually performs the update operations over the checked-out submodules.
            worktree_repo.update_submodules(verbose=verbose)

            if self.submodules_delete:
                for submodule_to_delete in self.submodules_delete:
                    worktree_repo.delete_submodule(submodule_to_delete, verbose=verbose)

        return worktree_repo

    @_needs_stage
    def fetch(self):
        current_expanded_ref = self._ensure_local_ref()
        # In case the repo requires e.g. being checked out at a specific branch (and not
        # just a particular commit hash in a detached HEAD state), we provide the
        # refspec again to create the worktree.
        worktree_repo = self._add_worktree(self.ref.refspec())
        # We use an `assert` here because this should never fail!
        assert current_expanded_ref == worktree_repo.expand_commit_hash(self.ref), (
            current_expanded_ref, worktree_repo, self.ref)
        return True

    @_needs_stage
    def archive(self, destination):
        super(GitFetchStrategy, self).archive(destination, exclude='.git')

    @_needs_stage
    def reset(self):
        shutil.rmtree(self.stage.source_path, ignore_errors=True)
        self.fetch()

    def __str__(self):
        return '[git] {0}'.format(self._repo_info())


@fetcher
class SvnFetchStrategy(VCSFetchStrategy):

    """Fetch strategy that gets source code from a subversion repository.
       Use like this in a package:

           version('name', svn='http://www.example.com/svn/trunk')

       Optionally, you can provide a revision for the URL:

           version('name', svn='http://www.example.com/svn/trunk',
                   revision='1641')

    Repositories are checked out into the standard stage source path directory.
    """
    url_attr = 'svn'
    optional_attrs = ['revision']

    def __init__(self, **kwargs):
        # Discards the keywords in kwargs that may conflict with the next call
        # to __init__
        forwarded_args = copy.copy(kwargs)
        forwarded_args.pop('name', None)
        super(SvnFetchStrategy, self).__init__(**forwarded_args)

        self._svn = None
        if self.revision is not None:
            self.revision = str(self.revision)

    @property
    def svn(self):
        if not self._svn:
            self._svn = which('svn', required=True)
        return self._svn

    @property
    def cachable(self):
        return self.cache_enabled and bool(self.revision)

    def source_id(self):
        return self.revision

    def mirror_id(self):
        if self.revision:
            repo_path = url_util.parse(self.url).path
            result = os.path.sep.join(['svn', repo_path, self.revision])
            return result

    @_needs_stage
    def fetch(self):
        if self.stage.expanded:
            tty.debug('Already fetched {0}'.format(self.stage.source_path))
            return

        tty.debug('Checking out subversion repository: {0}'.format(self.url))

        args = ['checkout', '--force', '--quiet']
        if self.revision:
            args += ['-r', self.revision]
        args.extend([self.url])

        with temp_cwd():
            self.svn(*args)
            repo_name = get_single_file('.')
            self.stage.srcdir = repo_name
            shutil.move(repo_name, self.stage.source_path)

    def _remove_untracked_files(self):
        """Removes untracked files in an svn repository."""
        with working_dir(self.stage.source_path):
            status = self.svn('status', '--no-ignore', output=str)
            self.svn('status', '--no-ignore')
            for line in status.split('\n'):
                if not re.match('^[I?]', line):
                    continue
                path = line[8:].strip()
                if os.path.isfile(path):
                    os.unlink(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)

    def archive(self, destination):
        super(SvnFetchStrategy, self).archive(destination, exclude='.svn')

    @_needs_stage
    def reset(self):
        self._remove_untracked_files()
        with working_dir(self.stage.source_path):
            self.svn('revert', '.', '-R')

    def __str__(self):
        return "[svn] %s" % self.url


@fetcher
class HgFetchStrategy(VCSFetchStrategy):

    """
    Fetch strategy that gets source code from a Mercurial repository.
    Use like this in a package:

        version('name', hg='https://jay.grs.rwth-aachen.de/hg/lwm2')

    Optionally, you can provide a branch, or revision to check out, e.g.:

        version('torus',
                hg='https://jay.grs.rwth-aachen.de/hg/lwm2', branch='torus')

    You can use the optional 'revision' attribute to check out a
    branch, tag, or particular revision in hg.  To prevent
    non-reproducible builds, using a moving target like a branch is
    discouraged.

        * ``revision``: Particular revision, branch, or tag.

    Repositories are cloned into the standard stage source path directory.
    """
    url_attr = 'hg'
    optional_attrs = ['revision']

    def __init__(self, **kwargs):
        # Discards the keywords in kwargs that may conflict with the next call
        # to __init__
        forwarded_args = copy.copy(kwargs)
        forwarded_args.pop('name', None)
        super(HgFetchStrategy, self).__init__(**forwarded_args)

        self._hg = None

    @property
    def hg(self):
        """:returns: The hg executable
        :rtype: Executable
        """
        if not self._hg:
            self._hg = which('hg', required=True)

            # When building PythonPackages, Spack automatically sets
            # PYTHONPATH. This can interfere with hg, which is a Python
            # script. Unset PYTHONPATH while running hg.
            self._hg.add_default_env('PYTHONPATH', '')

        return self._hg

    @property
    def cachable(self):
        return self.cache_enabled and bool(self.revision)

    def source_id(self):
        return self.revision

    def mirror_id(self):
        if self.revision:
            repo_path = url_util.parse(self.url).path
            result = os.path.sep.join(['hg', repo_path, self.revision])
            return result

    @_needs_stage
    def fetch(self):
        if self.stage.expanded:
            tty.debug('Already fetched {0}'.format(self.stage.source_path))
            return

        args = []
        if self.revision:
            args.append('at revision %s' % self.revision)
        tty.debug('Cloning mercurial repository: {0} {1}'
                  .format(self.url, args))

        args = ['clone']

        if not spack.config.get('config:verify_ssl'):
            args.append('--insecure')

        if self.revision:
            args.extend(['-r', self.revision])

        args.extend([self.url])

        with temp_cwd():
            self.hg(*args)
            repo_name = get_single_file('.')
            self.stage.srcdir = repo_name
            shutil.move(repo_name, self.stage.source_path)

    def archive(self, destination):
        super(HgFetchStrategy, self).archive(destination, exclude='.hg')

    @_needs_stage
    def reset(self):
        with working_dir(self.stage.path):
            source_path = self.stage.source_path
            scrubbed = "scrubbed-source-tmp"

            args = ['clone']
            if self.revision:
                args += ['-r', self.revision]
            args += [source_path, scrubbed]
            self.hg(*args)

            shutil.rmtree(source_path, ignore_errors=True)
            shutil.move(scrubbed, source_path)

    def __str__(self):
        return "[hg] %s" % self.url


@fetcher
class S3FetchStrategy(URLFetchStrategy):
    """FetchStrategy that pulls from an S3 bucket."""
    url_attr = 's3'

    def __init__(self, *args, **kwargs):
        try:
            super(S3FetchStrategy, self).__init__(*args, **kwargs)
        except ValueError:
            if not kwargs.get('url'):
                raise ValueError(
                    "S3FetchStrategy requires a url for fetching.")

    @_needs_stage
    def fetch(self):
        if self.archive_file:
            tty.debug('Already downloaded {0}'.format(self.archive_file))
            return

        parsed_url = url_util.parse(self.url)
        if parsed_url.scheme != 's3':
            raise FetchError(
                'S3FetchStrategy can only fetch from s3:// urls.')

        tty.debug('Fetching {0}'.format(self.url))

        basename = os.path.basename(parsed_url.path)

        with working_dir(self.stage.path):
            _, headers, stream = web_util.read_from_url(self.url)

            with open(basename, 'wb') as f:
                shutil.copyfileobj(stream, f)

            content_type = web_util.get_header(headers, 'Content-type')

        if content_type == 'text/html':
            warn_content_type_mismatch(self.archive_file or "the archive")

        if self.stage.save_filename:
            os.rename(
                os.path.join(self.stage.path, basename),
                self.stage.save_filename)

        if not self.archive_file:
            raise FailedDownloadError(self.url)


def stable_target(fetcher):
    """Returns whether the fetcher target is expected to have a stable
       checksum. This is only true if the target is a preexisting archive
       file."""
    if isinstance(fetcher, URLFetchStrategy) and fetcher.cachable:
        return True
    return False


def from_url(url):
    """Given a URL, find an appropriate fetch strategy for it.
       Currently just gives you a URLFetchStrategy that uses curl.

       TODO: make this return appropriate fetch strategies for other
             types of URLs.
    """
    return URLFetchStrategy(url)


def from_kwargs(**kwargs):
    """Construct an appropriate FetchStrategy from the given keyword arguments.

    Args:
        **kwargs: dictionary of keyword arguments, e.g. from a
            ``version()`` directive in a package.

    Returns:
        fetch_strategy: The fetch strategy that matches the args, based
            on attribute names (e.g., ``git``, ``hg``, etc.)

    Raises:
        FetchError: If no ``fetch_strategy`` matches the args.
    """
    for fetcher in all_strategies:
        if fetcher.matches(kwargs):
            return fetcher(**kwargs)

    raise InvalidArgsError(**kwargs)


def check_pkg_attributes(pkg):
    """Find ambiguous top-level fetch attributes in a package.

    Currently this only ensures that two or more VCS fetch strategies are
    not specified at once.
    """
    # a single package cannot have URL attributes for multiple VCS fetch
    # strategies *unless* they are the same attribute.
    conflicts = set([s.url_attr for s in all_strategies
                     if hasattr(pkg, s.url_attr)])

    # URL isn't a VCS fetch method. We can use it with a VCS method.
    conflicts -= set(['url'])

    if len(conflicts) > 1:
        raise FetcherConflict(
            'Package %s cannot specify %s together. Pick at most one.'
            % (pkg.name, comma_and(quote(conflicts))))


def _check_version_attributes(fetcher, pkg, version):
    """Ensure that the fetcher for a version is not ambiguous.

    This assumes that we have already determined the fetcher for the
    specific version using ``for_package_version()``
    """
    all_optionals = set(a for s in all_strategies for a in s.optional_attrs)

    args = pkg.versions[version]
    extra\
        = set(args) - set(fetcher.optional_attrs) - \
        set([fetcher.url_attr, 'no_cache'])
    extra.intersection_update(all_optionals)

    if extra:
        legal_attrs = [fetcher.url_attr] + list(fetcher.optional_attrs)
        raise FetcherConflict(
            "%s version '%s' has extra arguments: %s"
            % (pkg.name, version, comma_and(quote(extra))),
            "Valid arguments for a %s fetcher are: \n    %s"
            % (fetcher.url_attr, comma_and(quote(legal_attrs))))


def _extrapolate(pkg, version):
    """Create a fetcher from an extrapolated URL for this version."""
    try:
        return URLFetchStrategy(pkg.url_for_version(version),
                                fetch_options=pkg.fetch_options)
    except spack.package.NoURLError:
        msg = ("Can't extrapolate a URL for version %s "
               "because package %s defines no URLs")
        raise ExtrapolationError(msg % (version, pkg.name))


def _from_merged_attrs(fetcher, pkg, version):
    """Create a fetcher from merged package and version attributes."""
    if fetcher.url_attr == 'url':
        url = pkg.url_for_version(version)
        # TODO: refactor this logic into its own method or function
        # TODO: to avoid duplication
        mirrors = [spack.url.substitute_version(u, version)
                   for u in getattr(pkg, 'urls', [])[1:]]
        attrs = {fetcher.url_attr: url, 'mirrors': mirrors}
    else:
        url = getattr(pkg, fetcher.url_attr)
        attrs = {fetcher.url_attr: url}

    attrs['fetch_options'] = pkg.fetch_options
    # version() directives may not explicitly provide any kwargs, and if this occurs
    # then the appropriate fetch strategy does not otherwise have access to the value of
    # the version() argument. Fetch strategies can accept 'version_name' in their
    # optional_attrs in order to be able to interpret bare version strings.
    attrs['version_name'] = str(version)
    attrs.update(pkg.versions[version])
    return fetcher(**attrs)


def for_package_version(pkg, version):
    """Determine a fetch strategy based on the arguments supplied to
       version() in the package description."""

    # No-code packages have a custom fetch strategy to work around issues
    # with resource staging.
    if not pkg.has_code:
        return BundleFetchStrategy()

    check_pkg_attributes(pkg)

    if not isinstance(version, Version):
        version = Version(version)

    # If it's not a known version, try to extrapolate one by URL
    if version not in pkg.versions:
        return _extrapolate(pkg, version)

    # Set package args first so version args can override them
    args = {'fetch_options': pkg.fetch_options}
    # Grab a dict of args out of the package version dict
    args.update(pkg.versions[version])

    # If the version specifies a `url_attr` directly, use that.
    for fetcher in all_strategies:
        if fetcher.url_attr in args:
            _check_version_attributes(fetcher, pkg, version)
            return fetcher(**args)

    # if a version's optional attributes imply a particular fetch
    # strategy, and we have the `url_attr`, then use that strategy.
    for fetcher in all_strategies:
        if hasattr(pkg, fetcher.url_attr) or fetcher.url_attr == 'url':
            optionals = fetcher.optional_attrs
            if optionals and any(a in args for a in optionals):
                _check_version_attributes(fetcher, pkg, version)
                return _from_merged_attrs(fetcher, pkg, version)

    # if the optional attributes tell us nothing, then use any `url_attr`
    # on the package.  This prefers URL vs. VCS, b/c URLFetchStrategy is
    # defined first in this file.
    for fetcher in all_strategies:
        if hasattr(pkg, fetcher.url_attr):
            _check_version_attributes(fetcher, pkg, version)
            return _from_merged_attrs(fetcher, pkg, version)

    raise InvalidArgsError(pkg, version, **args)


def from_url_scheme(url, *args, **kwargs):
    """Finds a suitable FetchStrategy by matching its url_attr with the scheme
       in the given url."""

    url = kwargs.get('url', url)
    parsed_url = urllib_parse.urlparse(url, scheme='file')

    scheme_mapping = (
        kwargs.get('scheme_mapping') or
        {
            'file': 'url',
            'http': 'url',
            'https': 'url',
            'ftp': 'url',
            'ftps': 'url',
        })

    scheme = parsed_url.scheme
    scheme = scheme_mapping.get(scheme, scheme)

    for fetcher in all_strategies:
        url_attr = getattr(fetcher, 'url_attr', None)
        if url_attr and url_attr == scheme:
            return fetcher(url, *args, **kwargs)

    raise ValueError(
        'No FetchStrategy found for url with scheme: "{SCHEME}"'.format(
            SCHEME=parsed_url.scheme))


def from_list_url(pkg):
    """If a package provides a URL which lists URLs for resources by
       version, this can can create a fetcher for a URL discovered for
       the specified package's version."""

    if pkg.list_url:
        try:
            versions = pkg.fetch_remote_versions()
            try:
                # get a URL, and a checksum if we have it
                url_from_list = versions[pkg.version]
                checksum = None

                # try to find a known checksum for version, from the package
                version = pkg.version
                if version in pkg.versions:
                    args = pkg.versions[version]
                    checksum = next(
                        (v for k, v in args.items() if k in crypto.hashes),
                        args.get('checksum'))

                # construct a fetcher
                return URLFetchStrategy(url_from_list, checksum,
                                        fetch_options=pkg.fetch_options)
            except KeyError as e:
                tty.debug(e)
                tty.msg("Cannot find version %s in url_list" % pkg.version)

        except BaseException as e:
            # TODO: Don't catch BaseException here! Be more specific.
            tty.debug(e)
            tty.msg("Could not determine url from list_url.")


class FsCache(object):

    def __init__(self, root):
        self.root = os.path.abspath(root)

    # TODO: use this method to determine the cache path for CacheURLFetchStrategy too!
    def persistent_cache_dir_for(self, fetcher):
        url_components = os.path.sep.join(filter(None, url_util.parse(fetcher.url)))
        return os.path.join(self.root, fetcher.url_attr, url_components)

    def store(self, fetcher, relative_dest):
        # Skip fetchers that aren't cachable.
        if not fetcher.cachable:
            return

        # Don't store things that are already cached.
        if isinstance(fetcher, CacheURLFetchStrategy):
            return

        dst = os.path.join(self.root, relative_dest)
        mkdirp(os.path.dirname(dst))
        fetcher.archive(dst)

    def fetcher(self, target_path, digest, **kwargs):
        path = os.path.join(self.root, target_path)
        return CacheURLFetchStrategy(path, digest, **kwargs)

    def destroy(self):
        shutil.rmtree(self.root, ignore_errors=True)


class FetchError(spack.error.SpackError):
    """Superclass fo fetcher errors."""


class NoCacheError(FetchError):
    """Raised when there is no cached archive for a package."""


class FailedDownloadError(FetchError):
    """Raised when a download fails."""
    def __init__(self, url, msg=""):
        super(FailedDownloadError, self).__init__(
            "Failed to fetch file from URL: %s" % url, msg)
        self.url = url


class NoArchiveFileError(FetchError):
    """"Raised when an archive file is expected but none exists."""


class NoDigestError(FetchError):
    """Raised after attempt to checksum when URL has no digest."""


class ExtrapolationError(FetchError):
    """Raised when we can't extrapolate a version for a package."""


class FetcherConflict(FetchError):
    """Raised for packages with invalid fetch attributes."""


class InvalidArgsError(FetchError):
    """Raised when a version can't be deduced from a set of arguments."""
    def __init__(self, pkg=None, version=None, **args):
        msg = "Could not guess a fetch strategy"
        if pkg:
            msg += ' for {pkg}'.format(pkg=pkg)
            if version:
                msg += '@{version}'.format(version=version)
        long_msg = 'with arguments: {args}'.format(args=args)
        super(InvalidArgsError, self).__init__(msg, long_msg)


class ChecksumError(FetchError):
    """Raised when archive fails to checksum."""


class NoStageError(FetchError):
    """Raised when fetch operations are called before set_stage()."""
    def __init__(self, method):
        super(NoStageError, self).__init__(
            "Must call FetchStrategy.set_stage() before calling %s" %
            method.__name__)


class InvalidGitRef(ValueError):
    """Raised internally when a single git version can't be deduced."""


class FailedGitFetch(FetchError):
    """Raised when git fails to fetch a ref for an unknown reason."""
    def __init__(self, remote_url, ref, git_repo, exc):
        # type: (str, GitRef, GitRepo, BaseException) -> None
        super(FailedGitFetch, self).__init__(
            "Failed to fetch ref {0} into repo {1} from remote: {2}"
            .format(ref, git_repo, remote_url),
            str(exc))
