# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Components that manage Spack's installation tree.

An install tree, or "build store" consists of two parts:

  1. A package database that tracks what is installed.
  2. A directory layout that determines how the installations
     are laid out.

The store contains all the install prefixes for packages installed by
Spack. The simplest store could just contain prefixes named by DAG hash,
but we use a fancier directory layout to make browsing the store and
debugging easier.

The directory layout is currently hard-coded to be a YAMLDirectoryLayout,
so called because it stores build metadata within each prefix, in
`spec.yaml` files. In future versions of Spack we may consider allowing
install trees to define their own layouts with some per-tree
configuration.

"""
import contextlib
import os
import re
import six
import stat as st

import llnl.util.lang
import llnl.util.tty as tty

import spack.paths
import spack.config
import spack.util.path
import spack.database
import spack.directory_layout
import llnl.util.filesystem as fs

#: default installation root, relative to the Spack install path
default_install_tree_root = os.path.join(spack.paths.opt_path, 'spack')

install_root = None


def parse_install_tree(config_dict):
    """Parse config settings and return values relevant to the store object.

    Arguments:
        config_dict (dict): dictionary of config values, as returned from
            spack.config.get('config')

    Returns:
        (tuple): triple of the install tree root, the unpadded install tree
            root (before padding was applied), and the projections for the
            install tree

    Encapsulate backwards compatibility capabilities for install_tree
    and deprecated values that are now parsed as part of install_tree.
    """
    # The following two configs are equivalent, the first being the old format
    # and the second the new format. The new format is also more flexible.

    # config:
    #   install_tree: /path/to/root$padding:128
    #   install_path_scheme: '{name}-{version}'

    # config:
    #   install_tree:
    #     install_tree_name:
    #       root: /path/to/root
    #       padding: 128
    #       projections:
    #         all: '{name}-{version}'
    #       permissions:
    #         read: world
    #         write: user

    # Dictionaries of all install trees
    install_trees = spack.config.get('config:install_trees')
    shared_install_trees = spack.config.get('config:shared_install_trees')

    # Tests if non-default install root is specified
    if install_root:
        # Determines if install_root exists
        if install_root in install_trees:
            install_tree = install_trees[install_root]
        elif shared_install_trees and (install_root in shared_install_trees):
            install_tree = shared_install_trees[install_root]
        else:
            tty.die("Specified install tree does not exist: {0}"
                    .format(install_root))
    elif shared_install_trees:
        # If no install tree is specified and there are shared install trees,
        # then we are in user mode, and the install tree is in ~
        install_tree = install_trees['user']
    else:
        # If this is not a shared spack instance, then by default we will place
        # the install prefix inside the Spack tree
        if install_trees:
            install_tree = install_trees['spack-root']
        elif spack.config.get('config:install_tree'):
            install_tree = spack.config.get('config:install_tree')
        else:
            tty.die('No supported install tree formats found')

    padded_length = False
    if isinstance(install_tree, six.string_types):
        tty.warn("Using deprecated format for configuring install_tree")
        unpadded_root = install_tree
        unpadded_root = spack.util.path.canonicalize_path(unpadded_root)
        # construct projection from previous values for backwards compatibility
        all_projection = config_dict.get(
            'install_path_scheme',
            spack.directory_layout.default_projections['all'])

        projections = {'all': all_projection}
    else:
        # Sets install tree permissions
        set_install_tree_permissions(install_tree)

        unpadded_root = install_tree.get('root', default_install_tree_root)
        unpadded_root = spack.util.path.canonicalize_path(unpadded_root)

        padded_length = install_tree.get('padded_length', False)
        if padded_length is True:
            padded_length = spack.util.path.get_system_path_max()
            padded_length -= spack.util.path.SPACK_MAX_INSTALL_PATH_LENGTH

        projections = install_tree.get(
            'projections', spack.directory_layout.default_projections)

        path_scheme = config_dict.get('install_path_scheme', None)
        if path_scheme:
            tty.warn("Deprecated config value 'install_path_scheme' ignored"
                     " when using new install_tree syntax")

    # Handle backwards compatibility for padding
    old_pad = re.search(r'\$padding(:\d+)?|\${padding(:\d+)?}', unpadded_root)
    if old_pad:
        if padded_length:
            msg = "Ignoring deprecated padding option in install_tree root "
            msg += "because new syntax padding is present."
            tty.warn(msg)
        else:
            unpadded_root = unpadded_root.replace(old_pad.group(0), '')
            if old_pad.group(1) or old_pad.group(2):
                length_group = 2 if '{' in old_pad.group(0) else 1
                padded_length = int(old_pad.group(length_group)[1:])
            else:
                padded_length = spack.util.path.get_system_path_max()
                padded_length -= spack.util.path.SPACK_MAX_INSTALL_PATH_LENGTH

    unpadded_root = unpadded_root.rstrip(os.path.sep)

    if padded_length:
        root = spack.util.path.add_padding(unpadded_root, padded_length)
        if len(root) != padded_length:
            msg = "Cannot pad %s to %s characters." % (root, padded_length)
            msg += " It is already %s characters long" % len(root)
            tty.warn(msg)
    else:
        root = unpadded_root

    return (root, unpadded_root, projections)


def set_install_tree_permissions(install_tree):
    """Sets the permissions configured for the install tree.
    If install_root already exists then permissions are not set.

    Arguments:
        install_tree (dict): install tree dictionary with install
            tree information
    """
    root = install_tree.get('root')
    permissions = install_tree.get('permissions', {})

    # Special exception for test paths
    # Permissions should not be set during tests
    try:
        root = spack.util.path.canonicalize_path(root)

        # Ensures path is writeable (fails in some tests)
        if not os.access(root, os.W_OK):
            return
    except Exception:
        tty.debug('Invalid path, skipping setting permissions')
        return

    if os.path.exists(spack.util.path.canonicalize_path(root)):
        tty.debug('Install root already exists, skipping setting permissions')
        return
    else:
        os.mkdir(spack.util.path.canonicalize_path(root))

    # Get read permissions level
    if permissions.get('read'):
        readable = permissions.get('read')
    else:
        readable = 'world'

    # Get write permissions level
    if permissions.get('write'):
        writable = permissions.get('write')
    else:
        writable = 'user'

    # Get group (if specified)
    if permissions.get('group'):
        group = permissions.get('group')
    else:
        group = None

    perms = st.S_IRWXU
    if readable in ('world', 'group'):  # world includes group
        perms |= st.S_IRGRP | st.S_IXGRP
    if readable == 'world':
        perms |= st.S_IROTH | st.S_IXOTH

    if writable in ('world', 'group'):
        if readable == 'user':
            tty.die('Writable permissions may not be more' +
                    ' permissive than readable permissions.\n')
        perms |= st.S_IWGRP
    if writable == 'world':
        if readable != 'world':
            tty.die('Writable permissions may not be more' +
                    ' permissive than readable permissions.\n')
        perms |= st.S_IWOTH

    # Preserve higher-order bits of file permissions
    perms |= os.st(root).st_mode & (st.S_ISUID | st.S_ISGID | st.S_ISVTX)

    # Do not let users create world/group writable suid binaries
    if perms & st.S_ISUID:
        if perms & st.S_IWOTH:
            tty.die("Attempting to set suid with world writable")
        if perms & st.S_IWGRP:
            tty.die("Attempting to set suid with group writable")
    # Or world writable sgid binaries
    if perms & st.S_ISGID:
        if perms & st.S_IWOTH:
            tty.die("Attempting to set sgid with world writable")

    fs.chmod_x(root, perms)

    if group:
        fs.chgrp(root, group)


class Store(object):
    """A store is a path full of installed Spack packages.

    Stores consist of packages installed according to a
    ``DirectoryLayout``, along with an index, or _database_ of their
    contents. The directory layout controls what paths look like and how
    Spack ensures that each unique spec gets its own unique directory (or
    not, though we don't recommend that). The database is a single file
    that caches metadata for the entire Spack installation. It prevents
    us from having to spider the install tree to figure out what's there.

    Args:
        root (str): path to the root of the install tree
        unpadded_root (str): path to the root of the install tree without
            padding; the sbang script has to be installed here to work with
            padded roots
        path_scheme (str): expression according to guidelines in
            ``spack.util.path`` that describes how to construct a path to
            a package prefix in this store
        hash_length (int): length of the hashes used in the directory
            layout; spec hash suffixes will be truncated to this length
    """
    def __init__(
            self, root, unpadded_root=None,
            projections=None, hash_length=None):
        self.root = root
        self.unpadded_root = unpadded_root or root
        upstream_dbs = upstream_dbs_from_pointers(root)
        self.projections = projections
        self.hash_length = hash_length
        self.db = spack.database.Database(
            root, upstream_dbs=upstream_dbs)
        self.layout = spack.directory_layout.YamlDirectoryLayout(
            root, projections=projections, hash_length=hash_length)

    def reindex(self):
        """Convenience function to reindex the store DB with its own layout."""
        return self.db.reindex(self.layout)

    def serialize(self):
        """Return a pickle-able object that can be used to reconstruct
        a store.
        """
        return (
            self.root, self.unpadded_root, self.projections, self.hash_length
        )

    @staticmethod
    def deserialize(token):
        """Return a store reconstructed from a token created by
        the serialize method.

        Args:
            token: return value of the serialize method

        Returns:
            Store object reconstructed from the token
        """
        return Store(*token)


def _store():
    """Get the singleton store instance."""
    config_dict = spack.config.get('config')
    root, unpadded_root, projections = parse_install_tree(config_dict)
    hash_length = spack.config.get('config:install_hash_length')

    return Store(root=root,
                 unpadded_root=unpadded_root,
                 projections=projections,
                 hash_length=hash_length)


#: Singleton store instance
store = llnl.util.lang.Singleton(_store)


def _store_root():
    return store.root


def _store_unpadded_root():
    return store.unpadded_root


def _store_db():
    return store.db


def _store_layout():
    return store.layout


# convenience accessors for parts of the singleton store
root = llnl.util.lang.LazyReference(_store_root)
unpadded_root = llnl.util.lang.LazyReference(_store_unpadded_root)
db = llnl.util.lang.LazyReference(_store_db)
layout = llnl.util.lang.LazyReference(_store_layout)


def upstream_set(root):
    upstream_root_description = os.path.join(root, 'upstream-spack')
    return os.path.exists(upstream_root_description)


def initialize_upstream_pointer_if_unset(root, init_upstream_root):
    """Set the installation to point to the specified upstream."""
    if not os.path.exists(root):
        fs.mkdirp(root)
    upstream_root_description = os.path.join(root, 'upstream-spack')
    if not os.path.exists(upstream_root_description):
        with open(upstream_root_description, 'w') as f:
            f.write(init_upstream_root)


def upstream_install_roots(root):
    # Each installation root directory contains a file that points to the
    # upstream installation used (if any). This constructs a sequence of
    # upstream installations by recursively following these references.
    upstream_root_description = os.path.join(root, 'upstream-spack')
    install_roots = list()
    while os.path.exists(upstream_root_description):
        with open(upstream_root_description, 'r') as f:
            upstream_root = f.read()
            install_roots.append(upstream_root)
            upstream_root_description = os.path.join(
                upstream_root, 'upstream-spack')
    return install_roots


def upstream_dbs_from_pointers(root):
    return _construct_upstream_dbs_from_install_roots(
        upstream_install_roots(root))


def upstream_dbs_from_config():
    other_spack_instances = spack.config.get('upstreams', {})
    install_roots = []
    for install_properties in other_spack_instances.values():
        install_roots.append(spack.util.path.canonicalize_path(
                             install_properties['install_tree']))

    return _construct_upstream_dbs_from_install_roots(install_roots)


def _construct_upstream_dbs_from_install_roots(
        install_roots, _test=False):
    accumulated_upstream_dbs = []
    for install_root in reversed(install_roots):
        upstream_dbs = list(accumulated_upstream_dbs)
        next_db = spack.database.Database(
            install_root.strip(), is_upstream=True, upstream_dbs=upstream_dbs)
        next_db._fail_when_missing_deps = _test
        next_db._read()
        accumulated_upstream_dbs.insert(0, next_db)

    return accumulated_upstream_dbs


@contextlib.contextmanager
def use_store(store_or_path):
    """Use the store passed as argument within the context manager.

    Args:
        store_or_path: either a Store object ot a path to where the store resides

    Returns:
        Store object associated with the context manager's store
    """
    global store, db, layout, root, unpadded_root

    # Normalize input arguments
    temporary_store = store_or_path
    if not isinstance(store_or_path, Store):
        temporary_store = Store(store_or_path)

    # Swap the store with the one just constructed and return it
    _ = store.db
    original_store, store = store, temporary_store
    db, layout = store.db, store.layout
    root, unpadded_root = store.root, store.unpadded_root

    yield temporary_store

    # Restore the original store
    store = original_store
    db, layout = original_store.db, original_store.layout
    root, unpadded_root = original_store.root, original_store.unpadded_root
