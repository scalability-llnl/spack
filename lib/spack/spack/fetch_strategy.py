# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
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
import http.client
import os
import os.path
import re
import shutil
import urllib.error
import urllib.parse
import urllib.request
from pathlib import PurePath
from typing import List, Optional

import llnl.url
import llnl.util
import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.string import comma_and, quote
from llnl.util.filesystem import get_single_file, mkdirp, temp_cwd, working_dir
from llnl.util.symlink import symlink

import spack.config
import spack.error
import spack.oci.opener
import spack.util.archive
import spack.util.crypto as crypto
import spack.util.git
import spack.util.url as url_util
import spack.util.web as web_util
import spack.version
import spack.version.git_ref_lookup
from spack.util.compression import decompressor_for
from spack.util.executable import CommandNotFoundError, Executable, which

#: List of all fetch strategies, created by FetchStrategy metaclass.
all_strategies = []


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


class FetchStrategy:
    """Superclass of all fetch strategies."""

    #: The URL attribute must be specified either at the package class
    #: level, or as a keyword argument to ``version()``.  It is used to
    #: distinguish fetchers for different versions in the package DSL.
    url_attr: Optional[str] = None

    #: Optional attributes can be used to distinguish fetchers when :
    #: classes have multiple ``url_attrs`` at the top-level.
    # optional attributes in version() args.
    optional_attrs: List[str] = []

    def __init__(self, **kwargs):
        # The stage is initialized late, so that fetch strategies can be
        # constructed at package construction time.  This is where things
        # will be fetched.
        self.stage = None
        # Enable or disable caching for this strategy based on
        # 'no_cache' option from version directive.
        self.cache_enabled = not kwargs.pop("no_cache", False)

        self.package = None

    def set_package(self, package):
        self.package = package

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
    url_attr = ""

    def fetch(self):
        """Simply report success -- there is no code to fetch."""
        return True

    @property
    def cachable(self):
        """Report False as there is no code to cache."""
        return False

    def source_id(self):
        """BundlePackages don't have a source id."""
        return ""

    def mirror_id(self):
        """BundlePackages don't have a mirror id."""


@fetcher
class URLFetchStrategy(FetchStrategy):
    """URLFetchStrategy pulls source code from a URL for an archive, check the
    archive against a checksum, and decompresses the archive.

    The destination for the resulting file(s) is the standard stage path.
    """

    url_attr = "url"

    # these are checksum types. The generic 'checksum' is deprecated for
    # specific hash names, but we need it for backward compatibility
    optional_attrs = [*crypto.hashes.keys(), "checksum"]

    def __init__(self, *, url: str, checksum: Optional[str] = None, **kwargs) -> None:
        super().__init__(**kwargs)

        self.url = url
        self.mirrors = kwargs.get("mirrors", [])

        # digest can be set as the first argument, or from an explicit
        # kwarg by the hash name.
        self.digest: Optional[str] = checksum
        for h in self.optional_attrs:
            if h in kwargs:
                self.digest = kwargs[h]

        self.expand_archive: bool = kwargs.get("expand", True)
        self.extra_options: dict = kwargs.get("fetch_options", {})
        self._curl: Optional[Executable] = None
        self.extension: Optional[str] = kwargs.get("extension", None)
        self._effective_url: Optional[str] = None

    @property
    def curl(self) -> Executable:
        if not self._curl:
            self._curl = web_util.require_curl()
        return self._curl

    def source_id(self):
        return self.digest

    def mirror_id(self):
        if not self.digest:
            return None
        # The filename is the digest. A directory is also created based on
        # truncating the digest to avoid creating a directory with too many
        # entries
        return os.path.sep.join(["archive", self.digest[:2], self.digest])

    @property
    def candidate_urls(self):
        return [self.url] + (self.mirrors or [])

    @_needs_stage
    def fetch(self):
        if self.archive_file:
            tty.debug(f"Already downloaded {self.archive_file}")
            return

        errors: List[Exception] = []
        for url in self.candidate_urls:
            try:
                self._fetch_from_url(url)
                break
            except FailedDownloadError as e:
                errors.extend(e.exceptions)
        else:
            raise FailedDownloadError(*errors)

        if not self.archive_file:
            raise FailedDownloadError(
                RuntimeError(f"Missing archive {self.archive_file} after fetching")
            )

    def _fetch_from_url(self, url):
        if spack.config.get("config:url_fetch_method") == "curl":
            return self._fetch_curl(url)
        else:
            return self._fetch_urllib(url)

    def _check_headers(self, headers):
        # Check if we somehow got an HTML file rather than the archive we
        # asked for.  We only look at the last content type, to handle
        # redirects properly.
        content_types = re.findall(r"Content-Type:[^\r\n]+", headers, flags=re.IGNORECASE)
        if content_types and "text/html" in content_types[-1]:
            msg = (
                f"The contents of {self.archive_file or 'the archive'} fetched from {self.url} "
                " looks like HTML. This can indicate a broken URL, or an internet gateway issue."
            )
            if self._effective_url != self.url:
                msg += f" The URL redirected to {self._effective_url}."
            tty.warn(msg)

    @_needs_stage
    def _fetch_urllib(self, url):
        save_file = self.stage.save_filename

        request = urllib.request.Request(url, headers={"User-Agent": web_util.SPACK_USER_AGENT})

        try:
            response = web_util.urlopen(request)
        except (TimeoutError, urllib.error.URLError) as e:
            # clean up archive on failure.
            if self.archive_file:
                os.remove(self.archive_file)
            if os.path.lexists(save_file):
                os.remove(save_file)
            raise FailedDownloadError(e) from e

        tty.msg(f"Fetching {url}")

        if os.path.lexists(save_file):
            os.remove(save_file)

        with open(save_file, "wb") as f:
            shutil.copyfileobj(response, f)

        # Save the redirected URL for error messages. Sometimes we're redirected to an arbitrary
        # mirror that is broken, leading to spurious download failures. In that case it's helpful
        # for users to know which URL was actually fetched.
        if isinstance(response, http.client.HTTPResponse):
            self._effective_url = response.geturl()

        self._check_headers(str(response.headers))

    @_needs_stage
    def _fetch_curl(self, url):
        save_file = None
        partial_file = None
        if self.stage.save_filename:
            save_file = self.stage.save_filename
            partial_file = self.stage.save_filename + ".part"
        tty.msg(f"Fetching {url}")
        if partial_file:
            save_args = [
                "-C",
                "-",  # continue partial downloads
                "-o",
                partial_file,
            ]  # use a .part file
        else:
            save_args = ["-O"]

        timeout = 0
        cookie_args = []
        if self.extra_options:
            cookie = self.extra_options.get("cookie")
            if cookie:
                cookie_args.append("-j")  # junk cookies
                cookie_args.append("-b")  # specify cookie
                cookie_args.append(cookie)

            timeout = self.extra_options.get("timeout")

        base_args = web_util.base_curl_fetch_args(url, timeout)
        curl_args = save_args + base_args + cookie_args

        # Run curl but grab the mime type from the http headers
        curl = self.curl
        with working_dir(self.stage.path):
            headers = curl(*curl_args, output=str, fail_on_error=False)

        if curl.returncode != 0:
            # clean up archive on failure.
            if self.archive_file:
                os.remove(self.archive_file)

            if partial_file and os.path.lexists(partial_file):
                os.remove(partial_file)

            try:
                web_util.check_curl_code(curl.returncode)
            except spack.error.FetchError as e:
                raise FailedDownloadError(e) from e

        self._check_headers(headers)

        if save_file and (partial_file is not None):
            fs.rename(partial_file, save_file)

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
            tty.debug(
                "Staging unexpanded archive {0} in {1}".format(
                    self.archive_file, self.stage.source_path
                )
            )
            if not self.stage.expanded:
                mkdirp(self.stage.source_path)
            dest = os.path.join(self.stage.source_path, os.path.basename(self.archive_file))
            shutil.move(self.archive_file, dest)
            return

        tty.debug("Staging archive: {0}".format(self.archive_file))

        if not self.archive_file:
            raise NoArchiveFileError(
                "Couldn't find archive file", "Failed on expand() for URL %s" % self.url
            )

        # TODO: replace this by mime check.
        if not self.extension:
            self.extension = llnl.url.determine_url_file_extension(self.url)

        if self.stage.expanded:
            tty.debug("Source already staged to %s" % self.stage.source_path)
            return

        decompress = decompressor_for(self.archive_file, self.extension)

        # Below we assume that the command to decompress expand the
        # archive in the current working directory
        with fs.exploding_archive_catch(self.stage):
            decompress(self.archive_file)

    def archive(self, destination):
        """Just moves this archive to the destination."""
        if not self.archive_file:
            raise NoArchiveFileError("Cannot call archive() before fetching.")

        web_util.push_to_url(
            self.archive_file, url_util.path_to_file_url(destination), keep_original=True
        )

    @_needs_stage
    def check(self):
        """Check the downloaded archive against a checksum digest.
        No-op if this stage checks code out of a repository."""
        if not self.digest:
            raise NoDigestError(f"Attempt to check {self.__class__.__name__} with no digest.")

        verify_checksum(self.archive_file, self.digest, self.url, self._effective_url)

    @_needs_stage
    def reset(self):
        """
        Removes the source path if it exists, then re-expands the archive.
        """
        if not self.archive_file:
            raise NoArchiveFileError(
                f"Tried to reset {self.__class__.__name__} before fetching",
                f"Failed on reset() for URL{self.url}",
            )

        # Remove everything but the archive from the stage
        for filename in os.listdir(self.stage.path):
            abspath = os.path.join(self.stage.path, filename)
            if abspath != self.archive_file:
                shutil.rmtree(abspath, ignore_errors=True)

        # Expand the archive again
        self.expand()

    def __repr__(self):
        return f"{self.__class__.__name__}<{self.url}>"

    def __str__(self):
        return self.url


@fetcher
class CacheURLFetchStrategy(URLFetchStrategy):
    """The resource associated with a cache URL may be out of date."""

    @_needs_stage
    def fetch(self):
        path = url_util.file_url_string_to_path(self.url)

        # check whether the cache file exists.
        if not os.path.isfile(path):
            raise NoCacheError(f"No cache of {path}")

        # remove old symlink if one is there.
        filename = self.stage.save_filename
        if os.path.lexists(filename):
            os.remove(filename)

        # Symlink to local cached archive.
        symlink(path, filename)

        # Remove link if checksum fails, or subsequent fetchers will assume they don't need to
        # download.
        if self.digest:
            try:
                self.check()
            except ChecksumError:
                os.remove(self.archive_file)
                raise

        # Notify the user how we fetched.
        tty.msg(f"Using cached archive: {path}")


class OCIRegistryFetchStrategy(URLFetchStrategy):
    def __init__(self, *, url: str, checksum: Optional[str] = None, **kwargs):
        super().__init__(url=url, checksum=checksum, **kwargs)

        self._urlopen = kwargs.get("_urlopen", spack.oci.opener.urlopen)

    @_needs_stage
    def fetch(self):
        file = self.stage.save_filename
        tty.msg(f"Fetching {self.url}")

        try:
            response = self._urlopen(self.url)
        except (TimeoutError, urllib.error.URLError) as e:
            # clean up archive on failure.
            if self.archive_file:
                os.remove(self.archive_file)
            if os.path.lexists(file):
                os.remove(file)
            raise FailedDownloadError(e) from e

        if os.path.lexists(file):
            os.remove(file)

        with open(file, "wb") as f:
            shutil.copyfileobj(response, f)


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
        super().__init__(**kwargs)

        # Set a URL based on the type of fetch strategy.
        self.url = kwargs.get(self.url_attr, None)
        if not self.url:
            raise ValueError(f"{self.__class__} requires {self.url_attr} argument.")

        for attr in self.optional_attrs:
            setattr(self, attr, kwargs.get(attr, None))

    @_needs_stage
    def check(self):
        tty.debug(f"No checksum needed when fetching with {self.url_attr}")

    @_needs_stage
    def expand(self):
        tty.debug(f"Source fetched with {self.url_attr} is already expanded.")

    @_needs_stage
    def archive(self, destination, *, exclude: Optional[str] = None):
        assert llnl.url.extension_from_path(destination) == "tar.gz"
        assert self.stage.source_path.startswith(self.stage.path)
        # We need to prepend this dir name to every entry of the tarfile
        top_level_dir = PurePath(self.stage.srcdir or os.path.basename(self.stage.source_path))

        with working_dir(self.stage.source_path), spack.util.archive.gzip_compressed_tarfile(
            destination
        ) as (tar, _, _):
            spack.util.archive.reproducible_tarfile_from_prefix(
                tar=tar,
                prefix=".",
                skip=lambda entry: entry.name == exclude,
                path_to_name=lambda path: (top_level_dir / PurePath(path)).as_posix(),
            )

    def __str__(self):
        return f"VCS: {self.url}"

    def __repr__(self):
        return f"{self.__class__}<{self.url}>"


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

    url_attr = "go"

    def __init__(self, **kwargs):
        # Discards the keywords in kwargs that may conflict with the next
        # call to __init__
        forwarded_args = copy.copy(kwargs)
        forwarded_args.pop("name", None)
        super().__init__(**forwarded_args)

        self._go = None

    @property
    def go_version(self):
        vstring = self.go("version", output=str).split(" ")[2]
        return spack.version.Version(vstring)

    @property
    def go(self):
        if not self._go:
            self._go = which("go", required=True)
        return self._go

    @_needs_stage
    def fetch(self):
        tty.debug("Getting go resource: {0}".format(self.url))

        with working_dir(self.stage.path):
            try:
                os.mkdir("go")
            except OSError:
                pass
            env = dict(os.environ)
            env["GOPATH"] = os.path.join(os.getcwd(), "go")
            self.go("get", "-v", "-d", self.url, env=env)

    def archive(self, destination):
        super().archive(destination, exclude=".git")

    @_needs_stage
    def expand(self):
        tty.debug("Source fetched with %s is already expanded." % self.url_attr)

        # Move the directory to the well-known stage source path
        repo_root = _ensure_one_stage_entry(self.stage.path)
        shutil.move(repo_root, self.stage.source_path)

    @_needs_stage
    def reset(self):
        with working_dir(self.stage.source_path):
            self.go("clean")

    def __str__(self):
        return "[go] %s" % self.url


@fetcher
class GitFetchStrategy(VCSFetchStrategy):
    """
    Fetch strategy that gets source code from a git repository.
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

    url_attr = "git"
    optional_attrs = [
        "tag",
        "branch",
        "commit",
        "submodules",
        "get_full_repo",
        "submodules_delete",
        "git_sparse_paths",
    ]

    git_version_re = r"git version (\S+)"

    def __init__(self, **kwargs):

        self.commit: Optional[str] = None
        self.tag: Optional[str] = None
        self.branch: Optional[str] = None

        # Discards the keywords in kwargs that may conflict with the next call
        # to __init__
        forwarded_args = copy.copy(kwargs)
        forwarded_args.pop("name", None)
        super().__init__(**forwarded_args)

        self._git = None
        self.submodules = kwargs.get("submodules", False)
        self.submodules_delete = kwargs.get("submodules_delete", False)
        self.get_full_repo = kwargs.get("get_full_repo", False)
        self.git_sparse_paths = kwargs.get("git_sparse_paths", None)

    @property
    def git_version(self):
        return GitFetchStrategy.version_from_git(self.git)

    @staticmethod
    def version_from_git(git_exe):
        """Given a git executable, return the Version (this will fail if
        the output cannot be parsed into a valid Version).
        """
        version_output = git_exe("--version", output=str)
        m = re.search(GitFetchStrategy.git_version_re, version_output)
        return spack.version.Version(m.group(1))

    @property
    def git(self):
        if not self._git:
            try:
                self._git = spack.util.git.git(required=True)
            except CommandNotFoundError as exc:
                tty.error(str(exc))
                raise

            # Disable advice for a quieter fetch
            # https://github.com/git/git/blob/master/Documentation/RelNotes/1.7.2.txt
            if self.git_version >= spack.version.Version("1.7.2"):
                self._git.add_default_arg("-c", "advice.detachedHead=false")

            # If the user asked for insecure fetching, make that work
            # with git as well.
            if not spack.config.get("config:verify_ssl"):
                self._git.add_default_env("GIT_SSL_NO_VERIFY", "true")

        return self._git

    @property
    def cachable(self):
        return self.cache_enabled and bool(self.commit)

    def source_id(self):
        # TODO: tree-hash would secure download cache and mirrors, commit only secures checkouts.
        return self.commit

    def mirror_id(self):
        if self.commit:
            repo_path = urllib.parse.urlparse(self.url).path
            result = os.path.sep.join(["git", repo_path, self.commit])
            return result

    def _repo_info(self):
        args = ""
        if self.commit:
            args = f" at commit {self.commit}"
        elif self.tag:
            args = f" at tag {self.tag}"
        elif self.branch:
            args = f" on branch {self.branch}"

        return f"{self.url}{args}"

    @_needs_stage
    def fetch(self):
        if self.stage.expanded:
            tty.debug(f"Already fetched {self.stage.source_path}")
            return

        if self.git_sparse_paths:
            self._sparse_clone_src()
        else:
            self._clone_src()
        self.submodule_operations()

    def bare_clone(self, dest: str) -> None:
        """
        Execute a bare clone for metadata only

        Requires a destination since bare cloning does not provide source
        and shouldn't be used for staging.
        """
        # Default to spack source path
        tty.debug(f"Cloning git repository: {self._repo_info()}")

        git = self.git
        debug = spack.config.get("config:debug")

        # We don't need to worry about which commit/branch/tag is checked out
        clone_args = ["clone", "--bare"]
        if not debug:
            clone_args.append("--quiet")
        clone_args.extend([self.url, dest])
        git(*clone_args)

    def _clone_src(self) -> None:
        """Clone a repository to a path using git."""
        # Default to spack source path
        dest = self.stage.source_path
        tty.debug(f"Cloning git repository: {self._repo_info()}")

        git = self.git
        debug = spack.config.get("config:debug")

        if self.commit:
            # Need to do a regular clone and check out everything if
            # they asked for a particular commit.
            clone_args = ["clone", self.url]
            if not debug:
                clone_args.insert(1, "--quiet")
            with temp_cwd():
                git(*clone_args)
                repo_name = get_single_file(".")
                if self.stage:
                    self.stage.srcdir = repo_name
                shutil.copytree(repo_name, dest, symlinks=True)
                shutil.rmtree(
                    repo_name,
                    ignore_errors=False,
                    onerror=fs.readonly_file_handler(ignore_errors=True),
                )

            with working_dir(dest):
                checkout_args = ["checkout", self.commit]
                if not debug:
                    checkout_args.insert(1, "--quiet")
                git(*checkout_args)

        else:
            # Can be more efficient if not checking out a specific commit.
            args = ["clone"]
            if not debug:
                args.append("--quiet")

            # If we want a particular branch ask for it.
            if self.branch:
                args.extend(["--branch", self.branch])
            elif self.tag and self.git_version >= spack.version.Version("1.8.5.2"):
                args.extend(["--branch", self.tag])

            # Try to be efficient if we're using a new enough git.
            # This checks out only one branch's history
            if self.git_version >= spack.version.Version("1.7.10"):
                if self.get_full_repo:
                    args.append("--no-single-branch")
                else:
                    args.append("--single-branch")

            with temp_cwd():
                # Yet more efficiency: only download a 1-commit deep
                # tree, if the in-use git and protocol permit it.
                if (
                    (not self.get_full_repo)
                    and self.git_version >= spack.version.Version("1.7.1")
                    and self.protocol_supports_shallow_clone()
                ):
                    args.extend(["--depth", "1"])

                args.extend([self.url])
                git(*args)

                repo_name = get_single_file(".")
                if self.stage:
                    self.stage.srcdir = repo_name
                shutil.move(repo_name, dest)

            with working_dir(dest):
                # For tags, be conservative and check them out AFTER
                # cloning.  Later git versions can do this with clone
                # --branch, but older ones fail.
                if self.tag and self.git_version < spack.version.Version("1.8.5.2"):
                    # pull --tags returns a "special" error code of 1 in
                    # older versions that we have to ignore.
                    # see: https://github.com/git/git/commit/19d122b
                    pull_args = ["pull", "--tags"]
                    co_args = ["checkout", self.tag]
                    if not spack.config.get("config:debug"):
                        pull_args.insert(1, "--quiet")
                        co_args.insert(1, "--quiet")

                    git(*pull_args, ignore_errors=1)
                    git(*co_args)

    def _sparse_clone_src(self, **kwargs):
        """Use git's sparse checkout feature to clone portions of a git repository"""
        dest = self.stage.source_path
        git = self.git

        if self.git_version < spack.version.Version("2.26.0"):
            # technically this should be supported for 2.25, but bumping for OS issues
            # see https://github.com/spack/spack/issues/45771
            # code paths exist where the package is not set.  Assure some indentifier for the
            # package that was configured  for sparse checkout exists in the error message
            identifier = str(self.url)
            if self.package:
                identifier += f" ({self.package.name})"
            tty.warn(
                (
                    f"{identifier} is configured for git sparse-checkout "
                    "but the git version is too old to support sparse cloning. "
                    "Cloning the full repository instead."
                )
            )
            self._clone_src()
        else:
            # default to depth=2 to allow for retention of some git properties
            depth = kwargs.get("depth", 2)
            needs_fetch = self.branch or self.tag
            git_ref = self.branch or self.tag or self.commit

            assert git_ref

            clone_args = ["clone"]

            if needs_fetch:
                clone_args.extend(["--branch", git_ref])

            if self.get_full_repo:
                clone_args.append("--no-single-branch")
            else:
                clone_args.append("--single-branch")

            clone_args.extend(
                [f"--depth={depth}", "--no-checkout", "--filter=blob:none", self.url]
            )

            sparse_args = ["sparse-checkout", "set"]

            if callable(self.git_sparse_paths):
                sparse_args.extend(self.git_sparse_paths())
            else:
                sparse_args.extend([p for p in self.git_sparse_paths])

            sparse_args.append("--cone")

            checkout_args = ["checkout", git_ref]

            if not spack.config.get("config:debug"):
                clone_args.insert(1, "--quiet")
                checkout_args.insert(1, "--quiet")

            with temp_cwd():
                git(*clone_args)
                repo_name = get_single_file(".")
                if self.stage:
                    self.stage.srcdir = repo_name
                shutil.move(repo_name, dest)

            with working_dir(dest):
                git(*sparse_args)
                git(*checkout_args)

    def submodule_operations(self):
        dest = self.stage.source_path
        git = self.git

        if self.submodules_delete:
            with working_dir(dest):
                for submodule_to_delete in self.submodules_delete:
                    args = ["rm", submodule_to_delete]
                    if not spack.config.get("config:debug"):
                        args.insert(1, "--quiet")
                    git(*args)

        # Init submodules if the user asked for them.
        git_commands = []
        submodules = self.submodules
        if callable(submodules):
            submodules = submodules(self.package)
            if submodules:
                if isinstance(submodules, str):
                    submodules = [submodules]
                git_commands.append(["submodule", "init", "--"] + submodules)
                git_commands.append(["submodule", "update", "--recursive"])
        elif submodules:
            git_commands.append(["submodule", "update", "--init", "--recursive"])

        if not git_commands:
            return

        with working_dir(dest):
            for args in git_commands:
                if not spack.config.get("config:debug"):
                    args.insert(1, "--quiet")
                git(*args)

    def archive(self, destination):
        super().archive(destination, exclude=".git")

    @_needs_stage
    def reset(self):
        with working_dir(self.stage.source_path):
            co_args = ["checkout", "."]
            clean_args = ["clean", "-f"]
            if spack.config.get("config:debug"):
                co_args.insert(1, "--quiet")
                clean_args.insert(1, "--quiet")

            self.git(*co_args)
            self.git(*clean_args)

    def protocol_supports_shallow_clone(self):
        """Shallow clone operations (--depth #) are not supported by the basic
        HTTP protocol or by no-protocol file specifications.
        Use (e.g.) https:// or file:// instead."""
        return not (self.url.startswith("http://") or self.url.startswith("/"))

    def __str__(self):
        return f"[git] {self._repo_info()}"


@fetcher
class CvsFetchStrategy(VCSFetchStrategy):
    """Fetch strategy that gets source code from a CVS repository.
       Use like this in a package:

           version('name',
                   cvs=':pserver:anonymous@www.example.com:/cvsroot%module=modulename')

       Optionally, you can provide a branch and/or a date for the URL:

           version('name',
                   cvs=':pserver:anonymous@www.example.com:/cvsroot%module=modulename',
                   branch='branchname', date='date')

    Repositories are checked out into the standard stage source path directory.
    """

    url_attr = "cvs"
    optional_attrs = ["branch", "date"]

    def __init__(self, **kwargs):
        # Discards the keywords in kwargs that may conflict with the next call
        # to __init__
        forwarded_args = copy.copy(kwargs)
        forwarded_args.pop("name", None)
        super().__init__(**forwarded_args)

        self._cvs = None
        if self.branch is not None:
            self.branch = str(self.branch)
        if self.date is not None:
            self.date = str(self.date)

    @property
    def cvs(self):
        if not self._cvs:
            self._cvs = which("cvs", required=True)
        return self._cvs

    @property
    def cachable(self):
        return self.cache_enabled and (bool(self.branch) or bool(self.date))

    def source_id(self):
        if not (self.branch or self.date):
            # We need a branch or a date to make a checkout reproducible
            return None
        id = "id"
        if self.branch:
            id += "-branch=" + self.branch
        if self.date:
            id += "-date=" + self.date
        return id

    def mirror_id(self):
        if not (self.branch or self.date):
            # We need a branch or a date to make a checkout reproducible
            return None
        # Special-case handling because this is not actually a URL
        elements = self.url.split(":")
        final = elements[-1]
        elements = final.split("/")
        # Everything before the first slash is a port number
        elements = elements[1:]
        result = os.path.sep.join(["cvs"] + elements)
        if self.branch:
            result += "%branch=" + self.branch
        if self.date:
            result += "%date=" + self.date
        return result

    @_needs_stage
    def fetch(self):
        if self.stage.expanded:
            tty.debug("Already fetched {0}".format(self.stage.source_path))
            return

        tty.debug("Checking out CVS repository: {0}".format(self.url))

        with temp_cwd():
            url, module = self.url.split("%module=")
            # Check out files
            args = ["-z9", "-d", url, "checkout"]
            if self.branch is not None:
                args.extend(["-r", self.branch])
            if self.date is not None:
                args.extend(["-D", self.date])
            args.append(module)
            self.cvs(*args)
            # Rename repo
            repo_name = get_single_file(".")
            self.stage.srcdir = repo_name
            shutil.move(repo_name, self.stage.source_path)

    def _remove_untracked_files(self):
        """Removes untracked files in a CVS repository."""
        with working_dir(self.stage.source_path):
            status = self.cvs("-qn", "update", output=str)
            for line in status.split("\n"):
                if re.match(r"^[?]", line):
                    path = line[2:].strip()
                    if os.path.isfile(path):
                        os.unlink(path)

    def archive(self, destination):
        super().archive(destination, exclude="CVS")

    @_needs_stage
    def reset(self):
        self._remove_untracked_files()
        with working_dir(self.stage.source_path):
            self.cvs("update", "-C", ".")

    def __str__(self):
        return "[cvs] %s" % self.url


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

    url_attr = "svn"
    optional_attrs = ["revision"]

    def __init__(self, **kwargs):
        # Discards the keywords in kwargs that may conflict with the next call
        # to __init__
        forwarded_args = copy.copy(kwargs)
        forwarded_args.pop("name", None)
        super().__init__(**forwarded_args)

        self._svn = None
        if self.revision is not None:
            self.revision = str(self.revision)

    @property
    def svn(self):
        if not self._svn:
            self._svn = which("svn", required=True)
        return self._svn

    @property
    def cachable(self):
        return self.cache_enabled and bool(self.revision)

    def source_id(self):
        return self.revision

    def mirror_id(self):
        if self.revision:
            repo_path = urllib.parse.urlparse(self.url).path
            result = os.path.sep.join(["svn", repo_path, self.revision])
            return result

    @_needs_stage
    def fetch(self):
        if self.stage.expanded:
            tty.debug("Already fetched {0}".format(self.stage.source_path))
            return

        tty.debug("Checking out subversion repository: {0}".format(self.url))

        args = ["checkout", "--force", "--quiet"]
        if self.revision:
            args += ["-r", self.revision]
        args.extend([self.url])

        with temp_cwd():
            self.svn(*args)
            repo_name = get_single_file(".")
            self.stage.srcdir = repo_name
            shutil.move(repo_name, self.stage.source_path)

    def _remove_untracked_files(self):
        """Removes untracked files in an svn repository."""
        with working_dir(self.stage.source_path):
            status = self.svn("status", "--no-ignore", output=str)
            self.svn("status", "--no-ignore")
            for line in status.split("\n"):
                if not re.match("^[I?]", line):
                    continue
                path = line[8:].strip()
                if os.path.isfile(path):
                    os.unlink(path)
                elif os.path.isdir(path):
                    shutil.rmtree(path, ignore_errors=True)

    def archive(self, destination):
        super().archive(destination, exclude=".svn")

    @_needs_stage
    def reset(self):
        self._remove_untracked_files()
        with working_dir(self.stage.source_path):
            self.svn("revert", ".", "-R")

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

    url_attr = "hg"
    optional_attrs = ["revision"]

    def __init__(self, **kwargs):
        # Discards the keywords in kwargs that may conflict with the next call
        # to __init__
        forwarded_args = copy.copy(kwargs)
        forwarded_args.pop("name", None)
        super().__init__(**forwarded_args)

        self._hg = None

    @property
    def hg(self):
        """
        Returns:
            Executable: the hg executable
        """
        if not self._hg:
            self._hg = which("hg", required=True)

            # When building PythonPackages, Spack automatically sets
            # PYTHONPATH. This can interfere with hg, which is a Python
            # script. Unset PYTHONPATH while running hg.
            self._hg.add_default_env("PYTHONPATH", "")

        return self._hg

    @property
    def cachable(self):
        return self.cache_enabled and bool(self.revision)

    def source_id(self):
        return self.revision

    def mirror_id(self):
        if self.revision:
            repo_path = urllib.parse.urlparse(self.url).path
            result = os.path.sep.join(["hg", repo_path, self.revision])
            return result

    @_needs_stage
    def fetch(self):
        if self.stage.expanded:
            tty.debug("Already fetched {0}".format(self.stage.source_path))
            return

        args = []
        if self.revision:
            args.append("at revision %s" % self.revision)
        tty.debug("Cloning mercurial repository: {0} {1}".format(self.url, args))

        args = ["clone"]

        if not spack.config.get("config:verify_ssl"):
            args.append("--insecure")

        if self.revision:
            args.extend(["-r", self.revision])

        args.extend([self.url])

        with temp_cwd():
            self.hg(*args)
            repo_name = get_single_file(".")
            self.stage.srcdir = repo_name
            shutil.move(repo_name, self.stage.source_path)

    def archive(self, destination):
        super().archive(destination, exclude=".hg")

    @_needs_stage
    def reset(self):
        with working_dir(self.stage.path):
            source_path = self.stage.source_path
            scrubbed = "scrubbed-source-tmp"

            args = ["clone"]
            if self.revision:
                args += ["-r", self.revision]
            args += [source_path, scrubbed]
            self.hg(*args)

            shutil.rmtree(source_path, ignore_errors=True)
            shutil.move(scrubbed, source_path)

    def __str__(self):
        return f"[hg] {self.url}"


@fetcher
class S3FetchStrategy(URLFetchStrategy):
    """FetchStrategy that pulls from an S3 bucket."""

    url_attr = "s3"

    @_needs_stage
    def fetch(self):
        if not self.url.startswith("s3://"):
            raise spack.error.FetchError(
                f"{self.__class__.__name__} can only fetch from s3:// urls."
            )
        if self.archive_file:
            tty.debug(f"Already downloaded {self.archive_file}")
            return
        self._fetch_urllib(self.url)
        if not self.archive_file:
            raise FailedDownloadError(
                RuntimeError(f"Missing archive {self.archive_file} after fetching")
            )


@fetcher
class GCSFetchStrategy(URLFetchStrategy):
    """FetchStrategy that pulls from a GCS bucket."""

    url_attr = "gs"

    @_needs_stage
    def fetch(self):
        if not self.url.startswith("gs"):
            raise spack.error.FetchError(
                f"{self.__class__.__name__} can only fetch from gs:// urls."
            )
        if self.archive_file:
            tty.debug(f"Already downloaded {self.archive_file}")
            return

        self._fetch_urllib(self.url)

        if not self.archive_file:
            raise FailedDownloadError(
                RuntimeError(f"Missing archive {self.archive_file} after fetching")
            )


@fetcher
class FetchAndVerifyExpandedFile(URLFetchStrategy):
    """Fetch strategy that verifies the content digest during fetching,
    as well as after expanding it."""

    def __init__(self, url, archive_sha256: str, expanded_sha256: str):
        super().__init__(url=url, checksum=archive_sha256)
        self.expanded_sha256 = expanded_sha256

    def expand(self):
        """Verify checksum after expanding the archive."""

        # Expand the archive
        super().expand()

        # Ensure a single patch file.
        src_dir = self.stage.source_path
        files = os.listdir(src_dir)

        if len(files) != 1:
            raise ChecksumError(self, f"Expected a single file in {src_dir}.")

        verify_checksum(
            os.path.join(src_dir, files[0]), self.expanded_sha256, self.url, self._effective_url
        )


def verify_checksum(file: str, digest: str, url: str, effective_url: Optional[str]) -> None:
    checker = crypto.Checker(digest)
    if not checker.check(file):
        # On failure, provide some information about the file size and
        # contents, so that we can quickly see what the issue is (redirect
        # was not followed, empty file, text instead of binary, ...)
        size, contents = fs.filesummary(file)
        long_msg = (
            f"Expected {digest} but got {checker.sum}. "
            f"File size = {size} bytes. Contents = {contents!r}. "
            f"URL = {url}"
        )
        if effective_url and effective_url != url:
            long_msg += f", redirected to = {effective_url}"
        raise ChecksumError(f"{checker.hash_name} checksum failed for {file}", long_msg)


def stable_target(fetcher):
    """Returns whether the fetcher target is expected to have a stable
    checksum. This is only true if the target is a preexisting archive
    file."""
    if isinstance(fetcher, URLFetchStrategy) and fetcher.cachable:
        return True
    return False


def from_url(url: str) -> URLFetchStrategy:
    """Given a URL, find an appropriate fetch strategy for it.
    Currently just gives you a URLFetchStrategy that uses curl.

    TODO: make this return appropriate fetch strategies for other
          types of URLs.
    """
    return URLFetchStrategy(url=url)


def from_kwargs(**kwargs):
    """Construct an appropriate FetchStrategy from the given keyword arguments.

    Args:
        **kwargs: dictionary of keyword arguments, e.g. from a
            ``version()`` directive in a package.

    Returns:
        typing.Callable: The fetch strategy that matches the args, based
            on attribute names (e.g., ``git``, ``hg``, etc.)

    Raises:
        spack.error.FetchError: If no ``fetch_strategy`` matches the args.
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
    conflicts = set([s.url_attr for s in all_strategies if hasattr(pkg, s.url_attr)])

    # URL isn't a VCS fetch method. We can use it with a VCS method.
    conflicts -= set(["url"])

    if len(conflicts) > 1:
        raise FetcherConflict(
            "Package %s cannot specify %s together. Pick at most one."
            % (pkg.name, comma_and(quote(conflicts)))
        )


def _check_version_attributes(fetcher, pkg, version):
    """Ensure that the fetcher for a version is not ambiguous.

    This assumes that we have already determined the fetcher for the
    specific version using ``for_package_version()``
    """
    all_optionals = set(a for s in all_strategies for a in s.optional_attrs)

    args = pkg.versions[version]
    extra = set(args) - set(fetcher.optional_attrs) - set([fetcher.url_attr, "no_cache"])
    extra.intersection_update(all_optionals)

    if extra:
        legal_attrs = [fetcher.url_attr] + list(fetcher.optional_attrs)
        raise FetcherConflict(
            "%s version '%s' has extra arguments: %s"
            % (pkg.name, version, comma_and(quote(extra))),
            "Valid arguments for a %s fetcher are: \n    %s"
            % (fetcher.url_attr, comma_and(quote(legal_attrs))),
        )


def _extrapolate(pkg, version):
    """Create a fetcher from an extrapolated URL for this version."""
    try:
        return URLFetchStrategy(url=pkg.url_for_version(version), fetch_options=pkg.fetch_options)
    except spack.error.NoURLError:
        raise ExtrapolationError(
            f"Can't extrapolate a URL for version {version} because "
            f"package {pkg.name} defines no URLs"
        )


def _from_merged_attrs(fetcher, pkg, version):
    """Create a fetcher from merged package and version attributes."""
    if fetcher.url_attr == "url":
        mirrors = pkg.all_urls_for_version(version)
        url = mirrors[0]
        mirrors = mirrors[1:]
        attrs = {fetcher.url_attr: url, "mirrors": mirrors}
    else:
        url = getattr(pkg, fetcher.url_attr)
        attrs = {fetcher.url_attr: url}

    attrs["fetch_options"] = pkg.fetch_options
    attrs.update(pkg.versions[version])

    if fetcher.url_attr == "git":
        pkg_attr_list = ["submodules", "git_sparse_paths"]
        for pkg_attr in pkg_attr_list:
            if hasattr(pkg, pkg_attr):
                attrs.setdefault(pkg_attr, getattr(pkg, pkg_attr))

    return fetcher(**attrs)


def for_package_version(pkg, version=None):
    """Determine a fetch strategy based on the arguments supplied to
    version() in the package description."""

    # No-code packages have a custom fetch strategy to work around issues
    # with resource staging.
    if not pkg.has_code:
        return BundleFetchStrategy()

    check_pkg_attributes(pkg)

    if version is not None:
        assert not pkg.spec.concrete, "concrete specs should not pass the 'version=' argument"
        # Specs are initialized with the universe range, if no version information is given,
        # so here we make sure we always match the version passed as argument
        if not isinstance(version, spack.version.StandardVersion):
            version = spack.version.Version(version)

        version_list = spack.version.VersionList()
        version_list.add(version)
        pkg.spec.versions = version_list
    else:
        version = pkg.version

    # if it's a commit, we must use a GitFetchStrategy
    if isinstance(version, spack.version.GitVersion):
        if not hasattr(pkg, "git"):
            raise spack.error.FetchError(
                f"Cannot fetch git version for {pkg.name}. Package has no 'git' attribute"
            )
        # Populate the version with comparisons to other commits
        version.attach_lookup(spack.version.git_ref_lookup.GitRefLookup(pkg.name))

        # For GitVersion, we have no way to determine whether a ref is a branch or tag
        # Fortunately, we handle branches and tags identically, except tags are
        # handled slightly more conservatively for older versions of git.
        # We call all non-commit refs tags in this context, at the cost of a slight
        # performance hit for branches on older versions of git.
        # Branches cannot be cached, so we tell the fetcher not to cache tags/branches
        ref_type = "commit" if version.is_commit else "tag"
        kwargs = {"git": pkg.git, ref_type: version.ref, "no_cache": True}

        kwargs["submodules"] = getattr(pkg, "submodules", False)

        # if the ref_version is a known version from the package, use that version's
        # submodule specifications
        ref_version_attributes = pkg.versions.get(pkg.version.ref_version)
        if ref_version_attributes:
            kwargs["submodules"] = ref_version_attributes.get("submodules", kwargs["submodules"])

        fetcher = GitFetchStrategy(**kwargs)
        return fetcher

    # If it's not a known version, try to extrapolate one by URL
    if version not in pkg.versions:
        return _extrapolate(pkg, version)

    # Set package args first so version args can override them
    args = {"fetch_options": pkg.fetch_options}
    # Grab a dict of args out of the package version dict
    args.update(pkg.versions[version])

    # If the version specifies a `url_attr` directly, use that.
    for fetcher in all_strategies:
        if fetcher.url_attr in args:
            _check_version_attributes(fetcher, pkg, version)
            if fetcher.url_attr == "git" and hasattr(pkg, "submodules"):
                args.setdefault("submodules", pkg.submodules)
            return fetcher(**args)

    # if a version's optional attributes imply a particular fetch
    # strategy, and we have the `url_attr`, then use that strategy.
    for fetcher in all_strategies:
        if hasattr(pkg, fetcher.url_attr) or fetcher.url_attr == "url":
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


def from_url_scheme(url: str, **kwargs) -> FetchStrategy:
    """Finds a suitable FetchStrategy by matching its url_attr with the scheme
    in the given url."""
    parsed_url = urllib.parse.urlparse(url, scheme="file")

    scheme_mapping = kwargs.get("scheme_mapping") or {
        "file": "url",
        "http": "url",
        "https": "url",
        "ftp": "url",
        "ftps": "url",
    }

    scheme = parsed_url.scheme
    scheme = scheme_mapping.get(scheme, scheme)

    for fetcher in all_strategies:
        url_attr = getattr(fetcher, "url_attr", None)
        if url_attr and url_attr == scheme:
            return fetcher(url=url, **kwargs)

    raise ValueError(f'No FetchStrategy found for url with scheme: "{parsed_url.scheme}"')


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
                        (v for k, v in args.items() if k in crypto.hashes), args.get("checksum")
                    )

                # construct a fetcher
                return URLFetchStrategy(
                    url=url_from_list, checksum=checksum, fetch_options=pkg.fetch_options
                )
            except KeyError as e:
                tty.debug(e)
                tty.msg("Cannot find version %s in url_list" % pkg.version)

        except BaseException as e:
            # TODO: Don't catch BaseException here! Be more specific.
            tty.debug(e)
            tty.msg("Could not determine url from list_url.")


class FsCache:
    def __init__(self, root):
        self.root = os.path.abspath(root)

    def store(self, fetcher, relative_dest):
        # skip fetchers that aren't cachable
        if not fetcher.cachable:
            return

        # Don't store things that are already cached.
        if isinstance(fetcher, CacheURLFetchStrategy):
            return

        dst = os.path.join(self.root, relative_dest)
        mkdirp(os.path.dirname(dst))
        fetcher.archive(dst)

    def fetcher(self, target_path: str, digest: Optional[str], **kwargs) -> CacheURLFetchStrategy:
        path = os.path.join(self.root, target_path)
        url = url_util.path_to_file_url(path)
        return CacheURLFetchStrategy(url=url, checksum=digest, **kwargs)

    def destroy(self):
        shutil.rmtree(self.root, ignore_errors=True)


class NoCacheError(spack.error.FetchError):
    """Raised when there is no cached archive for a package."""


class FailedDownloadError(spack.error.FetchError):
    """Raised when a download fails."""

    def __init__(self, *exceptions: Exception):
        super().__init__("Failed to download")
        self.exceptions = exceptions


class NoArchiveFileError(spack.error.FetchError):
    """Raised when an archive file is expected but none exists."""


class NoDigestError(spack.error.FetchError):
    """Raised after attempt to checksum when URL has no digest."""


class ExtrapolationError(spack.error.FetchError):
    """Raised when we can't extrapolate a version for a package."""


class FetcherConflict(spack.error.FetchError):
    """Raised for packages with invalid fetch attributes."""


class InvalidArgsError(spack.error.FetchError):
    """Raised when a version can't be deduced from a set of arguments."""

    def __init__(self, pkg=None, version=None, **args):
        msg = "Could not guess a fetch strategy"
        if pkg:
            msg += " for {pkg}".format(pkg=pkg)
            if version:
                msg += "@{version}".format(version=version)
        long_msg = "with arguments: {args}".format(args=args)
        super().__init__(msg, long_msg)


class ChecksumError(spack.error.FetchError):
    """Raised when archive fails to checksum."""


class NoStageError(spack.error.FetchError):
    """Raised when fetch operations are called before set_stage()."""

    def __init__(self, method):
        super().__init__("Must call FetchStrategy.set_stage() before calling %s" % method.__name__)
