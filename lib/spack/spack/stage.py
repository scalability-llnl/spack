# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import errno
import getpass
import glob
import hashlib
import io
import os
import shutil
import stat
import sys
import tempfile
from typing import Callable, Dict, Generator, Iterable, List, Optional, Set

import llnl.string
import llnl.util.lang
import llnl.util.tty as tty
from llnl.util.filesystem import (
    can_access,
    get_owner_uid,
    getuid,
    install,
    install_tree,
    mkdirp,
    partition_path,
    remove_linked_tree,
)
from llnl.util.tty.colify import colify
from llnl.util.tty.color import colorize

import spack.caches
import spack.config
import spack.error
import spack.mirror
import spack.resource
import spack.spec
import spack.util.crypto
import spack.util.lock
import spack.util.parallel
import spack.util.path as sup
import spack.util.pattern as pattern
import spack.util.url as url_util
from spack import fetch_strategy as fs  # breaks a cycle
from spack.util.crypto import bit_length, prefix_bits
from spack.util.editor import editor, executable
from spack.version import StandardVersion, VersionList

# The well-known stage source subdirectory name.
_source_path_subdir = "spack-src"

# The temporary stage name prefix.
stage_prefix = "spack-stage-"


def compute_stage_name(spec):
    """Determine stage name given a spec"""
    default_stage_structure = stage_prefix + "{name}-{version}-{hash}"
    stage_name_structure = spack.config.get("config:stage_name", default=default_stage_structure)
    return spec.format_path(format_string=stage_name_structure)


def create_stage_root(path: str) -> None:
    """Create the stage root directory and ensure appropriate access perms."""
    assert os.path.isabs(path) and len(path.strip()) > 1

    err_msg = "Cannot create stage root {0}: Access to {1} is denied"

    user_uid = getuid()

    # Obtain lists of ancestor and descendant paths of the $user node, if any.
    group_paths, user_node, user_paths = partition_path(path, getpass.getuser())

    for p in group_paths:
        if not os.path.exists(p):
            # Ensure access controls of subdirs created above `$user` inherit
            # from the parent and share the group.
            par_stat = os.stat(os.path.dirname(p))
            mkdirp(p, group=par_stat.st_gid, mode=par_stat.st_mode)

            p_stat = os.stat(p)
            if par_stat.st_gid != p_stat.st_gid:
                tty.warn(
                    "Expected {0} to have group {1}, but it is {2}".format(
                        p, par_stat.st_gid, p_stat.st_gid
                    )
                )

            if par_stat.st_mode & p_stat.st_mode != par_stat.st_mode:
                tty.warn(
                    "Expected {0} to support mode {1}, but it is {2}".format(
                        p, par_stat.st_mode, p_stat.st_mode
                    )
                )

            if not can_access(p):
                raise OSError(errno.EACCES, err_msg.format(path, p))

    # Add the path ending with the $user node to the user paths to ensure paths
    # from $user (on down) meet the ownership and permission requirements.
    if user_node:
        user_paths.insert(0, user_node)

    for p in user_paths:
        # Ensure access controls of subdirs from `$user` on down are
        # restricted to the user.
        owner_uid = get_owner_uid(p)
        if user_uid != owner_uid:
            tty.warn(
                "Expected user {0} to own {1}, but it is owned by {2}".format(
                    user_uid, p, owner_uid
                )
            )

    spack_src_subdir = os.path.join(path, _source_path_subdir)
    # When staging into a user-specified directory with `spack stage -p <PATH>`, we need
    # to ensure the `spack-src` subdirectory exists, as we can't rely on it being
    # created automatically by spack. It's not clear why this is the case for `spack
    # stage -p`, but since `mkdirp()` is idempotent, this should not change the behavior
    # for any other code paths.
    if not os.path.isdir(spack_src_subdir):
        mkdirp(spack_src_subdir, mode=stat.S_IRWXU)


def _first_accessible_path(paths):
    """Find the first path that is accessible, creating it if necessary."""
    for path in paths:
        try:
            # Ensure the user has access, creating the directory if necessary.
            if os.path.exists(path):
                if can_access(path):
                    return path
            else:
                # Now create the stage root with the proper group/perms.
                create_stage_root(path)
                return path

        except OSError as e:
            tty.debug("OSError while checking stage path %s: %s" % (path, str(e)))

    return None


def _resolve_paths(candidates):
    """
    Resolve candidate paths and make user-related adjustments.

    Adjustments involve removing extra $user from $tempdir if $tempdir includes
    $user and appending $user if it is not present in the path.
    """
    temp_path = sup.canonicalize_path("$tempdir")
    user = getpass.getuser()
    tmp_has_usr = user in temp_path.split(os.path.sep)

    paths = []
    for path in candidates:
        # Remove the extra `$user` node from a `$tempdir/$user` entry for
        # hosts that automatically append `$user` to `$tempdir`.
        if path.startswith(os.path.join("$tempdir", "$user")) and tmp_has_usr:
            path = path.replace("/$user", "", 1)

        # Ensure the path is unique per user.
        can_path = sup.canonicalize_path(path)
        # When multiple users share a stage root, we can avoid conflicts between
        # them by adding a per-user subdirectory.
        # Avoid doing this on Windows to keep stage absolute path as short as possible.
        if user not in can_path and not sys.platform == "win32":
            can_path = os.path.join(can_path, user)

        paths.append(can_path)

    return paths


# Cached stage path root
_stage_root = None


def get_stage_root():
    global _stage_root

    if _stage_root is None:
        candidates = spack.config.get("config:build_stage")
        if isinstance(candidates, str):
            candidates = [candidates]

        resolved_candidates = _resolve_paths(candidates)
        path = _first_accessible_path(resolved_candidates)
        if not path:
            raise StageError("No accessible stage paths in:", " ".join(resolved_candidates))

        _stage_root = path

    return _stage_root


def _mirror_roots():
    mirrors = spack.config.get("mirrors")
    return [
        (
            sup.substitute_path_variables(root)
            if root.endswith(os.sep)
            else sup.substitute_path_variables(root) + os.sep
        )
        for root in mirrors.values()
    ]


class LockableStagingDir:
    """A directory whose lifetime can be managed with a context
    manager (but persists if the user requests it). Instances can have
    a specified name and if they do, then for all instances that have
    the same name, only one can enter the context manager at a time.
    """

    def __init__(self, name, path, keep, lock):
        # TODO: This uses a protected member of tempfile, but seemed the only
        # TODO: way to get a temporary name.  It won't be the same as the
        # TODO: temporary stage area in _stage_root.
        self.name = name
        if name is None:
            self.name = stage_prefix + next(tempfile._get_candidate_names())

        # Use the provided path or construct an optionally named stage path.
        if path is not None:
            self.path = path
        else:
            self.path = os.path.join(get_stage_root(), self.name)

        # Flag to decide whether to delete the stage folder on exit or not
        self.keep = keep

        # File lock for the stage directory.  We use one file for all
        # stage locks. See spack.database.Database.prefix_locker.lock for
        # details on this approach.
        self._lock = None
        self._use_locks = lock

        # When stages are reused, we need to know whether to re-create
        # it.  This marks whether it has been created/destroyed.
        self.created = False

    def _get_lock(self):
        if not self._lock:
            sha1 = hashlib.sha1(self.name.encode("utf-8")).digest()
            lock_id = prefix_bits(sha1, bit_length(sys.maxsize))
            stage_lock_path = os.path.join(get_stage_root(), ".lock")
            self._lock = spack.util.lock.Lock(
                stage_lock_path, start=lock_id, length=1, desc=self.name
            )
        return self._lock

    def __enter__(self):
        """
        Entering a stage context will create the stage directory

        Returns:
            self
        """
        if self._use_locks:
            self._get_lock().acquire_write(timeout=60)
        self.create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exiting from a stage context will delete the stage directory unless:
        - it was explicitly requested not to do so
        - an exception has been raised

        Args:
            exc_type: exception type
            exc_val: exception value
            exc_tb: exception traceback

        Returns:
            Boolean
        """
        # Delete when there are no exceptions, unless asked to keep.
        if exc_type is None and not self.keep:
            self.destroy()

        if self._use_locks:
            self._get_lock().release_write()

    def create(self):
        """
        Ensures the top-level (config:build_stage) directory exists.
        """
        # User has full permissions and group has only read permissions
        if not os.path.exists(self.path):
            mkdirp(self.path, mode=stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)
        elif not os.path.isdir(self.path):
            os.remove(self.path)
            mkdirp(self.path, mode=stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP)

        # Make sure we can actually do something with the stage we made.
        ensure_access(self.path)
        self.created = True

    def destroy(self):
        raise NotImplementedError(f"{self.__class__.__name__} is abstract")


class Stage(LockableStagingDir):
    """Manages a temporary stage directory for building.

    A Stage object is a context manager that handles a directory where
    some source code is downloaded and built before being installed.
    It handles fetching the source code, either as an archive to be
    expanded or by checking it out of a repository.  A stage's
    lifecycle looks like this::

        with Stage() as stage:      # Context manager creates and destroys the
                                    # stage directory
            stage.fetch()           # Fetch a source archive into the stage.
            stage.expand_archive()  # Expand the archive into source_path.
            <install>               # Build and install the archive.
                                    # (handled by user of Stage)

    When used as a context manager, the stage is automatically
    destroyed if no exception is raised by the context. If an
    excpetion is raised, the stage is left in the filesystem and NOT
    destroyed, for potential reuse later.

    You can also use the stage's create/destroy functions manually,
    like this::

        stage = Stage()
        try:
            stage.create()          # Explicitly create the stage directory.
            stage.fetch()           # Fetch a source archive into the stage.
            stage.expand_archive()  # Expand the archive into source_path.
            <install>               # Build and install the archive.
                                    # (handled by user of Stage)
        finally:
            stage.destroy()         # Explicitly destroy the stage directory.

    There are two kinds of stages: named and unnamed.  Named stages
    can persist between runs of spack, e.g. if you fetched a tarball
    but didn't finish building it, you won't have to fetch it again.

    Unnamed stages are created using standard mkdtemp mechanisms or
    similar, and are intended to persist for only one run of spack.
    """

    requires_patch_success = True

    def __init__(
        self,
        url_or_fetch_strategy,
        *,
        name=None,
        mirror_paths: Optional["spack.mirror.MirrorLayout"] = None,
        mirrors: Optional[Iterable["spack.mirror.Mirror"]] = None,
        keep=False,
        path=None,
        lock=True,
        search_fn=None,
    ):
        """Create a stage object.
        Parameters:
          url_or_fetch_strategy
              URL of the archive to be downloaded into this stage, OR a valid FetchStrategy.

          name
              If a name is provided, then this stage is a named stage and will persist between runs
              (or if you construct another stage object later).  If name is not provided, then this
              stage will be given a unique name automatically.

          mirror_paths
              If provided, Stage will search Spack's mirrors for this archive at each of the
              provided relative mirror paths before using the default fetch strategy.

          keep
              By default, when used as a context manager, the Stage is deleted on exit when no
              exceptions are raised. Pass True to keep the stage intact even if no exceptions are
              raised.

         path
              If provided, the stage path to use for associated builds.

         lock
              True if the stage directory file lock is to be used, False otherwise.

         search_fn
              The search function that provides the fetch strategy instance.
        """
        super().__init__(name, path, keep, lock)

        # TODO: fetch/stage coupling needs to be reworked -- the logic
        # TODO: here is convoluted and not modular enough.
        if isinstance(url_or_fetch_strategy, str):
            self.fetcher = fs.from_url_scheme(url_or_fetch_strategy)
        elif isinstance(url_or_fetch_strategy, fs.FetchStrategy):
            self.fetcher = url_or_fetch_strategy
        else:
            raise ValueError("Can't construct Stage without url or fetch strategy")
        self.fetcher.stage = self
        # self.fetcher can change with mirrors.
        self.default_fetcher = self.fetcher
        self.search_fn = search_fn
        # If we fetch from a mirror, but the original data is from say git, we can currently not
        # prove that they are equal (we don't even have a tree hash in package.py). This bool is
        # used to skip checksum verification and instead warn the user.
        if isinstance(self.default_fetcher, fs.URLFetchStrategy):
            self.skip_checksum_for_mirror = not bool(self.default_fetcher.digest)
        else:
            self.skip_checksum_for_mirror = True

        self.srcdir = None

        self.mirror_layout = mirror_paths
        self.mirrors = list(mirrors) if mirrors else []
        # Allow users the disable both mirrors and download cache
        self.default_fetcher_only = False

    @property
    def expected_archive_files(self):
        """Possible archive file paths."""
        fnames = []
        expanded = True
        if isinstance(self.default_fetcher, fs.URLFetchStrategy):
            expanded = self.default_fetcher.expand_archive
            fnames.append(url_util.default_download_filename(self.default_fetcher.url))

        if self.mirror_layout:
            fnames.append(os.path.basename(self.mirror_layout.path))

        paths = [os.path.join(self.path, f) for f in fnames]
        if not expanded:
            # If the download file is not compressed, the "archive" is a single file placed in
            # Stage.source_path
            paths.extend(os.path.join(self.source_path, f) for f in fnames)

        return paths

    @property
    def save_filename(self):
        possible_filenames = self.expected_archive_files
        if possible_filenames:
            # This prefers using the URL associated with the default fetcher if
            # available, so that the fetched resource name matches the remote
            # name
            return possible_filenames[0]

    @property
    def archive_file(self):
        """Path to the source archive within this stage directory."""
        for path in self.expected_archive_files:
            if os.path.exists(path):
                return path
        else:
            return None

    @property
    def expanded(self):
        """Returns True if source path expanded; else False."""
        return os.path.exists(self.source_path)

    @property
    def source_path(self):
        """Returns the well-known source directory path."""
        return os.path.join(self.path, _source_path_subdir)

    def _generate_fetchers(self, mirror_only=False) -> Generator["fs.FetchStrategy", None, None]:
        fetchers: List[fs.FetchStrategy] = []
        if not mirror_only:
            fetchers.append(self.default_fetcher)

        # If this archive is normally fetched from a URL, then use the same digest.
        if isinstance(self.default_fetcher, fs.URLFetchStrategy):
            digest = self.default_fetcher.digest
            expand = self.default_fetcher.expand_archive
            extension = self.default_fetcher.extension
        else:
            digest = None
            expand = True
            extension = None

        # TODO: move mirror logic out of here and clean it up!
        # TODO: Or @alalazo may have some ideas about how to use a
        # TODO: CompositeFetchStrategy here.
        if not self.default_fetcher_only and self.mirror_layout and self.mirrors:
            # Add URL strategies for all the mirrors with the digest
            # Insert fetchers in the order that the URLs are provided.
            fetchers[:0] = (
                fs.from_url_scheme(
                    url_util.join(mirror.fetch_url, self.mirror_layout.path),
                    checksum=digest,
                    expand=expand,
                    extension=extension,
                )
                for mirror in self.mirrors
                if not mirror.fetch_url.startswith("oci://")  # no support for mirrors yet
            )

        if not self.default_fetcher_only and self.mirror_layout and self.default_fetcher.cachable:
            fetchers.insert(
                0,
                spack.caches.FETCH_CACHE.fetcher(
                    self.mirror_layout.path, digest, expand=expand, extension=extension
                ),
            )

        yield from fetchers

        # The search function may be expensive, so wait until now to call it so the user can stop
        # if a prior fetcher succeeded
        if self.search_fn and not mirror_only:
            yield from self.search_fn()

    def fetch(self, mirror_only: bool = False, err_msg: Optional[str] = None) -> None:
        """Retrieves the code or archive

        Args:
            mirror_only: only fetch from a mirror
            err_msg: the error message to display if all fetchers fail or ``None`` for the default
                fetch failure message
        """
        errors: List[str] = []
        for fetcher in self._generate_fetchers(mirror_only):
            try:
                fetcher.stage = self
                self.fetcher = fetcher
                self.fetcher.fetch()
                break
            except fs.NoCacheError:
                # Don't bother reporting when something is not cached.
                continue
            except fs.FailedDownloadError as f:
                errors.extend(f"{fetcher}: {e.__class__.__name__}: {e}" for e in f.exceptions)
                continue
            except spack.error.SpackError as e:
                errors.append(f"{fetcher}: {e.__class__.__name__}: {e}")
                continue
        else:
            self.fetcher = self.default_fetcher
            if err_msg:
                raise spack.error.FetchError(err_msg)
            raise spack.error.FetchError(
                f"All fetchers failed for {self.name}", "\n".join(f"    {e}" for e in errors)
            )

    def steal_source(self, dest):
        """Copy the source_path directory in its entirety to directory dest

        This operation creates/fetches/expands the stage if it is not already,
        and destroys the stage when it is done."""
        if not self.created:
            self.create()
        if not self.expanded and not self.archive_file:
            self.fetch()
        if not self.expanded:
            self.expand_archive()

        if not os.path.isdir(dest):
            mkdirp(dest)

        # glob all files and directories in the source path
        hidden_entries = glob.glob(os.path.join(self.source_path, ".*"))
        entries = glob.glob(os.path.join(self.source_path, "*"))

        # Move all files from stage to destination directory
        # Include hidden files for VCS repo history
        for entry in hidden_entries + entries:
            if os.path.isdir(entry):
                d = os.path.join(dest, os.path.basename(entry))
                shutil.copytree(entry, d, symlinks=True)
            else:
                shutil.copy2(entry, dest)

        # copy archive file if we downloaded from url -- replaces for vcs
        if self.archive_file and os.path.exists(self.archive_file):
            shutil.copy2(self.archive_file, dest)

        # remove leftover stage
        self.destroy()

    def check(self):
        """Check the downloaded archive against a checksum digest."""
        if self.fetcher is not self.default_fetcher and self.skip_checksum_for_mirror:
            cache = isinstance(self.fetcher, fs.CacheURLFetchStrategy)
            if cache:
                secure_msg = "your download cache is in a secure location"
            else:
                secure_msg = "you trust this mirror and have a secure connection"
            tty.warn(
                f"Using {'download cache' if cache else 'a mirror'} instead of version control",
                "The required sources are normally checked out from a version control system, "
                f"but have been archived {'in download cache' if cache else 'on a mirror'}: "
                f"{self.fetcher}. Spack lacks a tree hash to verify the integrity of this "
                f"archive. Make sure {secure_msg}.",
            )
        elif spack.config.get("config:checksum"):
            self.fetcher.check()

    def cache_local(self):
        spack.caches.FETCH_CACHE.store(self.fetcher, self.mirror_layout.path)

    def cache_mirror(
        self, mirror: "spack.caches.MirrorCache", stats: "spack.mirror.MirrorStats"
    ) -> None:
        """Perform a fetch if the resource is not already cached

        Arguments:
            mirror: the mirror to cache this Stage's resource in
            stats: this is updated depending on whether the caching operation succeeded or failed
        """
        if isinstance(self.default_fetcher, fs.BundleFetchStrategy):
            # BundleFetchStrategy has no source to fetch. The associated fetcher does nothing but
            # the associated stage may still exist. There is currently no method available on the
            # fetcher to distinguish this ('cachable' refers to whether the fetcher refers to a
            # resource with a fixed ID, which is not the same concept as whether there is anything
            # to fetch at all) so we must examine the type of the fetcher.
            return

        elif mirror.skip_unstable_versions and not fs.stable_target(self.default_fetcher):
            return

        elif not self.mirror_layout:
            return

        absolute_storage_path = os.path.join(mirror.root, self.mirror_layout.path)

        if os.path.exists(absolute_storage_path):
            stats.already_existed(absolute_storage_path)
        else:
            self.fetch()
            self.check()
            mirror.store(self.fetcher, self.mirror_layout.path)
            stats.added(absolute_storage_path)

        self.mirror_layout.make_alias(mirror.root)

    def expand_archive(self):
        """Changes to the stage directory and attempt to expand the downloaded
        archive.  Fail if the stage is not set up or if the archive is not yet
        downloaded."""
        if not self.expanded:
            self.fetcher.expand()
            tty.debug(f"Created stage in {self.path}")
        else:
            tty.debug(f"Already staged {self.name} in {self.path}")

    def restage(self):
        """Removes the expanded archive path if it exists, then re-expands
        the archive.
        """
        self.fetcher.reset()

    def destroy(self):
        """Removes this stage directory."""
        remove_linked_tree(self.path)

        # Make sure we don't end up in a removed directory
        try:
            os.getcwd()
        except OSError as e:
            tty.debug(e)
            os.chdir(os.path.dirname(self.path))

        # mark as destroyed
        self.created = False


class ResourceStage(Stage):
    def __init__(
        self,
        fetch_strategy: "fs.FetchStrategy",
        root: Stage,
        resource: spack.resource.Resource,
        **kwargs,
    ):
        super().__init__(fetch_strategy, **kwargs)
        self.root_stage = root
        self.resource = resource

    def restage(self):
        super().restage()
        self._add_to_root_stage()

    def expand_archive(self):
        super().expand_archive()
        self._add_to_root_stage()

    def _add_to_root_stage(self):
        """
        Move the extracted resource to the root stage (according to placement).
        """
        root_stage = self.root_stage
        resource = self.resource

        if resource.placement:
            placement = resource.placement
        elif self.srcdir:
            placement = self.srcdir
        else:
            placement = self.source_path

        if not isinstance(placement, dict):
            placement = {"": placement}

        target_path = os.path.join(root_stage.source_path, resource.destination)

        try:
            os.makedirs(target_path)
        except OSError as err:
            tty.debug(err)
            if err.errno == errno.EEXIST and os.path.isdir(target_path):
                pass
            else:
                raise

        for key, value in placement.items():
            destination_path = os.path.join(target_path, value)
            source_path = os.path.join(self.source_path, key)

            if not os.path.exists(destination_path):
                tty.info(
                    "Moving resource stage\n\tsource: "
                    "{stage}\n\tdestination: {destination}".format(
                        stage=source_path, destination=destination_path
                    )
                )

                src = os.path.realpath(source_path)

                if os.path.isdir(src):
                    install_tree(src, destination_path)
                else:
                    install(src, destination_path)


class StageComposite(pattern.Composite):
    """Composite for Stage type objects. The first item in this composite is
    considered to be the root package, and operations that return a value are
    forwarded to it."""

    #
    # __enter__ and __exit__ delegate to all stages in the composite.
    #

    def __init__(self):
        super().__init__(
            [
                "fetch",
                "create",
                "created",
                "check",
                "expand_archive",
                "restage",
                "destroy",
                "cache_local",
                "cache_mirror",
                "steal_source",
                "disable_mirrors",
            ]
        )

    @classmethod
    def from_iterable(cls, iterable: Iterable[Stage]) -> "StageComposite":
        """Create a new composite from an iterable of stages."""
        composite = cls()
        composite.extend(iterable)
        return composite

    def __enter__(self):
        for item in self:
            item.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for item in reversed(self):
            item.__exit__(exc_type, exc_val, exc_tb)

    #
    # Below functions act only on the *first* stage in the composite.
    #
    @property
    def source_path(self):
        return self[0].source_path

    @property
    def expanded(self):
        return self[0].expanded

    @property
    def path(self):
        return self[0].path

    @property
    def archive_file(self):
        return self[0].archive_file

    @property
    def requires_patch_success(self):
        return self[0].requires_patch_success

    @property
    def keep(self):
        return self[0].keep

    @keep.setter
    def keep(self, value):
        for item in self:
            item.keep = value


class DevelopStage(LockableStagingDir):
    requires_patch_success = False

    def __init__(self, name, dev_path, reference_link):
        super().__init__(name=name, path=None, keep=False, lock=True)
        self.dev_path = dev_path
        self.source_path = dev_path

        # The path of a link that will point to this stage
        if os.path.isabs(reference_link):
            link_path = reference_link
        else:
            link_path = os.path.join(self.source_path, reference_link)
        if not os.path.isdir(os.path.dirname(link_path)):
            raise StageError(f"The directory containing {link_path} must exist")
        self.reference_link = link_path

    @property
    def archive_file(self):
        return None

    def fetch(self, *args, **kwargs):
        tty.debug("No fetching needed for develop stage.")

    def check(self):
        tty.debug("No checksum needed for develop stage.")

    def expand_archive(self):
        tty.debug("No expansion needed for develop stage.")

    @property
    def expanded(self):
        """Returns True since the source_path must exist."""
        return True

    def create(self):
        super().create()
        try:
            llnl.util.symlink.symlink(self.path, self.reference_link)
        except (llnl.util.symlink.AlreadyExistsError, FileExistsError):
            pass

    def destroy(self):
        # Destroy all files, but do not follow symlinks
        try:
            shutil.rmtree(self.path)
        except FileNotFoundError:
            pass
        try:
            os.remove(self.reference_link)
        except FileNotFoundError:
            pass
        self.created = False

    def restage(self):
        self.destroy()
        self.create()

    def cache_local(self):
        tty.debug("Sources for Develop stages are not cached")


def ensure_access(file):
    """Ensure we can access a directory and die with an error if we can't."""
    if not can_access(file):
        tty.die("Insufficient permissions for %s" % file)


def purge():
    """Remove all build directories in the top-level stage path."""
    root = get_stage_root()
    if os.path.isdir(root):
        for stage_dir in os.listdir(root):
            if stage_dir.startswith(stage_prefix) or stage_dir == ".lock":
                stage_path = os.path.join(root, stage_dir)
                if os.path.isdir(stage_path):
                    remove_linked_tree(stage_path)
                else:
                    os.remove(stage_path)


def interactive_version_filter(
    url_dict: Dict[StandardVersion, str],
    known_versions: Iterable[StandardVersion] = (),
    *,
    initial_verion_filter: Optional[VersionList] = None,
    url_changes: Set[StandardVersion] = set(),
    input: Callable[..., str] = input,
) -> Optional[Dict[StandardVersion, str]]:
    """Interactively filter the list of spidered versions.

    Args:
        url_dict: Dictionary of versions to URLs
        known_versions: Versions that can be skipped because they are already known

    Returns:
        Filtered dictionary of versions to URLs or None if the user wants to quit
    """
    # Find length of longest string in the list for padding
    version_filter = initial_verion_filter or VersionList([":"])
    max_len = max(len(str(v)) for v in url_dict) if url_dict else 0
    sorted_and_filtered = [v for v in url_dict if v.satisfies(version_filter)]
    sorted_and_filtered.sort(reverse=True)
    orig_url_dict = url_dict  # only copy when using editor to modify
    print_header = True
    VERSION_COLOR = spack.spec.VERSION_COLOR
    while True:
        if print_header:
            has_filter = version_filter != VersionList([":"])
            header = []
            if len(orig_url_dict) > 0 and len(sorted_and_filtered) == len(orig_url_dict):
                header.append(
                    f"Selected {llnl.string.plural(len(sorted_and_filtered), 'version')}"
                )
            else:
                header.append(
                    f"Selected {len(sorted_and_filtered)} of "
                    f"{llnl.string.plural(len(orig_url_dict), 'version')}"
                )
            if sorted_and_filtered and known_versions:
                num_new = sum(1 for v in sorted_and_filtered if v not in known_versions)
                header.append(f"{llnl.string.plural(num_new, 'new version')}")
            if has_filter:
                header.append(colorize(f"Filtered by {VERSION_COLOR}@@{version_filter}@."))

            version_with_url = [
                colorize(
                    f"{VERSION_COLOR}{str(v):{max_len}}@.  {url_dict[v]}"
                    f"{'  @K{# NOTE: change of URL}' if v in url_changes else ''}"
                )
                for v in sorted_and_filtered
            ]
            tty.msg(". ".join(header), *llnl.util.lang.elide_list(version_with_url))
            print()

        print_header = True

        tty.info(colorize("Enter @*{number} of versions to take, or use a @*{command}:"))
        commands = (
            "@*b{[c]}hecksum",
            "@*b{[e]}dit",
            "@*b{[f]}ilter",
            "@*b{[a]}sk each",
            "@*b{[n]}ew only",
            "@*b{[r]}estart",
            "@*b{[q]}uit",
        )
        colify(list(map(colorize, commands)), indent=4)

        try:
            command = input(colorize("@*g{action>} ")).strip().lower()
        except EOFError:
            print()
            command = "q"

        if command == "c":
            break
        elif command == "e":
            # Create a temporary file in the stage dir with lines of the form
            # <version> <url>
            # which the user can modify. Once the editor is closed, the file is
            # read back in and the versions to url dict is updated.

            # Create a temporary file by hashing its contents.
            buffer = io.StringIO()
            buffer.write("# Edit this file to change the versions and urls to fetch\n")
            for v in sorted_and_filtered:
                buffer.write(f"{str(v):{max_len}}  {url_dict[v]}\n")
            data = buffer.getvalue().encode("utf-8")

            short_hash = hashlib.sha1(data).hexdigest()[:7]
            filename = f"{stage_prefix}versions-{short_hash}.txt"
            filepath = os.path.join(get_stage_root(), filename)

            # Write contents
            with open(filepath, "wb") as f:
                f.write(data)

            # Open editor
            editor(filepath, exec_fn=executable)

            # Read back in
            with open(filepath, "r") as f:
                orig_url_dict, url_dict = url_dict, {}
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith("#"):
                        continue
                    try:
                        version, url = line.split(None, 1)
                    except ValueError:
                        tty.warn(f"Couldn't parse: {line}")
                        continue
                    try:
                        url_dict[StandardVersion.from_string(version)] = url
                    except ValueError:
                        tty.warn(f"Invalid version: {version}")
                        continue
                sorted_and_filtered = sorted(url_dict.keys(), reverse=True)

            os.unlink(filepath)
        elif command == "f":
            tty.msg(
                colorize(
                    f"Examples filters: {VERSION_COLOR}1.2@. "
                    f"or {VERSION_COLOR}1.1:1.3@. "
                    f"or {VERSION_COLOR}=1.2, 1.2.2:@."
                )
            )
            try:
                # Allow a leading @ version specifier
                filter_spec = input(colorize("@*g{filter>} ")).strip().lstrip("@")
            except EOFError:
                print()
                continue
            try:
                version_filter.intersect(VersionList([filter_spec]))
            except ValueError:
                tty.warn(f"Invalid version specifier: {filter_spec}")
                continue
            # Apply filter
            sorted_and_filtered = [v for v in sorted_and_filtered if v.satisfies(version_filter)]
        elif command == "a":
            i = 0
            while i < len(sorted_and_filtered):
                v = sorted_and_filtered[i]
                try:
                    answer = input(f"  {str(v):{max_len}}  {url_dict[v]} [Y/n]? ").strip().lower()
                except EOFError:
                    # If ^D, don't fully exit, but go back to the command prompt, now with possibly
                    # fewer versions
                    print()
                    break
                if answer in ("n", "no"):
                    del sorted_and_filtered[i]
                elif answer in ("y", "yes", ""):
                    i += 1
            else:
                # Went over each version, so go to checksumming
                break
        elif command == "n":
            sorted_and_filtered = [v for v in sorted_and_filtered if v not in known_versions]
        elif command == "r":
            url_dict = orig_url_dict
            sorted_and_filtered = sorted(url_dict.keys(), reverse=True)
            version_filter = VersionList([":"])
        elif command == "q":
            try:
                if input("Really quit [y/N]? ").strip().lower() in ("y", "yes"):
                    return None
            except EOFError:
                print()
                return None
        else:
            # Last restort: filter the top N versions
            try:
                n = int(command)
                invalid_command = n < 1
            except ValueError:
                invalid_command = True

            if invalid_command:
                tty.warn(f"Ignoring invalid command: {command}")
                print_header = False
                continue

            sorted_and_filtered = sorted_and_filtered[:n]

    return {v: url_dict[v] for v in sorted_and_filtered}


def get_checksums_for_versions(
    url_by_version: Dict[StandardVersion, str],
    package_name: str,
    *,
    first_stage_function: Optional[Callable[[Stage, str], None]] = None,
    keep_stage: bool = False,
    concurrency: Optional[int] = None,
    fetch_options: Optional[Dict[str, str]] = None,
) -> Dict[StandardVersion, str]:
    """Computes the checksums for each version passed in input, and returns the results.

    Archives are fetched according to the usl dictionary passed as input.

    The ``first_stage_function`` argument allows the caller to inspect the first downloaded
    archive, e.g., to determine the build system.

    Args:
        url_by_version: URL keyed by version
        package_name: name of the package
        first_stage_function: function that takes a Stage and a URL; this is run on the stage
            of the first URL downloaded
        keep_stage: whether to keep staging area when command completes
        batch: whether to ask user how many versions to fetch (false) or fetch all versions (true)
        fetch_options: options used for the fetcher (such as timeout or cookies)
        concurrency: maximum number of workers to use for retrieving archives

    Returns:
        A dictionary mapping each version to the corresponding checksum
    """
    versions = sorted(url_by_version.keys(), reverse=True)
    search_arguments = [(url_by_version[v], v) for v in versions]

    version_hashes, errors = {}, []

    # Don't spawn 16 processes when we need to fetch 2 urls
    if concurrency is not None:
        concurrency = min(concurrency, len(search_arguments))
    else:
        concurrency = min(os.cpu_count() or 1, len(search_arguments))

    # The function might have side effects in memory, that would not be reflected in the
    # parent process, if run in a child process. If this pattern happens frequently, we
    # can move this function call *after* having distributed the work to executors.
    if first_stage_function is not None:
        (url, version), search_arguments = search_arguments[0], search_arguments[1:]
        checksum, error = _fetch_and_checksum(url, fetch_options, keep_stage, first_stage_function)
        if error is not None:
            errors.append(error)

        if checksum is not None:
            version_hashes[version] = checksum

    with spack.util.parallel.make_concurrent_executor(concurrency, require_fork=False) as executor:
        results = []
        for url, version in search_arguments:
            future = executor.submit(_fetch_and_checksum, url, fetch_options, keep_stage)
            results.append((version, future))

        for version, future in results:
            checksum, error = future.result()
            if error is not None:
                errors.append(error)
                continue
            version_hashes[version] = checksum

        for msg in errors:
            tty.debug(msg)

    if not version_hashes:
        tty.die(f"Could not fetch any versions for {package_name}")

    num_hash = len(version_hashes)
    tty.debug(f"Checksummed {num_hash} version{'' if num_hash == 1 else 's'} of {package_name}:")

    return version_hashes


def _fetch_and_checksum(url, options, keep_stage, action_fn=None):
    try:
        url_or_fs = url
        if options:
            url_or_fs = fs.URLFetchStrategy(url=url, fetch_options=options)

        with Stage(url_or_fs, keep=keep_stage) as stage:
            # Fetch the archive
            stage.fetch()
            archive = stage.archive_file
            assert archive is not None, f"Archive not found for {url}"
            if action_fn is not None and archive:
                # Only run first_stage_function the first time,
                # no need to run it every time
                action_fn(archive, url)

            # Checksum the archive and add it to the list
            checksum = spack.util.crypto.checksum(hashlib.sha256, archive)
        return checksum, None
    except fs.FailedDownloadError:
        return None, f"[WORKER] Failed to fetch {url}"
    except Exception as e:
        return None, f"[WORKER] Something failed on {url}, skipping.  ({e})"


class StageError(spack.error.SpackError):
    """ "Superclass for all errors encountered during staging."""


class StagePathError(StageError):
    """ "Error encountered with stage path."""


class RestageError(StageError):
    """ "Error encountered during restaging."""


class VersionFetchError(StageError):
    """Raised when we can't determine a URL to fetch a package."""
