# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module encapsulates package installation functionality.

The PackageInstaller coordinates concurrent builds of packages for the same
Spack instance by leveraging the dependency DAG and file system locks.  It
also proceeds with the installation of non-dependent packages of failed
dependencies in order to install as many dependencies of a package as possible.

Bottom-up traversal of the dependency DAG while prioritizing packages with no
uninstalled dependencies allows multiple processes to perform concurrent builds
of separate packages associated with a spec.

File system locks enable coordination such that no two processes attempt to
build the same or a failed dependency package.

Failures to install dependency packages result in removal of their dependents'
build tasks from the current process.  A failure file is also written (and
locked) so that other processes can detect the failure and adjust their build
tasks accordingly.

This module supports the coordination of local and distributed concurrent
installations of packages in a Spack instance.
"""

import copy
import glob
import heapq
import itertools
import os
import shutil
import six
import sys
import time

from collections import defaultdict

import llnl.util.filesystem as fs
import llnl.util.lock as lk
import llnl.util.tty as tty
import spack.binary_distribution as binary_distribution
import spack.compilers
import spack.error
import spack.hooks
import spack.package
import spack.package_prefs as prefs
import spack.repo
import spack.store

from llnl.util.tty.color import colorize
from llnl.util.tty.log import log_output
from spack.util.environment import dump_environment
from spack.util.executable import which


#: Counter to support unique spec sequencing that is used to ensure packages
#: with the same priority are (initially) processed in the order in which they
#: were added (see https://docs.python.org/2/library/heapq.html).
_counter = itertools.count(0)

#: Build status indicating task has been added.
STATUS_ADDED = 'queued'

#: Build status indicating the spec failed to install
STATUS_FAILED = 'failed'

#: Build status indicating the spec is being installed (possibly by another
#: process)
STATUS_INSTALLING = 'installing'

#: Build status indicating the spec was sucessfully installed
STATUS_INSTALLED = 'installed'

#: Build status indicating the task has been popped from the queue
STATUS_DEQUEUED = 'dequeued'

#: Build status indicating task has been removed (to maintain priority
#: queue invariants).
STATUS_REMOVED = 'removed'


def _check_last_phase(pkg):
    """
    Ensures the specified package has a valid last phase before proceeding
    with its installation.

    The last phase is also set to None if it is the last phase of the
    package already.

    Args:
        pkg (PackageBase): the package being installed

    Raises:
        ``BadInstallPhase`` if stop_before or last phase is invalid
    """
    if pkg.stop_before_phase and pkg.stop_before_phase not in pkg.phases:
        raise BadInstallPhase(pkg.name, pkg.stop_before_phase)

    if pkg.last_phase and pkg.last_phase not in pkg.phases:
        raise BadInstallPhase(pkg.name, pkg.last_phase)

    # If we got a last_phase, make sure it's not already last
    if pkg.last_phase and pkg.last_phase == pkg.phases[-1]:
        pkg.last_phase = None


def _handle_external_and_upstream(pkg, explicit):
    """
    Determine if the package is external or upstream and register it in the
    database if it is external package.

    Args:
        pkg (Package): the package whose installation is under consideration
        explicit (bool): the package was explicitly requested by the user
    Return:
        (bool): ``True`` if the package is external or upstream (so not to
            be installed locally), otherwise, ``True``
    """
    # For external packages the workflow is simplified, and basically
    # consists in module file generation and registration in the DB.
    if pkg.spec.external:
        _process_external_package(pkg, explicit)
        _print_installed_pkg('{0} (external {1})'
                             .format(pkg.prefix, package_id(pkg)))
        return True

    if pkg.installed_upstream:
        tty.verbose('{0} is installed in an upstream Spack instance at {1}'
                    .format(package_id(pkg), pkg.spec.prefix))
        _print_installed_pkg(pkg.prefix)

        # This will result in skipping all post-install hooks. In the case
        # of modules this is considered correct because we want to retrieve
        # the module from the upstream Spack instance.
        return True

    return False


def _do_fake_install(pkg):
    """
    Make a fake install directory containing fake executables, headers,
    and libraries.

    Args:
        pkg (PackageBase): the package whose installation is to be faked
    """

    command = pkg.name
    header = pkg.name
    library = pkg.name

    # Avoid double 'lib' for packages whose names already start with lib
    if not pkg.name.startswith('lib'):
        library = 'lib' + library

    dso_suffix = '.dylib' if sys.platform == 'darwin' else '.so'
    chmod = which('chmod')

    # Install fake command
    fs.mkdirp(pkg.prefix.bin)
    fs.touch(os.path.join(pkg.prefix.bin, command))
    chmod('+x', os.path.join(pkg.prefix.bin, command))

    # Install fake header file
    fs.mkdirp(pkg.prefix.include)
    fs.touch(os.path.join(pkg.prefix.include, header + '.h'))

    # Install fake shared and static libraries
    fs.mkdirp(pkg.prefix.lib)
    for suffix in [dso_suffix, '.a']:
        fs.touch(os.path.join(pkg.prefix.lib, library + suffix))

    # Install fake man page
    fs.mkdirp(pkg.prefix.man.man1)

    packages_dir = spack.store.layout.build_packages_path(pkg.spec)
    dump_packages(pkg.spec, packages_dir)


def _packages_needed_to_bootstrap_compiler(compiler, architecture, pkgs):
    """
    Return a list of packages required to bootstrap `pkg`s compiler

    Checks Spack's compiler configuration for a compiler that
    matches the package spec.

    Args:
        compiler (CompilerSpec): the compiler to bootstrap
        architecture (ArchSpec): the architecture for which to boostrap the
            compiler
        pkgs (list of PackageBase): the packages that may need their compiler
            installed

    Return:
        (list) list of tuples, (PackageBase, bool), for concretized compiler-
            -related packages that need to be installed and bool values
            specify whether the package is the bootstrap compiler
            (``True``) or one of its dependencies (``False``).  The list
            will be empty if there are no compilers.
    """
    tty.debug('Bootstrapping {0} compiler'.format(compiler))
    compilers = spack.compilers.compilers_for_spec(
        compiler, arch_spec=architecture)
    if compilers:
        return []

    dep = spack.compilers.pkg_spec_for_compiler(compiler)

    # Set the architecture for the compiler package in a way that allows the
    # concretizer to back off if needed for the older bootstrapping compiler
    dep.constrain('platform=%s' % str(architecture.platform))
    dep.constrain('os=%s' % str(architecture.os))
    dep.constrain('target=%s:' %
                  architecture.target.microarchitecture.family.name)
    # concrete CompilerSpec has less info than concrete Spec
    # concretize as Spec to add that information
    dep.concretize()
    # mark compiler as depended-on by the packages that use it
    for pkg in pkgs:
        dep._dependents[pkg.name] = spack.spec.DependencySpec(
            pkg.spec, dep, ('build',))
    packages = [(s.package, False) for
                s in dep.traverse(order='post', root=False)]
    packages.append((dep.package, True))
    return packages


def _hms(seconds):
    """
    Convert seconds to hours, minutes, seconds

    Args:
        seconds (int): time to be converted in seconds

    Return:
        (str) String representation of the time as #h #m #.##s
    """
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    parts = []
    if h:
        parts.append("%dh" % h)
    if m:
        parts.append("%dm" % m)
    if s:
        parts.append("%.2fs" % s)
    return ' '.join(parts)


def _install_from_cache(pkg, cache_only, explicit, unsigned=False,
                        full_hash_match=False):
    """
    Extract the package from binary cache

    Args:
        pkg (PackageBase): the package to install from the binary cache
        cache_only (bool): only extract from binary cache
        explicit (bool): ``True`` if installing the package was explicitly
            requested by the user, otherwise, ``False``
        unsigned (bool): ``True`` if binary package signatures to be checked,
            otherwise, ``False``

    Return:
        (bool) ``True`` if the package was extract from binary cache,
            ``False`` otherwise
    """
    installed_from_cache = _try_install_from_binary_cache(
        pkg, explicit, unsigned=unsigned, full_hash_match=full_hash_match)
    pkg_id = package_id(pkg)
    if not installed_from_cache:
        pre = 'No binary for {0} found'.format(pkg_id)
        if cache_only:
            tty.die('{0} when cache-only specified'.format(pre))

        tty.msg('{0}: installing from source'.format(pre))
        return False

    tty.debug('Successfully extracted {0} from binary cache'.format(pkg_id))
    _print_installed_pkg(pkg.spec.prefix)
    spack.hooks.post_install(pkg.spec)
    return True


def _print_installed_pkg(message):
    """
    Output a message with a package icon.

    Args:
        message (str): message to be output
    """
    print(colorize('@*g{[+]} ') + message)


def _process_external_package(pkg, explicit):
    """
    Helper function to run post install hooks and register external packages.

    Args:
        pkg (Package): the external package
        explicit (bool): if the package was requested explicitly by the user,
            ``False`` if it was pulled in as a dependency of an explicit
            package.
    """
    assert pkg.spec.external, \
        'Expected to post-install/register an external package.'

    pre = '{s.name}@{s.version} :'.format(s=pkg.spec)
    spec = pkg.spec

    if spec.external_modules:
        tty.msg('{0} has external module in {1}'
                .format(pre, spec.external_modules))
        tty.debug('{0} is actually installed in {1}'
                  .format(pre, spec.external_path))
    else:
        tty.debug('{0} externally installed in {1}'
                  .format(pre, spec.external_path))

    try:
        # Check if the package was already registered in the DB.
        # If this is the case, then just exit.
        tty.debug('{0} already registered in DB'.format(pre))

        # Update the explicit state if it is necessary
        if explicit:
            spack.store.db.update_explicit(spec, explicit)

    except KeyError:
        # If not, register it and generate the module file.
        # For external packages we just need to run
        # post-install hooks to generate module files.
        tty.debug('{0} generating module file'.format(pre))
        spack.hooks.post_install(spec)

        # Add to the DB
        tty.debug('{0} registering into DB'.format(pre))
        spack.store.db.add(spec, None, explicit=explicit)


def _process_binary_cache_tarball(pkg, binary_spec, explicit, unsigned,
                                  preferred_mirrors=None):
    """
    Process the binary cache tarball.

    Args:
        pkg (PackageBase): the package being installed
        binary_spec (Spec): the spec  whose cache has been confirmed
        explicit (bool): the package was explicitly requested by the user
        unsigned (bool): ``True`` if binary package signatures to be checked,
            otherwise, ``False``
        preferred_mirrors (list): Optional list of urls to prefer when
            attempting to download the tarball

    Return:
        (bool) ``True`` if the package was extracted from binary cache,
            else ``False``
    """
    tarball = binary_distribution.download_tarball(
        binary_spec, preferred_mirrors=preferred_mirrors)
    # see #10063 : install from source if tarball doesn't exist
    if tarball is None:
        tty.msg('{0} exists in binary cache but with different hash'
                .format(pkg.name))
        return False

    pkg_id = package_id(pkg)
    tty.msg('Extracting {0} from binary cache'.format(pkg_id))
    binary_distribution.extract_tarball(binary_spec, tarball, allow_root=False,
                                        unsigned=unsigned, force=False)
    pkg.installed_from_binary_cache = True
    spack.store.db.add(pkg.spec, spack.store.layout, explicit=explicit)
    return True


def _try_install_from_binary_cache(pkg, explicit, unsigned=False,
                                   full_hash_match=False):
    """
    Try to extract the package from binary cache.

    Args:
        pkg (PackageBase): the package to be extracted from binary cache
        explicit (bool): the package was explicitly requested by the user
        unsigned (bool): ``True`` if binary package signatures to be checked,
            otherwise, ``False``
    """
    pkg_id = package_id(pkg)
    tty.debug('Searching for binary cache of {0}'.format(pkg_id))
    matches = binary_distribution.get_mirrors_for_spec(
        pkg.spec, full_hash_match=full_hash_match)

    if not matches:
        return False

    # In the absence of guidance from user or some other reason to prefer one
    # mirror over another, any match will suffice, so just pick the first one.
    preferred_mirrors = [match['mirror_url'] for match in matches]
    binary_spec = matches[0]['spec']
    return _process_binary_cache_tarball(pkg, binary_spec, explicit, unsigned,
                                         preferred_mirrors=preferred_mirrors)


def clear_failures():
    """
    Remove all failure tracking markers for the Spack instance.
    """
    spack.store.db.clear_all_failures()


def dump_packages(spec, path):
    """
    Dump all package information for a spec and its dependencies.

    This creates a package repository within path for every namespace in the
    spec DAG, and fills the repos with package files and patch files for every
    node in the DAG.

    Args:
        spec (Spec): the Spack spec whose package information is to be dumped
        path (str): the path to the build packages directory
    """
    fs.mkdirp(path)

    # Copy in package.py files from any dependencies.
    # Note that we copy them in as they are in the *install* directory
    # NOT as they are in the repository, because we want a snapshot of
    # how *this* particular build was done.
    for node in spec.traverse(deptype=all):
        if node is not spec:
            # Locate the dependency package in the install tree and find
            # its provenance information.
            source = spack.store.layout.build_packages_path(node)
            source_repo_root = os.path.join(source, node.namespace)

            # If there's no provenance installed for the package, skip it.
            # If it's external, skip it because it either:
            # 1) it wasn't built with Spack, so it has no Spack metadata
            # 2) it was built by another Spack instance, and we do not
            # (currently) use Spack metadata to associate repos with externals
            # built by other Spack instances.
            # Spack can always get something current from the builtin repo.
            if node.external or not os.path.isdir(source_repo_root):
                continue

            # Create a source repo and get the pkg directory out of it.
            try:
                source_repo = spack.repo.Repo(source_repo_root)
                source_pkg_dir = source_repo.dirname_for_package_name(
                    node.name)
            except spack.repo.RepoError as err:
                tty.debug('Failed to create source repo for {0}: {1}'
                          .format(node.name, str(err)))
                source_pkg_dir = None
                tty.warn("Warning: Couldn't copy in provenance for {0}"
                         .format(node.name))

        # Create a destination repository
        dest_repo_root = os.path.join(path, node.namespace)
        if not os.path.exists(dest_repo_root):
            spack.repo.create_repo(dest_repo_root)
        repo = spack.repo.Repo(dest_repo_root)

        # Get the location of the package in the dest repo.
        dest_pkg_dir = repo.dirname_for_package_name(node.name)
        if node is spec:
            spack.repo.path.dump_provenance(node, dest_pkg_dir)
        elif source_pkg_dir:
            fs.install_tree(source_pkg_dir, dest_pkg_dir)


def get_dependent_ids(spec):
    """
    Return a list of package ids for the spec's dependents

    Args:
        spec (Spec): Concretized spec

    Returns:
        (list of str): list of package ids
    """
    return [package_id(d.package) for d in spec.dependents()]


def install_msg(name, pid):
    """
    Colorize the name/id of the package being installed

    Args:
        name (str): Name/id of the package being installed
        pid (id): id of the installer process

    Return:
        (str) Colorized installing message
    """
    pre = '{0}: '.format(pid) if tty.show_pid() else ''
    return pre + colorize('@*{Installing} @*g{%s}' % name)


def log(pkg):
    """
    Copy provenance into the install directory on success

    Args:
        pkg (Package): the package that was built and installed
    """
    packages_dir = spack.store.layout.build_packages_path(pkg.spec)

    # Remove first if we're overwriting another build
    try:
        # log and env install paths are inside this
        shutil.rmtree(packages_dir)
    except Exception as e:
        # FIXME : this potentially catches too many things...
        tty.debug(e)

    # Archive the whole stdout + stderr for the package
    fs.install(pkg.log_path, pkg.install_log_path)

    # Archive the environment used for the build
    fs.install(pkg.env_path, pkg.install_env_path)

    if os.path.exists(pkg.configure_args_path):
        # Archive the args used for the build
        fs.install(pkg.configure_args_path, pkg.install_configure_args_path)

    # Finally, archive files that are specific to each package
    with fs.working_dir(pkg.stage.path):
        errors = six.StringIO()
        target_dir = os.path.join(
            spack.store.layout.metadata_path(pkg.spec), 'archived-files')

        for glob_expr in pkg.archive_files:
            # Check that we are trying to copy things that are
            # in the stage tree (not arbitrary files)
            abs_expr = os.path.realpath(glob_expr)
            if os.path.realpath(pkg.stage.path) not in abs_expr:
                errors.write('[OUTSIDE SOURCE PATH]: {0}\n'.format(glob_expr))
                continue
            # Now that we are sure that the path is within the correct
            # folder, make it relative and check for matches
            if os.path.isabs(glob_expr):
                glob_expr = os.path.relpath(glob_expr, pkg.stage.path)
            files = glob.glob(glob_expr)
            for f in files:
                try:
                    target = os.path.join(target_dir, f)
                    # We must ensure that the directory exists before
                    # copying a file in
                    fs.mkdirp(os.path.dirname(target))
                    fs.install(f, target)
                except Exception as e:
                    tty.debug(e)

                    # Here try to be conservative, and avoid discarding
                    # the whole install procedure because of copying a
                    # single file failed
                    errors.write('[FAILED TO ARCHIVE]: {0}'.format(f))

        if errors.getvalue():
            error_file = os.path.join(target_dir, 'errors.txt')
            fs.mkdirp(target_dir)
            with open(error_file, 'w') as err:
                err.write(errors.getvalue())
            tty.warn('Errors occurred when archiving files.\n\t'
                     'See: {0}'.format(error_file))

    dump_packages(pkg.spec, packages_dir)


def package_id(pkg):
    """A "unique" package identifier for installation purposes

    The identifier is used to track build tasks, locks, install, and
    failure statuses.

    The identifier needs to distinguish between combinations of compilers
    and packages for combinatorial environments.

    Args:
        pkg (PackageBase): the package from which the identifier is derived
    """
    if not pkg.spec.concrete:
        raise ValueError("Cannot provide a unique, readable id when "
                         "the spec is not concretized.")

    return "{0}-{1}-{2}".format(pkg.name, pkg.version, pkg.spec.dag_hash())


class PackageInstaller(object):
    '''
    Class for managing the install process for a Spack instance based on a
    bottom-up DAG approach.

    This installer can coordinate concurrent batch and interactive, local
    and distributed (on a shared file system) builds for the same Spack
    instance.
    '''

    def __init__(self, installs=[]):
        """ Initialize the installer.

        Args:
            installs (list of (pkg, install_args)): list of tuples, where each
                tuple consists of a package (PackageBase) and its associated
                 install arguments (dict)
        Return:
            (PackageInstaller) instance
        """
        # List of build requests
        self.build_requests = [BuildRequest(pkg, install_args)
                               for pkg, install_args in installs]

        # Priority queue of build tasks
        self.build_pq = []

        # Mapping of unique package ids to build task
        self.build_tasks = {}

        # Cache of package locks for failed packages, keyed on package's ids
        self.failed = {}

        # Cache the PID for distributed build messaging
        self.pid = os.getpid()

        # Cache of installed packages' unique ids
        self.installed = set()

        # Data store layout
        self.layout = spack.store.layout

        # Locks on specs being built, keyed on the package's unique id
        self.locks = {}

        # Cache fail_fast option to ensure if one build request asks to fail
        # fast then that option applies to all build requests.
        self.fail_fast = False

    def __repr__(self):
        """Returns a formal representation of the package installer."""
        rep = '{0}('.format(self.__class__.__name__)
        for attr, value in self.__dict__.items():
            rep += '{0}={1}, '.format(attr, value.__repr__())
        return '{0})'.format(rep.strip(', '))

    def __str__(self):
        """Returns a printable version of the package installer."""
        requests = '#requests={0}'.format(len(self.build_requests))
        tasks = '#tasks={0}'.format(len(self.build_tasks))
        failed = 'failed ({0}) = {1}'.format(len(self.failed), self.failed)
        installed = 'installed ({0}) = {1}'.format(
            len(self.installed), self.installed)
        return '{0}: {1}; {2}; {3}; {4}'.format(
            self.pid, requests, tasks, installed, failed)

    def _add_bootstrap_compilers(
            self, compiler, architecture, pkgs, request, all_deps):
        """
        Add bootstrap compilers and dependencies to the build queue.

        Args:
            compiler: the compiler to boostrap
            architecture: the architecture for which to bootstrap the compiler
            pkgs (PackageBase): the package with possible compiler dependencies
            request (BuildRequest): the associated install request
            all_deps (defaultdict(set)): dictionary of all dependencies and
                associated dependents
        """
        packages = _packages_needed_to_bootstrap_compiler(
            compiler, architecture, pkgs)
        for (comp_pkg, is_compiler) in packages:
            if package_id(comp_pkg) not in self.build_tasks:
                self._add_init_task(comp_pkg, request, is_compiler, all_deps)

    def _add_init_task(self, pkg, request, is_compiler, all_deps):
        """
        Creates and queus the initial build task for the package.

        Args:
            pkg (Package): the package to be built and installed
            request (BuildRequest or None): the associated install request
                 where ``None`` can be used to indicate the package was
                 explicitly requested by the user
            is_compiler (bool): whether task is for a bootstrap compiler
            all_deps (defaultdict(set)): dictionary of all dependencies and
                associated dependents
        """
        task = BuildTask(pkg, request, is_compiler, 0, 0, STATUS_ADDED,
                         self.installed)
        for dep_id in task.dependencies:
            all_deps[dep_id].add(package_id(pkg))

        self._push_task(task)

    def _check_db(self, spec):
        """Determine if the spec is flagged as installed in the database

        Args:
            spec (Spec): spec whose database install status is being checked

        Return:
            (rec, installed_in_db) tuple where rec is the database record, or
                None, if there is no matching spec, and installed_in_db is
                ``True`` if the spec is considered installed and ``False``
                otherwise
        """
        try:
            rec = spack.store.db.get_record(spec)
            installed_in_db = rec.installed if rec else False
        except KeyError:
            # KeyError is raised if there is no matching spec in the database
            # (versus no matching specs that are installed).
            rec = None
            installed_in_db = False
        return rec, installed_in_db

    def _check_deps_status(self, request):
        """Check the install status of the requested package

        Args:
            request (BuildRequest): the associated install request
        """
        err = 'Cannot proceed with {0}: {1}'
        for dep in request.traverse_dependencies():
            dep_pkg = dep.package
            dep_id = package_id(dep_pkg)

            # Check for failure since a prefix lock is not required
            if spack.store.db.prefix_failed(dep):
                action = "'spack install' the dependency"
                msg = '{0} is marked as an install failure: {1}' \
                    .format(dep_id, action)
                raise InstallError(err.format(request.pkg_id, msg))

            # Attempt to get a write lock to ensure another process does not
            # uninstall the dependency while the requested spec is being
            # installed
            ltype, lock = self._ensure_locked('write', dep_pkg)
            if lock is None:
                msg = '{0} is write locked by another process'.format(dep_id)
                raise InstallError(err.format(request.pkg_id, msg))

            # Flag external and upstream packages as being installed
            if dep_pkg.spec.external or dep_pkg.installed_upstream:
                self._flag_installed(dep_pkg)
                continue

            # Check the database to see if the dependency has been installed
            # and flag as such if appropriate
            rec, installed_in_db = self._check_db(dep)
            if installed_in_db and (
                    dep.dag_hash() not in request.overwrite or
                    rec.installation_time > request.overwrite_time):
                tty.debug('Flagging {0} as installed per the database'
                          .format(dep_id))
                self._flag_installed(dep_pkg)

    def _prepare_for_install(self, task):
        """
        Check the database and leftover installation directories/files and
        prepare for a new install attempt for an uninstalled package.

        Preparation includes cleaning up installation and stage directories
        and ensuring the database is up-to-date.

        Args:
            task (BuildTask): the build task whose associated package is
                being checked
        """
        install_args = task.request.install_args
        keep_prefix = install_args.get('keep_prefix')
        keep_stage = install_args.get('keep_stage')
        restage = install_args.get('restage')

        # Make sure the package is ready to be locally installed.
        self._ensure_install_ready(task.pkg)

        # Skip file system operations if we've already gone through them for
        # this spec.
        if task.pkg_id in self.installed:
            # Already determined the spec has been installed
            return

        # Determine if the spec is flagged as installed in the database
        rec, installed_in_db = self._check_db(task.pkg.spec)

        # Make sure the installation directory is in the desired state
        # for uninstalled specs.
        partial = False
        if not installed_in_db and os.path.isdir(task.pkg.spec.prefix):
            if not keep_prefix:
                task.pkg.remove_prefix()
            else:
                tty.debug('{0} is partially installed'
                          .format(task.pkg_id))
                partial = True

        # Destroy the stage for a locally installed, non-DIYStage, package
        if restage and task.pkg.stage.managed_by_spack:
            task.pkg.stage.destroy()

        if not partial and self.layout.check_installed(task.pkg.spec) and (
                rec.spec.dag_hash() not in task.request.overwrite or
                rec.installation_time > task.request.overwrite_time
        ):
            self._update_installed(task)

            # Only update the explicit entry once for the explicit package
            if task.explicit:
                spack.store.db.update_explicit(task.pkg.spec, True)

            # In case the stage directory has already been created, this
            # check ensures it is removed after we checked that the spec is
            # installed.
            if not keep_stage:
                task.pkg.stage.destroy()

    def _cleanup_all_tasks(self):
        """Cleanup all build tasks to include releasing their locks."""
        for pkg_id in self.locks:
            self._release_lock(pkg_id)

        for pkg_id in self.failed:
            self._cleanup_failed(pkg_id)

        ids = list(self.build_tasks)
        for pkg_id in ids:
            try:
                self._remove_task(pkg_id)
            except Exception:
                pass

    def _cleanup_failed(self, pkg_id):
        """
        Cleanup any failed markers for the package

        Args:
            pkg_id (str): identifier for the failed package
        """
        lock = self.failed.get(pkg_id, None)
        if lock is not None:
            err = "{0} exception when removing failure tracking for {1}: {2}"
            msg = 'Removing failure mark on {0}'
            try:
                tty.verbose(msg.format(pkg_id))
                lock.release_write()
            except Exception as exc:
                tty.warn(err.format(exc.__class__.__name__, pkg_id, str(exc)))

    def _cleanup_task(self, pkg):
        """
        Cleanup the build task for the spec

        Args:
            pkg (PackageBase): the package being installed
        """
        self._remove_task(package_id(pkg))

        # Ensure we have a read lock to prevent others from uninstalling the
        # spec during our installation.
        self._ensure_locked('read', pkg)

    def _ensure_install_ready(self, pkg):
        """
        Ensure the package is ready to install locally, which includes
        already locked.

        Args:
            pkg (PackageBase): the package being locally installed
        """
        pkg_id = package_id(pkg)
        pre = "{0} cannot be installed locally:".format(pkg_id)

        # External packages cannot be installed locally.
        if pkg.spec.external:
            raise ExternalPackageError('{0} {1}'.format(pre, 'is external'))

        # Upstream packages cannot be installed locally.
        if pkg.installed_upstream:
            raise UpstreamPackageError('{0} {1}'.format(pre, 'is upstream'))

        # The package must have a prefix lock at this stage.
        if pkg_id not in self.locks:
            raise InstallLockError('{0} {1}'.format(pre, 'not locked'))

    def _ensure_locked(self, lock_type, pkg):
        """
        Add a prefix lock of the specified type for the package spec

        If the lock exists, then adjust accordingly.  That is, read locks
        will be upgraded to write locks if a write lock is requested and
        write locks will be downgraded to read locks if a read lock is
        requested.

        The lock timeout for write locks is deliberately near zero seconds in
        order to ensure the current process proceeds as quickly as possible to
        the next spec.

        Args:
            lock_type (str): 'read' for a read lock, 'write' for a write lock
            pkg (PackageBase): the package whose spec is being installed

        Return:
            (lock_type, lock) tuple where lock will be None if it could not
                be obtained
        """
        assert lock_type in ['read', 'write'], \
            '"{0}" is not a supported package management lock type' \
            .format(lock_type)

        pkg_id = package_id(pkg)
        ltype, lock = self.locks.get(pkg_id, (lock_type, None))
        if lock and ltype == lock_type:
            return ltype, lock

        desc = '{0} lock'.format(lock_type)
        msg = '{0} a {1} on {2} with timeout {3}'
        err = 'Failed to {0} a {1} for {2} due to {3}: {4}'

        if lock_type == 'read':
            # Wait until the other process finishes if there are no more
            # build tasks with priority 0 (i.e., with no uninstalled
            # dependencies).
            no_p0 = len(self.build_tasks) == 0 or not self._next_is_pri0()
            timeout = None if no_p0 else 3
        else:
            timeout = 1e-9  # Near 0 to iterate through install specs quickly

        try:
            if lock is None:
                tty.debug(msg.format('Acquiring', desc, pkg_id, timeout))
                op = 'acquire'
                lock = spack.store.db.prefix_lock(pkg.spec, timeout)
                if timeout != lock.default_timeout:
                    tty.warn('Expected prefix lock timeout {0}, not {1}'
                             .format(timeout, lock.default_timeout))
                if lock_type == 'read':
                    lock.acquire_read()
                else:
                    lock.acquire_write()

            elif lock_type == 'read':  # write -> read
                # Only get here if the current lock is a write lock, which
                # must be downgraded to be a read lock
                # Retain the original lock timeout, which is in the lock's
                # default_timeout setting.
                tty.debug(msg.format('Downgrading to', desc, pkg_id,
                                     lock.default_timeout))
                op = 'downgrade to'
                lock.downgrade_write_to_read()

            else:  # read -> write
                # Only get here if the current lock is a read lock, which
                # must be upgraded to be a write lock
                tty.debug(msg.format('Upgrading to', desc, pkg_id, timeout))
                op = 'upgrade to'
                lock.upgrade_read_to_write(timeout)
            tty.verbose('{0} is now {1} locked'.format(pkg_id, lock_type))

        except (lk.LockDowngradeError, lk.LockTimeoutError) as exc:
            tty.debug(err.format(op, desc, pkg_id, exc.__class__.__name__,
                                 str(exc)))
            lock = None

        except (Exception, KeyboardInterrupt, SystemExit) as exc:
            tty.error(err.format(op, desc, pkg_id, exc.__class__.__name__,
                      str(exc)))
            self._cleanup_all_tasks()
            raise

        self.locks[pkg_id] = (lock_type, lock)
        return self.locks[pkg_id]

    def _add_tasks(self, request, all_deps):
        """Add tasks to the priority queue for the given build request.

        It also tracks all dependents associated with each dependency in
        order to ensure proper tracking of uninstalled dependencies.

        Args:
            request (BuildRequest): the associated install request
            all_deps (defaultdict(set)): dictionary of all dependencies and
                associated dependents
        """
        tty.debug('Initializing the build queue for {0}'
                  .format(request.pkg.name))

        # Ensure not attempting to perform an installation when user didn't
        # want to go that far for the requested package.
        try:
            _check_last_phase(request.pkg)
        except BadInstallPhase as err:
            tty.warn('Installation request refused: {0}'.format(str(err)))
            return

        # Skip out early if the spec is not being installed locally (i.e., if
        # external or upstream).
        #
        # External and upstream packages need to get flagged as installed to
        # ensure proper status tracking for environment build.
        not_local = _handle_external_and_upstream(request.pkg, True)
        if not_local:
            self._flag_installed(request.pkg)
            return

        install_compilers = spack.config.get(
            'config:install_missing_compilers', False)

        install_deps = request.install_args.get('install_deps')
        # Bootstrap compilers first
        if install_deps and install_compilers:
            packages_per_compiler = {}

            for dep in request.traverse_dependencies():
                dep_pkg = dep.package
                compiler = dep_pkg.spec.compiler
                arch = dep_pkg.spec.architecture
                if compiler not in packages_per_compiler:
                    packages_per_compiler[compiler] = {}

                if arch not in packages_per_compiler[compiler]:
                    packages_per_compiler[compiler][arch] = []

                packages_per_compiler[compiler][arch].append(dep_pkg)

            compiler = request.pkg.spec.compiler
            arch = request.pkg.spec.architecture

            if compiler not in packages_per_compiler:
                packages_per_compiler[compiler] = {}

            if arch not in packages_per_compiler[compiler]:
                packages_per_compiler[compiler][arch] = []

            packages_per_compiler[compiler][arch].append(request.pkg)

            for compiler, archs in packages_per_compiler.items():
                for arch, packages in archs.items():
                    self._add_bootstrap_compilers(
                        compiler, arch, packages, request, all_deps)

        if install_deps:
            for dep in request.traverse_dependencies():
                dep_pkg = dep.package

                dep_id = package_id(dep_pkg)
                if dep_id not in self.build_tasks:
                    self._add_init_task(dep_pkg, request, False, all_deps)

                # Clear any persistent failure markings _unless_ they are
                # associated with another process in this parallel build
                # of the spec.
                spack.store.db.clear_failure(dep, force=False)

        install_package = request.install_args.get('install_package')
        if install_package and request.pkg_id not in self.build_tasks:

            # Be sure to clear any previous failure
            spack.store.db.clear_failure(request.spec, force=True)

            # If not installing dependencies, then determine their
            # installation status before proceeding
            if not install_deps:
                self._check_deps_status(request)

            # Now add the package itself, if appropriate
            self._add_init_task(request.pkg, request, False, all_deps)

        # Ensure if one request is to fail fast then all requests will.
        fail_fast = request.install_args.get('fail_fast')
        self.fail_fast = self.fail_fast or fail_fast

    def _install_task(self, task):
        """
        Perform the installation of the requested spec and/or dependency
        represented by the build task.

        Args:
            task (BuildTask): the installation build task for a package"""

        install_args = task.request.install_args
        cache_only = install_args.get('cache_only')
        explicit = task.explicit
        full_hash_match = install_args.get('full_hash_match')
        tests = install_args.get('tests')
        unsigned = install_args.get('unsigned')
        use_cache = install_args.get('use_cache')

        pkg, pkg_id = task.pkg, task.pkg_id

        tty.msg(install_msg(pkg_id, self.pid))
        task.start = task.start or time.time()
        task.status = STATUS_INSTALLING

        # Use the binary cache if requested
        if use_cache and \
                _install_from_cache(pkg, cache_only, explicit, unsigned,
                                    full_hash_match):
            self._update_installed(task)
            if task.compiler:
                spack.compilers.add_compilers_to_config(
                    spack.compilers.find_compilers([pkg.spec.prefix]))
            return

        pkg.run_tests = (tests is True or tests and pkg.name in tests)

        # hook that allows tests to inspect the Package before installation
        # see unit_test_check() docs.
        if not pkg.unit_test_check():
            return

        try:
            self._setup_install_dir(pkg)

            # Create a child process to do the actual installation.
            # Preserve verbosity settings across installs.
            spack.package.PackageBase._verbose = (
                spack.build_environment.start_build_process(
                    pkg, build_process, install_args)
            )

            # Note: PARENT of the build process adds the new package to
            # the database, so that we don't need to re-read from file.
            spack.store.db.add(pkg.spec, spack.store.layout,
                               explicit=explicit)

            # If a compiler, ensure it is added to the configuration
            if task.compiler:
                spack.compilers.add_compilers_to_config(
                    spack.compilers.find_compilers([pkg.spec.prefix]))
        except spack.build_environment.StopPhase as e:
            # A StopPhase exception means that do_install was asked to
            # stop early from clients, and is not an error at this point
            pid = '{0}: '.format(pkg.pid) if tty.show_pid() else ''
            tty.debug('{0}{1}'.format(pid, str(e)))
            tty.debug('Package stage directory: {0}'
                      .format(pkg.stage.source_path))

    def _next_is_pri0(self):
        """
        Determine if the next build task has priority 0

        Return:
            True if it does, False otherwise
        """
        # Leverage the fact that the first entry in the queue is the next
        # one that will be processed
        task = self.build_pq[0][1]
        return task.priority == 0

    def _pop_task(self):
        """
        Remove and return the lowest priority build task.

        Source: Variant of function at docs.python.org/2/library/heapq.html
        """
        while self.build_pq:
            task = heapq.heappop(self.build_pq)[1]
            if task.status != STATUS_REMOVED:
                del self.build_tasks[task.pkg_id]
                task.status = STATUS_DEQUEUED
                return task
        return None

    def _push_task(self, task):
        """
        Push (or queue) the specified build task for the package.

        Source: Customization of "add_task" function at
                docs.python.org/2/library/heapq.html

        Args:
            task (BuildTask): the installation build task for a package
        """
        msg = "{0} a build task for {1} with status '{2}'"
        skip = 'Skipping requeue of task for {0}: {1}'

        # Ensure do not (re-)queue installed or failed packages whose status
        # may have been determined by a separate process.
        if task.pkg_id in self.installed:
            tty.debug(skip.format(task.pkg_id, 'installed'))
            return

        if task.pkg_id in self.failed:
            tty.debug(skip.format(task.pkg_id, 'failed'))
            return

        # Remove any associated build task since its sequence will change
        self._remove_task(task.pkg_id)
        desc = 'Queueing' if task.attempts == 0 else 'Requeueing'
        tty.verbose(msg.format(desc, task.pkg_id, task.status))

        # Now add the new task to the queue with a new sequence number to
        # ensure it is the last entry popped with the same priority.  This
        # is necessary in case we are re-queueing a task whose priority
        # was decremented due to the installation of one of its dependencies.
        self.build_tasks[task.pkg_id] = task
        heapq.heappush(self.build_pq, (task.key, task))

    def _release_lock(self, pkg_id):
        """
        Release any lock on the package

        Args:
            pkg_id (str): identifier for the package whose lock is be released
        """
        if pkg_id in self.locks:
            err = "{0} exception when releasing {1} lock for {2}: {3}"
            msg = 'Releasing {0} lock on {1}'
            ltype, lock = self.locks[pkg_id]
            if lock is not None:
                try:
                    tty.verbose(msg.format(ltype, pkg_id))
                    if ltype == 'read':
                        lock.release_read()
                    else:
                        lock.release_write()
                except Exception as exc:
                    tty.warn(err.format(exc.__class__.__name__, ltype,
                                        pkg_id, str(exc)))

    def _remove_task(self, pkg_id):
        """
        Mark the existing package build task as being removed and return it.
        Raises KeyError if not found.

        Source: Variant of function at docs.python.org/2/library/heapq.html

        Args:
            pkg_id (str): identifier for the package to be removed
        """
        if pkg_id in self.build_tasks:
            tty.verbose('Removing build task for {0} from list'
                        .format(pkg_id))
            task = self.build_tasks.pop(pkg_id)
            task.status = STATUS_REMOVED
            return task
        else:
            return None

    def _requeue_task(self, task):
        """
        Requeues a task that appears to be in progress by another process.

        Args:
            task (BuildTask): the installation build task for a package
        """
        if task.status not in [STATUS_INSTALLED, STATUS_INSTALLING]:
            tty.msg('{0} {1}'.format(install_msg(task.pkg_id, self.pid),
                                     'in progress by another process'))

        new_task = task.next_attempt(self.installed)
        new_task.status = STATUS_INSTALLING
        self._push_task(new_task)

    def _setup_install_dir(self, pkg):
        """
        Create and ensure proper access controls for the install directory.

        Args:
            pkg (Package): the package to be built and installed
        """
        if not os.path.exists(pkg.spec.prefix):
            tty.verbose('Creating the installation directory {0}'
                        .format(pkg.spec.prefix))
            spack.store.layout.create_install_directory(pkg.spec)
        else:
            # Set the proper group for the prefix
            group = prefs.get_package_group(pkg.spec)
            if group:
                fs.chgrp(pkg.spec.prefix, group)

            # Set the proper permissions.
            # This has to be done after group because changing groups blows
            # away the sticky group bit on the directory
            mode = os.stat(pkg.spec.prefix).st_mode
            perms = prefs.get_package_dir_permissions(pkg.spec)
            if mode != perms:
                os.chmod(pkg.spec.prefix, perms)

            # Ensure the metadata path exists as well
            fs.mkdirp(spack.store.layout.metadata_path(pkg.spec), mode=perms)

    def _update_failed(self, task, mark=False, exc=None):
        """
        Update the task and transitive dependents as failed; optionally mark
        externally as failed; and remove associated build tasks.

        Args:
            task (BuildTask): the build task for the failed package
            mark (bool): ``True`` if the package and its dependencies are to
                be marked as "failed", otherwise, ``False``
            exc (Exception): optional exception if associated with the failure
        """
        pkg_id = task.pkg_id
        err = '' if exc is None else ': {0}'.format(str(exc))
        tty.debug('Flagging {0} as failed{1}'.format(pkg_id, err))
        if mark:
            self.failed[pkg_id] = spack.store.db.mark_failed(task.pkg.spec)
        else:
            self.failed[pkg_id] = None
        task.status = STATUS_FAILED

        for dep_id in task.dependents:
            if dep_id in self.build_tasks:
                tty.warn('Skipping build of {0} since {1} failed'
                         .format(dep_id, pkg_id))
                # Ensure the dependent's uninstalled dependents are
                # up-to-date and their build tasks removed.
                dep_task = self.build_tasks[dep_id]
                self._update_failed(dep_task, mark)
                self._remove_task(dep_id)
            else:
                tty.verbose('No build task for {0} to skip since {1} failed'
                            .format(dep_id, pkg_id))

    def _update_installed(self, task):
        """
        Mark the task as installed and ensure dependent build tasks are aware.

        Args:
            task (BuildTask): the build task for the installed package
        """
        task.status = STATUS_INSTALLED
        self._flag_installed(task.pkg, task.dependents)

    def _flag_installed(self, pkg, dependent_ids=None):
        """
        Flag the package as installed and ensure known by all build tasks of
        known dependents.

        Args:
            pkg (Package): Package that has been installed locally, externally
                or upstream
            dependent_ids (list of str or None): list of the package's
                dependent ids, or None if the dependent ids are limited to
                those maintained in the package (dependency DAG)
        """
        pkg_id = package_id(pkg)

        if pkg_id in self.installed:
            # Already determined the package has been installed
            return

        tty.debug('Flagging {0} as installed'.format(pkg_id))

        self.installed.add(pkg_id)

        # Update affected dependents
        dependent_ids = dependent_ids or get_dependent_ids(pkg.spec)
        for dep_id in set(dependent_ids):
            tty.debug('Removing {0} from {1}\'s uninstalled dependencies.'
                      .format(pkg_id, dep_id))
            if dep_id in self.build_tasks:
                # Ensure the dependent's uninstalled dependencies are
                # up-to-date.  This will require requeueing the task.
                dep_task = self.build_tasks[dep_id]
                self._push_task(dep_task.next_attempt(self.installed))
            else:
                tty.debug('{0} has no build task to update for {1}\'s success'
                          .format(dep_id, pkg_id))

    def _init_queue(self):
        """Initialize the build queue from the list of build requests."""
        all_dependencies = defaultdict(set)

        tty.debug('Initializing the build queue from the build requests')
        for request in self.build_requests:
            self._add_tasks(request, all_dependencies)

        # Add any missing dependents to ensure proper uninstalled dependency
        # tracking when installing multiple specs
        tty.debug('Ensure all dependencies know all dependents across specs')
        for dep_id in all_dependencies:
            if dep_id in self.build_tasks:
                dependents = all_dependencies[dep_id]
                task = self.build_tasks[dep_id]
                for dependent_id in dependents.difference(task.dependents):
                    task.add_dependent(dependent_id)

    def install(self):
        """
        Install the requested package(s) and or associated dependencies.

        Args:
            pkg (Package): the package to be built and installed"""
        self._init_queue()

        fail_fast_err = 'Terminating after first install failure'
        single_explicit_spec = len(self.build_requests) == 1
        failed_explicits = []
        exists_errors = []

        while self.build_pq:
            task = self._pop_task()
            if task is None:
                continue

            install_args = task.request.install_args
            keep_prefix = install_args.get('keep_prefix')

            pkg, pkg_id, spec = task.pkg, task.pkg_id, task.pkg.spec
            tty.verbose('Processing {0}: task={1}'.format(pkg_id, task))
            # Ensure that the current spec has NO uninstalled dependencies,
            # which is assumed to be reflected directly in its priority.
            #
            # If the spec has uninstalled dependencies, then there must be
            # a bug in the code (e.g., priority queue or uninstalled
            # dependencies handling).  So terminate under the assumption that
            # all subsequent tasks will have non-zero priorities or may be
            # dependencies of this task.
            if task.priority != 0:
                tty.error('Detected uninstalled dependencies for {0}: {1}'
                          .format(pkg_id, task.uninstalled_deps))
                left = [dep_id for dep_id in task.uninstalled_deps if
                        dep_id not in self.installed]
                if not left:
                    tty.warn('{0} does NOT actually have any uninstalled deps'
                             ' left'.format(pkg_id))
                dep_str = 'dependencies' if task.priority > 1 else 'dependency'
                raise InstallError(
                    'Cannot proceed with {0}: {1} uninstalled {2}: {3}'
                    .format(pkg_id, task.priority, dep_str,
                            ','.join(task.uninstalled_deps)))

            # Skip the installation if the spec is not being installed locally
            # (i.e., if external or upstream) BUT flag it as installed since
            # some package likely depends on it.
            if not task.explicit:
                if _handle_external_and_upstream(pkg, False):
                    self._flag_installed(pkg, task.dependents)
                    continue

            # Flag a failed spec.  Do not need an (install) prefix lock since
            # assume using a separate (failed) prefix lock file.
            if pkg_id in self.failed or spack.store.db.prefix_failed(spec):
                tty.warn('{0} failed to install'.format(pkg_id))
                self._update_failed(task)

                if self.fail_fast:
                    raise InstallError(fail_fast_err)

                continue

            # Attempt to get a write lock.  If we can't get the lock then
            # another process is likely (un)installing the spec or has
            # determined the spec has already been installed (though the
            # other process may be hung).
            ltype, lock = self._ensure_locked('write', pkg)
            if lock is None:
                # Attempt to get a read lock instead.  If this fails then
                # another process has a write lock so must be (un)installing
                # the spec (or that process is hung).
                ltype, lock = self._ensure_locked('read', pkg)

            # Requeue the spec if we cannot get at least a read lock so we
            # can check the status presumably established by another process
            # -- failed, installed, or uninstalled -- on the next pass.
            if lock is None:
                self._requeue_task(task)
                continue

            # Take a timestamp with the overwrite argument to allow checking
            # whether another process has already overridden the package.
            if task.request.overwrite and task.explicit:
                task.request.overwrite_time = time.time()

            # Determine state of installation artifacts and adjust accordingly.
            self._prepare_for_install(task)

            # Flag an already installed package
            if pkg_id in self.installed:
                # Downgrade to a read lock to preclude other processes from
                # uninstalling the package until we're done installing its
                # dependents.
                ltype, lock = self._ensure_locked('read', pkg)
                if lock is not None:
                    self._update_installed(task)
                    _print_installed_pkg(pkg.prefix)

                    # It's an already installed compiler, add it to the config
                    if task.compiler:
                        spack.compilers.add_compilers_to_config(
                            spack.compilers.find_compilers([pkg.spec.prefix]))

                else:
                    # At this point we've failed to get a write or a read
                    # lock, which means another process has taken a write
                    # lock between our releasing the write and acquiring the
                    # read.
                    #
                    # Requeue the task so we can re-check the status
                    # established by the other process -- failed, installed,
                    # or uninstalled -- on the next pass.
                    self.installed.remove(pkg_id)
                    self._requeue_task(task)
                continue

            # Having a read lock on an uninstalled pkg may mean another
            # process completed an uninstall of the software between the
            # time we failed to acquire the write lock and the time we
            # took the read lock.
            #
            # Requeue the task so we can check the status presumably
            # established by the other process -- failed, installed, or
            # uninstalled -- on the next pass.
            if ltype == 'read':
                self._requeue_task(task)
                continue

            # Proceed with the installation since we have an exclusive write
            # lock on the package.
            try:
                if pkg.spec.dag_hash() in task.request.overwrite:
                    rec, _ = self._check_db(pkg.spec)
                    if rec and rec.installed:
                        if rec.installation_time < task.request.overwrite_time:
                            # If it's actually overwriting, do a fs transaction
                            if os.path.exists(rec.path):
                                with fs.replace_directory_transaction(
                                        rec.path):
                                    self._install_task(task)
                            else:
                                tty.debug("Missing installation to overwrite")
                                self._install_task(task)
                    else:
                        # overwriting nothing
                        self._install_task(task)
                else:
                    self._install_task(task)

                self._update_installed(task)

                # If we installed then we should keep the prefix
                stop_before_phase = getattr(pkg, 'stop_before_phase', None)
                last_phase = getattr(pkg, 'last_phase', None)
                keep_prefix = keep_prefix or \
                    (stop_before_phase is None and last_phase is None)

            except spack.directory_layout.InstallDirectoryAlreadyExistsError \
                    as exc:
                tty.debug('Install prefix for {0} exists, keeping {1} in '
                          'place.'.format(pkg.name, pkg.prefix))
                self._update_installed(task)

                # Only terminate at this point if a single build request was
                # made.
                if task.explicit and single_explicit_spec:
                    raise

                if task.explicit:
                    exists_errors.append((pkg_id, str(exc)))

            except KeyboardInterrupt as exc:
                # The build has been terminated with a Ctrl-C so terminate
                # regardless of the number of remaining specs.
                err = 'Failed to install {0} due to {1}: {2}'
                tty.error(err.format(pkg.name, exc.__class__.__name__,
                          str(exc)))
                raise

            except (Exception, SystemExit) as exc:
                self._update_failed(task, True, exc)

                # Best effort installs suppress the exception and mark the
                # package as a failure.
                if (not isinstance(exc, spack.error.SpackError) or
                    not exc.printed):
                    # SpackErrors can be printed by the build process or at
                    # lower levels -- skip printing if already printed.
                    # TODO: sort out this and SpackError.print_context()
                    tty.error('Failed to install {0} due to {1}: {2}'
                              .format(pkg.name, exc.__class__.__name__,
                                      str(exc)))
                # Terminate if requested to do so on the first failure.
                if self.fail_fast:
                    raise InstallError('{0}: {1}'
                                       .format(fail_fast_err, str(exc)))

                # Terminate at this point if the single explicit spec has
                # failed to install.
                if single_explicit_spec and task.explicit:
                    raise

                # Track explicit spec id and error to summarize when done
                if task.explicit:
                    failed_explicits.append((pkg_id, str(exc)))

            finally:
                # Remove the install prefix if anything went wrong during
                # install.
                if not keep_prefix:
                    pkg.remove_prefix()

                # The subprocess *may* have removed the build stage. Mark it
                # not created so that the next time pkg.stage is invoked, we
                # check the filesystem for it.
                pkg.stage.created = False

            # Perform basic task cleanup for the installed spec to
            # include downgrading the write to a read lock
            self._cleanup_task(pkg)

        # Cleanup, which includes releasing all of the read locks
        self._cleanup_all_tasks()

        # Ensure we properly report if one or more explicit specs failed
        # or were not installed when should have been.
        missing = [request.pkg_id for request in self.build_requests if
                   request.install_args.get('install_package') and
                   request.pkg_id not in self.installed]
        if exists_errors or failed_explicits or missing:
            for pkg_id, err in exists_errors:
                tty.error('{0}: {1}'.format(pkg_id, err))

            for pkg_id, err in failed_explicits:
                tty.error('{0}: {1}'.format(pkg_id, err))

            for pkg_id in missing:
                tty.error('{0}: Package was not installed'.format(pkg_id))

            raise InstallError('Installation request failed.  Refer to '
                               'reported errors for failing package(s).')


def build_process(pkg, kwargs):
    """Perform the installation/build of the package.

    This runs in a separate child process, and has its own process and
    python module space set up by build_environment.start_build_process().

    This function's return value is returned to the parent process.
    """
    fake = kwargs.get('fake', False)
    install_source = kwargs.get('install_source', False)
    keep_stage = kwargs.get('keep_stage', False)
    skip_patch = kwargs.get('skip_patch', False)
    unmodified_env = kwargs.get('unmodified_env', {})
    verbose = kwargs.get('verbose', False)

    start_time = time.time()
    if not fake:
        if not skip_patch:
            pkg.do_patch()
        else:
            pkg.do_stage()

    pid = '{0}: '.format(pkg.pid) if tty.show_pid() else ''
    pre = '{0}{1}:'.format(pid, pkg.name)
    pkg_id = package_id(pkg)

    tty.debug('{0} Building {1} [{2}]'
              .format(pre, pkg_id, pkg.build_system_class))

    # get verbosity from do_install() parameter or saved value
    echo = verbose
    if spack.package.PackageBase._verbose is not None:
        echo = spack.package.PackageBase._verbose

    pkg.stage.keep = keep_stage
    with pkg.stage:
        # Run the pre-install hook in the child process after
        # the directory is created.
        spack.hooks.pre_install(pkg.spec)
        if fake:
            _do_fake_install(pkg)
        else:
            source_path = pkg.stage.source_path
            if install_source and os.path.isdir(source_path):
                src_target = os.path.join(pkg.spec.prefix, 'share',
                                          pkg.name, 'src')
                tty.debug('{0} Copying source to {1}'
                          .format(pre, src_target))
                fs.install_tree(pkg.stage.source_path, src_target)

            # Do the real install in the source directory.
            with fs.working_dir(pkg.stage.source_path):
                # Save the build environment in a file before building.
                dump_environment(pkg.env_path)

                for attr in ('configure_args', 'cmake_args'):
                    try:
                        configure_args = getattr(pkg, attr)()
                        configure_args = ' '.join(configure_args)

                        with open(pkg.configure_args_path, 'w') as \
                                args_file:
                            args_file.write(configure_args)

                        break
                    except Exception:
                        pass

                # cache debug settings
                debug_level = tty.debug_level()

                # Spawn a daemon that reads from a pipe and redirects
                # everything to log_path
                with log_output(pkg.log_path, echo, True,
                                env=unmodified_env) as logger:

                    for phase_name, phase_attr in zip(
                            pkg.phases, pkg._InstallPhase_phases):

                        with logger.force_echo():
                            inner_debug_level = tty.debug_level()
                            tty.set_debug(debug_level)
                            tty.msg("{0} Executing phase: '{1}'"
                                    .format(pre, phase_name))
                            tty.set_debug(inner_debug_level)

                        # Redirect stdout and stderr to daemon pipe
                        phase = getattr(pkg, phase_attr)
                        phase(pkg.spec, pkg.prefix)

            echo = logger.echo
            log(pkg)

        # Run post install hooks before build stage is removed.
        spack.hooks.post_install(pkg.spec)

    # Stop the timer
    pkg._total_time = time.time() - start_time
    build_time = pkg._total_time - pkg._fetch_time

    tty.msg('{0} Successfully installed {1}'.format(pre, pkg_id),
            'Fetch: {0}.  Build: {1}.  Total: {2}.'
            .format(_hms(pkg._fetch_time), _hms(build_time),
                    _hms(pkg._total_time)))
    _print_installed_pkg(pkg.prefix)

    # preserve verbosity across runs
    return echo


class BuildTask(object):
    """Class for representing the build task for a package."""

    def __init__(self, pkg, request, compiler, start, attempts, status,
                 installed):
        """
        Instantiate a build task for a package.

        Args:
            pkg (Package): the package to be built and installed
            request (BuildRequest or None): the associated install request
                 where ``None`` can be used to indicate the package was
                 explicitly requested by the user
            compiler (bool): whether task is for a bootstrap compiler
            start (int): the initial start time for the package, in seconds
            attempts (int): the number of attempts to install the package
            status (str): the installation status
            installed (list of str): the identifiers of packages that have
                been installed so far
        """

        # Ensure dealing with a package that has a concrete spec
        if not isinstance(pkg, spack.package.PackageBase):
            raise ValueError("{0} must be a package".format(str(pkg)))

        self.pkg = pkg
        if not self.pkg.spec.concrete:
            raise ValueError("{0} must have a concrete spec"
                             .format(self.pkg.name))

        # The "unique" identifier for the task's package
        self.pkg_id = package_id(self.pkg)

        # The explicit build request associated with the package
        if not isinstance(request, BuildRequest):
            raise ValueError("{0} must have a build request".format(str(pkg)))

        self.request = request

        # Initialize the status to an active state.  The status is used to
        # ensure priority queue invariants when tasks are "removed" from the
        # queue.
        if status == STATUS_REMOVED:
            msg = "Cannot create a build task for {0} with status '{1}'"
            raise InstallError(msg.format(self.pkg_id, status))

        self.status = status

        # Package is associated with a bootstrap compiler
        self.compiler = compiler

        # The initial start time for processing the spec
        self.start = start

        # Set of dependents, which needs to include the requesting package
        # to support tracking of parallel, multi-spec, environment installs.
        self.dependents = set(get_dependent_ids(self.pkg.spec))

        tty.debug(
            'Pkg id {0} has the following dependents:'.format(self.pkg_id))
        for dep_id in self.dependents:
            tty.debug('- {0}'.format(dep_id))

        # Set of dependencies
        #
        # Be consistent wrt use of dependents and dependencies.  That is,
        # if use traverse for transitive dependencies, then must remove
        # transitive dependents on failure.
        deptypes = self.request.get_deptypes(self.pkg)
        self.dependencies = set(package_id(d.package) for d in
                                self.pkg.spec.dependencies(deptype=deptypes)
                                if package_id(d.package) != self.pkg_id)

        # Handle bootstrapped compiler
        #
        # The bootstrapped compiler is not a dependency in the spec, but it is
        # a dependency of the build task. Here we add it to self.dependencies
        compiler_spec = self.pkg.spec.compiler
        arch_spec = self.pkg.spec.architecture
        if not spack.compilers.compilers_for_spec(compiler_spec,
                                                  arch_spec=arch_spec):
            # The compiler is in the queue, identify it as dependency
            dep = spack.compilers.pkg_spec_for_compiler(compiler_spec)
            dep.constrain('platform=%s' % str(arch_spec.platform))
            dep.constrain('os=%s' % str(arch_spec.os))
            dep.constrain('target=%s:' %
                          arch_spec.target.microarchitecture.family.name)
            dep.concretize()
            dep_id = package_id(dep.package)
            self.dependencies.add(dep_id)

        # List of uninstalled dependencies, which is used to establish
        # the priority of the build task.
        #
        self.uninstalled_deps = set(pkg_id for pkg_id in self.dependencies if
                                    pkg_id not in installed)

        # Ensure key sequence-related properties are updated accordingly.
        self.attempts = 0
        self._update()

    def __eq__(self, other):
        return self.key == other.key

    def __ge__(self, other):
        return self.key >= other.key

    def __gt__(self, other):
        return self.key > other.key

    def __le__(self, other):
        return self.key <= other.key

    def __lt__(self, other):
        return self.key < other.key

    def __ne__(self, other):
        return self.key != other.key

    def __repr__(self):
        """Returns a formal representation of the build task."""
        rep = '{0}('.format(self.__class__.__name__)
        for attr, value in self.__dict__.items():
            rep += '{0}={1}, '.format(attr, value.__repr__())
        return '{0})'.format(rep.strip(', '))

    def __str__(self):
        """Returns a printable version of the build task."""
        dependencies = '#dependencies={0}'.format(len(self.dependencies))
        return ('priority={0}, status={1}, start={2}, {3}'
                .format(self.priority, self.status, self.start, dependencies))

    def _update(self):
        """Update properties associated with a new instance of a task."""
        # Number of times the task has/will be queued
        self.attempts = self.attempts + 1

        # Ensure the task gets a unique sequence number to preserve the
        # order in which it is added.
        self.sequence = next(_counter)

    def add_dependent(self, pkg_id):
        """
        Ensure the dependent package id is in the task's list so it will be
        properly updated when this package is installed.

        Args:
            pkg_id (str):  package identifier of the dependent package
        """
        if pkg_id != self.pkg_id and pkg_id not in self.dependents:
            tty.debug('Adding {0} as a dependent of {1}'
                      .format(pkg_id, self.pkg_id))
            self.dependents.add(pkg_id)

    def flag_installed(self, installed):
        """
        Ensure the dependency is not considered to still be uninstalled.

        Args:
            installed (list of str): the identifiers of packages that have
                been installed so far
        """
        now_installed = self.uninstalled_deps & set(installed)
        for pkg_id in now_installed:
            self.uninstalled_deps.remove(pkg_id)
            tty.debug('{0}: Removed {1} from uninstalled deps list: {2}'
                      .format(self.pkg_id, pkg_id, self.uninstalled_deps))

    @property
    def explicit(self):
        """The package was explicitly requested by the user."""
        return self.pkg == self.request.pkg

    @property
    def key(self):
        """The key is the tuple (# uninstalled dependencies, sequence)."""
        return (self.priority, self.sequence)

    def next_attempt(self, installed):
        """Create a new, updated task for the next installation attempt."""
        task = copy.copy(self)
        task._update()
        task.start = self.start or time.time()
        task.flag_installed(installed)
        return task

    @property
    def priority(self):
        """The priority is based on the remaining uninstalled dependencies."""
        return len(self.uninstalled_deps)


class BuildRequest(object):
    """Class for representing an installation request."""

    def __init__(self, pkg, install_args):
        """
        Instantiate a build request for a package.

        Args:
            pkg (Package): the package to be built and installed
            install_args (dict): the install arguments associated with ``pkg``
        """
        # Ensure dealing with a package that has a concrete spec
        if not isinstance(pkg, spack.package.PackageBase):
            raise ValueError("{0} must be a package".format(str(pkg)))

        self.pkg = pkg
        if not self.pkg.spec.concrete:
            raise ValueError("{0} must have a concrete spec"
                             .format(self.pkg.name))

        # Cache the package phase options with the explicit package,
        # popping the options to ensure installation of associated
        # dependencies is NOT affected by these options.
        self.pkg.stop_before_phase = install_args.pop('stop_before', None)
        self.pkg.last_phase = install_args.pop('stop_at', None)

        # Cache the package id for convenience
        self.pkg_id = package_id(pkg)

        # Save off the original install arguments plus standard defaults
        # since they apply to the requested package *and* dependencies.
        self.install_args = install_args if install_args else {}
        self._add_default_args()

        # Cache overwrite information
        self.overwrite = set(self.install_args.get('overwrite', []))
        self.overwrite_time = time.time()

        # Save off dependency package ids for quick checks since traversals
        # are not able to return full dependents for all packages across
        # environment specs.
        deptypes = self.get_deptypes(self.pkg)
        self.dependencies = set(package_id(d.package) for d in
                                self.pkg.spec.dependencies(deptype=deptypes)
                                if package_id(d.package) != self.pkg_id)

    def __repr__(self):
        """Returns a formal representation of the build request."""
        rep = '{0}('.format(self.__class__.__name__)
        for attr, value in self.__dict__.items():
            rep += '{0}={1}, '.format(attr, value.__repr__())
        return '{0})'.format(rep.strip(', '))

    def __str__(self):
        """Returns a printable version of the build request."""
        return 'package={0}, install_args={1}' \
            .format(self.pkg.name, self.install_args)

    def _add_default_args(self):
        """Ensure standard install options are set to at least the default."""
        for arg, default in [('cache_only', False),
                             ('context', 'build'),  # installs *always* build
                             ('dirty', False),
                             ('fail_fast', False),
                             ('fake', False),
                             ('full_hash_match', False),
                             ('install_deps', True),
                             ('install_package', True),
                             ('install_source', False),
                             ('keep_prefix', False),
                             ('keep_stage', False),
                             ('restage', False),
                             ('skip_patch', False),
                             ('tests', False),
                             ('unsigned', False),
                             ('use_cache', True),
                             ('verbose', False), ]:
            _ = self.install_args.setdefault(arg, default)

    def get_deptypes(self, pkg):
        """Determine the required dependency types for the associated package.

        Args:
            pkg (PackageBase): explicit or implicit package being installed

        Returns:
            (tuple) required dependency type(s) for the package
        """
        deptypes = ['link', 'run']
        include_build_deps = self.install_args.get('include_build_deps')
        if not self.install_args.get('cache_only') or include_build_deps:
            deptypes.append('build')
        if self.run_tests(pkg):
            deptypes.append('test')
        return tuple(sorted(deptypes))

    def has_dependency(self, dep_id):
        """Returns ``True`` if the package id represents a known dependency
           of the requested package, ``False`` otherwise."""
        return dep_id in self.dependencies

    def run_tests(self, pkg):
        """Determine if the tests should be run for the provided packages

        Args:
            pkg (PackageBase): explicit or implicit package being installed

        Returns:
            (bool) ``True`` if they should be run; ``False`` otherwise
        """
        tests = self.install_args.get('tests', False)
        return tests is True or (tests and pkg.name in tests)

    @property
    def spec(self):
        """The specification associated with the package."""
        return self.pkg.spec

    def traverse_dependencies(self):
        """
        Yield any dependencies of the appropriate type(s)

        Yields:
            (Spec) The next child spec in the DAG
        """
        get_spec = lambda s: s.spec

        deptypes = self.get_deptypes(self.pkg)
        tty.debug('Processing dependencies for {0}: {1}'
                  .format(self.pkg_id, deptypes))
        for dspec in self.spec.traverse_edges(
                deptype=deptypes, order='post', root=False,
                direction='children'):
            yield get_spec(dspec)


class InstallError(spack.error.SpackError):
    """Raised when something goes wrong during install or uninstall."""

    def __init__(self, message, long_msg=None):
        super(InstallError, self).__init__(message, long_msg)


class BadInstallPhase(InstallError):
    """Raised for an install phase option is not allowed for a package."""

    def __init__(self, pkg_name, phase):
        super(BadInstallPhase, self).__init__(
            '\'{0}\' is not a valid phase for package {1}'
            .format(phase, pkg_name))


class ExternalPackageError(InstallError):
    """Raised by install() when a package is only for external use."""


class InstallLockError(InstallError):
    """Raised during install when something goes wrong with package locking."""


class UpstreamPackageError(InstallError):
    """Raised during install when something goes wrong with an upstream
       package."""
