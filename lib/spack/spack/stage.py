# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import os
import stat
import sys
import errno
import hashlib
import tempfile
import getpass
from six import string_types
from six import iteritems

import llnl.util.tty as tty
from llnl.util.filesystem import mkdirp, can_access, install, install_tree
from llnl.util.filesystem import partition_path, remove_linked_tree

import spack.paths
import spack.caches
import spack.cmd
import spack.config
import spack.error
import spack.mirror
import spack.util.lock
import spack.fetch_strategy as fs
import spack.util.pattern as pattern
import spack.util.path as sup
import spack.util.url as url_util

from spack.util.crypto import prefix_bits, bit_length


# The well-known stage source subdirectory name.
_source_path_subdir = 'spack-src'

# The temporary stage name prefix.
stage_prefix = 'spack-stage-'


def _create_stage_root(path):
    """Create the stage root directory and ensure appropriate access perms."""
    assert path.startswith(os.path.sep) and len(path.strip()) > 1

    err_msg = 'Cannot create stage root {0}: Access to {1} is denied'

    user_uid = os.getuid()

    # Obtain lists of ancestor and descendant paths of the $user node, if any.
    group_paths, user_node, user_paths = partition_path(path,
                                                        getpass.getuser())

    for p in group_paths:
        if not os.path.exists(p):
            # Ensure access controls of subdirs created above `$user` inherit
            # from the parent and share the group.
            par_stat = os.stat(os.path.dirname(p))
            mkdirp(p, group=par_stat.st_gid, mode=par_stat.st_mode)

            p_stat = os.stat(p)
            if par_stat.st_gid != p_stat.st_gid:
                tty.warn("Expected {0} to have group {1}, but it is {2}"
                         .format(p, par_stat.st_gid, p_stat.st_gid))

            if par_stat.st_mode & p_stat.st_mode != par_stat.st_mode:
                tty.warn("Expected {0} to support mode {1}, but it is {2}"
                         .format(p, par_stat.st_mode, p_stat.st_mode))

            if not can_access(p):
                raise OSError(errno.EACCES, err_msg.format(path, p))

    # Add the path ending with the $user node to the user paths to ensure paths
    # from $user (on down) meet the ownership and permission requirements.
    if user_node:
        user_paths.insert(0, user_node)

    for p in user_paths:
        # Ensure access controls of subdirs from `$user` on down are
        # restricted to the user.
        if not os.path.exists(p):
            mkdirp(p, mode=stat.S_IRWXU)

            p_stat = os.stat(p)
            if p_stat.st_mode & stat.S_IRWXU != stat.S_IRWXU:
                tty.error("Expected {0} to support mode {1}, but it is {2}"
                          .format(p, stat.S_IRWXU, p_stat.st_mode))

                raise OSError(errno.EACCES, err_msg.format(path, p))
        else:
            p_stat = os.stat(p)

        if user_uid != p_stat.st_uid:
            tty.warn("Expected user {0} to own {1}, but it is owned by {2}"
                     .format(user_uid, p, p_stat.st_uid))


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
                _create_stage_root(path)
                return path

        except OSError as e:
            tty.debug('OSError while checking stage path %s: %s' % (
                      path, str(e)))

    return None


def _resolve_paths(candidates):
    """
    Resolve candidate paths and make user-related adjustments.

    Adjustments involve removing extra $user from $tempdir if $tempdir includes
    $user and appending $user if it is not present in the path.
    """
    temp_path = sup.canonicalize_path('$tempdir')
    user = getpass.getuser()
    tmp_has_usr = user in temp_path.split(os.path.sep)

    paths = []
    for path in candidates:
        # Remove the extra `$user` node from a `$tempdir/$user` entry for
        # hosts that automatically append `$user` to `$tempdir`.
        if path.startswith(os.path.join('$tempdir', '$user')) and tmp_has_usr:
            path = path.replace("/$user", "", 1)

        # Ensure the path is unique per user.
        can_path = sup.canonicalize_path(path)
        if user not in can_path:
            can_path = os.path.join(can_path, user)

        paths.append(can_path)

    return paths


# Cached stage path root
_stage_root = None


def get_stage_root():
    global _stage_root

    if _stage_root is None:
        candidates = spack.config.get('config:build_stage')

        if isinstance(candidates, string_types):
            candidates = [candidates]

        resolved_candidates = _resolve_paths(candidates)
        path = _first_accessible_path(resolved_candidates)
        if not path:
            raise StageError("No accessible stage paths in:",
                             ' '.join(resolved_candidates))

        _stage_root = path

    return _stage_root


def _mirror_roots():
    mirrors = spack.config.get('mirrors')
    return [
        sup.substitute_path_variables(root) if root.endswith(os.sep)
        else sup.substitute_path_variables(root) + os.sep
        for root in mirrors.values()]


class Stage(object):
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

    """Shared dict of all stage locks."""
    stage_locks = {}

    """Most staging is managed by Spack.  DIYStage is one exception."""
    managed_by_spack = True

    def __init__(
            self, url_or_fetch_strategy,
            name=None, mirror_paths=None, keep=False, path=None, lock=True,
            search_fn=None):
        """Create a stage object.
           Parameters:
             url_or_fetch_strategy
                 URL of the archive to be downloaded into this stage, OR
                 a valid FetchStrategy.

             name
                 If a name is provided, then this stage is a named stage
                 and will persist between runs (or if you construct another
                 stage object later).  If name is not provided, then this
                 stage will be given a unique name automatically.

             mirror_paths
                 If provided, Stage will search Spack's mirrors for
                 this archive at each of the provided relative mirror paths
                 before using the default fetch strategy.

             keep
                 By default, when used as a context manager, the Stage
                 is deleted on exit when no exceptions are raised.
                 Pass True to keep the stage intact even if no
                 exceptions are raised.

            path
                 If provided, the stage path to use for associated builds.

            lock
                 True if the stage directory file lock is to be used, False
                 otherwise.

            search_fn
                 The search function that provides the fetch strategy
                 instance.
        """
        # TODO: fetch/stage coupling needs to be reworked -- the logic
        # TODO: here is convoluted and not modular enough.
        if isinstance(url_or_fetch_strategy, string_types):
            self.fetcher = fs.from_url_scheme(url_or_fetch_strategy)
        elif isinstance(url_or_fetch_strategy, fs.FetchStrategy):
            self.fetcher = url_or_fetch_strategy
        else:
            raise ValueError(
                "Can't construct Stage without url or fetch strategy")
        self.fetcher.stage = self
        # self.fetcher can change with mirrors.
        self.default_fetcher = self.fetcher
        self.search_fn = search_fn
        # used for mirrored archives of repositories.
        self.skip_checksum_for_mirror = True

        self.srcdir = None

        # TODO: This uses a protected member of tempfile, but seemed the only
        # TODO: way to get a temporary name.  It won't be the same as the
        # TODO: temporary stage area in _stage_root.
        self.name = name
        if name is None:
            self.name = stage_prefix + next(tempfile._get_candidate_names())
        self.mirror_paths = mirror_paths

        # Use the provided path or construct an optionally named stage path.
        if path is not None:
            self.path = path
        else:
            self.path = os.path.join(get_stage_root(), self.name)

        # Flag to decide whether to delete the stage folder on exit or not
        self.keep = keep

        # File lock for the stage directory.  We use one file for all
        # stage locks. See spack.database.Database.prefix_lock for
        # details on this approach.
        self._lock = None
        if lock:
            if self.name not in Stage.stage_locks:
                sha1 = hashlib.sha1(self.name.encode('utf-8')).digest()
                lock_id = prefix_bits(sha1, bit_length(sys.maxsize))
                stage_lock_path = os.path.join(get_stage_root(), '.lock')

                tty.debug("Creating stage lock {0}".format(self.name))
                Stage.stage_locks[self.name] = spack.util.lock.Lock(
                    stage_lock_path, lock_id, 1, desc=self.name)

            self._lock = Stage.stage_locks[self.name]

        # When stages are reused, we need to know whether to re-create
        # it.  This marks whether it has been created/destroyed.
        self.created = False

    def __enter__(self):
        """
        Entering a stage context will create the stage directory

        Returns:
            self
        """
        if self._lock is not None:
            self._lock.acquire_write(timeout=60)
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

        if self._lock is not None:
            self._lock.release_write()

    @property
    def expected_archive_files(self):
        """Possible archive file paths."""
        paths = []

        fnames = []
        expanded = True
        if isinstance(self.default_fetcher, fs.URLFetchStrategy):
            expanded = self.default_fetcher.expand_archive
            fnames.append(os.path.basename(self.default_fetcher.url))

        if self.mirror_paths:
            fnames.extend(os.path.basename(x) for x in self.mirror_paths)

        paths.extend(os.path.join(self.path, f) for f in fnames)
        if not expanded:
            # If the download file is not compressed, the "archive" is a
            # single file placed in Stage.source_path
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

    def fetch(self, mirror_only=False):
        """Downloads an archive or checks out code from a repository."""
        fetchers = []
        if not mirror_only:
            fetchers.append(self.default_fetcher)

        # TODO: move mirror logic out of here and clean it up!
        # TODO: Or @alalazo may have some ideas about how to use a
        # TODO: CompositeFetchStrategy here.
        self.skip_checksum_for_mirror = True
        if self.mirror_paths:
            # Join URLs of mirror roots with mirror paths. Because
            # urljoin() will strip everything past the final '/' in
            # the root, so we add a '/' if it is not present.
            urls = []
            for mirror in spack.mirror.MirrorCollection().values():
                for rel_path in self.mirror_paths:
                    urls.append(url_util.join(mirror.fetch_url, rel_path))

            # If this archive is normally fetched from a tarball URL,
            # then use the same digest.  `spack mirror` ensures that
            # the checksum will be the same.
            digest = None
            expand = True
            extension = None
            if isinstance(self.default_fetcher, fs.URLFetchStrategy):
                digest = self.default_fetcher.digest
                expand = self.default_fetcher.expand_archive
                extension = self.default_fetcher.extension

            # Have to skip the checksum for things archived from
            # repositories.  How can this be made safer?
            self.skip_checksum_for_mirror = not bool(digest)

            # Add URL strategies for all the mirrors with the digest
            for url in urls:
                fetchers.insert(
                    0, fs.from_url_scheme(
                        url, digest, expand=expand, extension=extension))

            if self.default_fetcher.cachable:
                for rel_path in reversed(list(self.mirror_paths)):
                    cache_fetcher = spack.caches.fetch_cache.fetcher(
                        rel_path, digest, expand=expand,
                        extension=extension)
                    fetchers.insert(0, cache_fetcher)

        def generate_fetchers():
            for fetcher in fetchers:
                yield fetcher
            # The search function may be expensive, so wait until now to
            # call it so the user can stop if a prior fetcher succeeded
            if self.search_fn and not mirror_only:
                dynamic_fetchers = self.search_fn()
                for fetcher in dynamic_fetchers:
                    yield fetcher

        for fetcher in generate_fetchers():
            try:
                fetcher.stage = self
                self.fetcher = fetcher
                self.fetcher.fetch()
                break
            except spack.fetch_strategy.NoCacheError:
                # Don't bother reporting when something is not cached.
                continue
            except spack.error.SpackError as e:
                tty.msg("Fetching from %s failed." % fetcher)
                tty.debug(e)
                continue
        else:
            err_msg = "All fetchers failed for %s" % self.name
            self.fetcher = self.default_fetcher
            raise fs.FetchError(err_msg, None)

    def check(self):
        """Check the downloaded archive against a checksum digest.
           No-op if this stage checks code out of a repository."""
        if self.fetcher is not self.default_fetcher and \
           self.skip_checksum_for_mirror:
            tty.warn("Fetching from mirror without a checksum!",
                     "This package is normally checked out from a version "
                     "control system, but it has been archived on a spack "
                     "mirror.  This means we cannot know a checksum for the "
                     "tarball in advance. Be sure that your connection to "
                     "this mirror is secure!")
        elif spack.config.get('config:checksum'):
            self.fetcher.check()

    def cache_local(self):
        spack.caches.fetch_cache.store(
            self.fetcher, self.mirror_paths.storage_path)

    def cache_mirror(self, mirror, stats):
        """Perform a fetch if the resource is not already cached

        Arguments:
            mirror (MirrorCache): the mirror to cache this Stage's resource in
            stats (MirrorStats): this is updated depending on whether the
                caching operation succeeded or failed
        """
        if isinstance(self.default_fetcher, fs.BundleFetchStrategy):
            # BundleFetchStrategy has no source to fetch. The associated
            # fetcher does nothing but the associated stage may still exist.
            # There is currently no method available on the fetcher to
            # distinguish this ('cachable' refers to whether the fetcher
            # refers to a resource with a fixed ID, which is not the same
            # concept as whether there is anything to fetch at all) so we
            # must examine the type of the fetcher.
            return

        if (mirror.skip_unstable_versions and
            not fs.stable_target(self.default_fetcher)):
            return

        absolute_storage_path = os.path.join(
            mirror.root, self.mirror_paths.storage_path)

        if os.path.exists(absolute_storage_path):
            stats.already_existed(absolute_storage_path)
        else:
            self.fetch()
            self.check()
            mirror.store(
                self.fetcher, self.mirror_paths.storage_path)
            stats.added(absolute_storage_path)

        mirror.symlink(self.mirror_paths)

    def expand_archive(self):
        """Changes to the stage directory and attempt to expand the downloaded
        archive.  Fail if the stage is not set up or if the archive is not yet
        downloaded."""
        if not self.expanded:
            self.fetcher.expand()
            tty.msg("Created stage in %s" % self.path)
        else:
            tty.msg("Already staged %s in %s" % (self.name, self.path))

    def restage(self):
        """Removes the expanded archive path if it exists, then re-expands
           the archive.
        """
        self.fetcher.reset()

    def create(self):
        """
        Ensures the top-level (config:build_stage) directory exists.
        """
        # Emulate file permissions for tempfile.mkdtemp.
        if not os.path.exists(self.path):
            mkdirp(self.path, mode=stat.S_IRWXU)
        elif not os.path.isdir(self.path):
            os.remove(self.path)
            mkdirp(self.path, mode=stat.S_IRWXU)

        # Make sure we can actually do something with the stage we made.
        ensure_access(self.path)
        self.created = True

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

    def __init__(self, url_or_fetch_strategy, root, resource, **kwargs):
        super(ResourceStage, self).__init__(url_or_fetch_strategy, **kwargs)
        self.root_stage = root
        self.resource = resource

    def restage(self):
        super(ResourceStage, self).restage()
        self._add_to_root_stage()

    def expand_archive(self):
        super(ResourceStage, self).expand_archive()
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
            placement = {'': placement}

        target_path = os.path.join(
            root_stage.source_path, resource.destination)

        try:
            os.makedirs(target_path)
        except OSError as err:
            tty.debug(err)
            if err.errno == errno.EEXIST and os.path.isdir(target_path):
                pass
            else:
                raise

        for key, value in iteritems(placement):
            destination_path = os.path.join(target_path, value)
            source_path = os.path.join(self.source_path, key)

            if not os.path.exists(destination_path):
                tty.info('Moving resource stage\n\tsource : '
                         '{stage}\n\tdestination : {destination}'.format(
                             stage=source_path, destination=destination_path
                         ))

                src = os.path.realpath(source_path)

                if os.path.isdir(src):
                    install_tree(src, destination_path)
                else:
                    install(src, destination_path)


@pattern.composite(method_list=[
    'fetch', 'create', 'created', 'check', 'expand_archive', 'restage',
    'destroy', 'cache_local', 'cache_mirror', 'managed_by_spack'])
class StageComposite:
    """Composite for Stage type objects. The first item in this composite is
    considered to be the root package, and operations that return a value are
    forwarded to it."""
    #
    # __enter__ and __exit__ delegate to all stages in the composite.
    #

    def __enter__(self):
        for item in self:
            item.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for item in reversed(self):
            item.keep = getattr(self, 'keep', False)
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


class DIYStage(object):
    """
    Simple class that allows any directory to be a spack stage.  Consequently,
    it does not expect or require that the source path adhere to the standard
    directory naming convention.
    """

    """DIY staging is, by definition, not managed by Spack."""
    managed_by_spack = False

    def __init__(self, path):
        if path is None:
            raise ValueError("Cannot construct DIYStage without a path.")
        elif not os.path.isdir(path):
            raise StagePathError("The stage path directory does not exist:",
                                 path)

        self.archive_file = None
        self.path = path
        self.source_path = path
        self.created = True

    # DIY stages do nothing as context managers.
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def fetch(self, *args, **kwargs):
        tty.msg("No need to fetch for DIY.")

    def check(self):
        tty.msg("No checksum needed for DIY.")

    def expand_archive(self):
        tty.msg("Using source directory: %s" % self.source_path)

    @property
    def expanded(self):
        """Returns True since the source_path must exist."""
        return True

    def restage(self):
        raise RestageError("Cannot restage a DIY stage.")

    def create(self):
        self.created = True

    def destroy(self):
        # No need to destroy DIY stage.
        pass

    def cache_local(self):
        tty.msg("Sources for DIY stages are not cached")


def ensure_access(file):
    """Ensure we can access a directory and die with an error if we can't."""
    if not can_access(file):
        tty.die("Insufficient permissions for %s" % file)


def purge():
    """Remove all build directories in the top-level stage path."""
    root = get_stage_root()
    if os.path.isdir(root):
        for stage_dir in os.listdir(root):
            if stage_dir.startswith(stage_prefix) or stage_dir == '.lock':
                stage_path = os.path.join(root, stage_dir)
                remove_linked_tree(stage_path)


def get_checksums_for_versions(
        url_dict, name, first_stage_function=None, keep_stage=False,
        fetch_options=None, batch=False):
    """Fetches and checksums archives from URLs.

    This function is called by both ``spack checksum`` and ``spack
    create``.  The ``first_stage_function`` argument allows the caller to
    inspect the first downloaded archive, e.g., to determine the build
    system.

    Args:
        url_dict (dict): A dictionary of the form: version -> URL
        name (str): The name of the package
        first_stage_function (callable): function that takes a Stage and a URL;
            this is run on the stage of the first URL downloaded
        keep_stage (bool): whether to keep staging area when command completes
        batch (bool): whether to ask user how many versions to fetch (false)
            or fetch all versions (true)
        fetch_options (dict): Options used for the fetcher (such as timeout
            or cookies)

    Returns:
        (str): A multi-line string containing versions and corresponding hashes

    """
    sorted_versions = sorted(url_dict.keys(), reverse=True)

    # Find length of longest string in the list for padding
    max_len = max(len(str(v)) for v in sorted_versions)
    num_ver = len(sorted_versions)

    tty.msg("Found {0} version{1} of {2}:".format(
            num_ver, '' if num_ver == 1 else 's', name),
            "",
            *spack.cmd.elide_list(
                ["{0:{1}}  {2}".format(str(v), max_len, url_dict[v])
                 for v in sorted_versions]))
    print()

    if batch:
        archives_to_fetch = len(sorted_versions)
    else:
        archives_to_fetch = tty.get_number(
            "How many would you like to checksum?", default=1, abort='q')

    if not archives_to_fetch:
        tty.die("Aborted.")

    versions = sorted_versions[:archives_to_fetch]
    urls = [url_dict[v] for v in versions]

    tty.msg("Downloading...")
    version_hashes = []
    i = 0
    for url, version in zip(urls, versions):
        try:
            if fetch_options:
                url_or_fs = fs.URLFetchStrategy(
                    url, fetch_options=fetch_options)
            else:
                url_or_fs = url
            with Stage(url_or_fs, keep=keep_stage) as stage:
                # Fetch the archive
                stage.fetch()
                if i == 0 and first_stage_function:
                    # Only run first_stage_function the first time,
                    # no need to run it every time
                    first_stage_function(stage, url)

                # Checksum the archive and add it to the list
                version_hashes.append((version, spack.util.crypto.checksum(
                    hashlib.sha256, stage.archive_file)))
                i += 1
        except FailedDownloadError:
            tty.msg("Failed to fetch {0}".format(url))
        except Exception as e:
            tty.msg("Something failed on {0}, skipping.".format(url),
                    "  ({0})".format(e))

    if not version_hashes:
        tty.die("Could not fetch any versions for {0}".format(name))

    # Find length of longest string in the list for padding
    max_len = max(len(str(v)) for v, h in version_hashes)

    # Generate the version directives to put in a package.py
    version_lines = "\n".join([
        "    version('{0}', {1}sha256='{2}')".format(
            v, ' ' * (max_len - len(str(v))), h) for v, h in version_hashes
    ])

    num_hash = len(version_hashes)
    tty.msg("Checksummed {0} version{1} of {2}:".format(
        num_hash, '' if num_hash == 1 else 's', name))

    return version_lines


class StageError(spack.error.SpackError):
    """"Superclass for all errors encountered during staging."""


class StagePathError(StageError):
    """"Error encountered with stage path."""


class RestageError(StageError):
    """"Error encountered during restaging."""


class VersionFetchError(StageError):
    """Raised when we can't determine a URL to fetch a package."""


# Keep this in namespace for convenience
FailedDownloadError = fs.FailedDownloadError
