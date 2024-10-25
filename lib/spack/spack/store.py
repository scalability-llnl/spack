# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Components that manage Spack's installation tree.

An install tree, or "build store" consists of two parts:

  1. A package database that tracks what is installed.
  2. A directory layout that determines how the installations
     are laid out.

The store contains all the install prefixes for packages installed by
Spack.  The simplest store could just contain prefixes named by DAG hash,
but we use a fancier directory layout to make browsing the store and
debugging easier.

"""
import contextlib
import os
import pathlib
import re
import uuid
from typing import Any, Callable, Dict, Generator, List, Optional, Union

import llnl.util.lang
from llnl.util import tty

import spack.config
import spack.database
import spack.directory_layout
import spack.error
import spack.paths
import spack.spec
import spack.store
import spack.util.path

#: default installation root, relative to the Spack install path
DEFAULT_INSTALL_TREE_ROOT = os.path.join(spack.paths.opt_path, "spack")


ConfigurationType = Union["spack.config.Configuration", "llnl.util.lang.Singleton"]


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
    #     root: /path/to/root
    #     padding: 128
    #     projections:
    #       all: '{name}-{version}'

    install_tree = config_dict.get("install_tree", {})

    padded_length = False
    if isinstance(install_tree, str):
        tty.warn("Using deprecated format for configuring install_tree")
        unpadded_root = install_tree
        unpadded_root = spack.util.path.canonicalize_path(unpadded_root)
        # construct projection from previous values for backwards compatibility
        all_projection = config_dict.get(
            "install_path_scheme", spack.directory_layout.default_projections["all"]
        )

        projections = {"all": all_projection}
    else:
        unpadded_root = install_tree.get("root", DEFAULT_INSTALL_TREE_ROOT)
        unpadded_root = spack.util.path.canonicalize_path(unpadded_root)

        padded_length = install_tree.get("padded_length", False)
        if padded_length is True:
            padded_length = spack.util.path.get_system_path_max()
            padded_length -= spack.util.path.SPACK_MAX_INSTALL_PATH_LENGTH

        projections = install_tree.get("projections", spack.directory_layout.default_projections)

        path_scheme = config_dict.get("install_path_scheme", None)
        if path_scheme:
            tty.warn(
                "Deprecated config value 'install_path_scheme' ignored"
                " when using new install_tree syntax"
            )

    # Handle backwards compatibility for padding
    old_pad = re.search(r"\$padding(:\d+)?|\${padding(:\d+)?}", unpadded_root)
    if old_pad:
        if padded_length:
            msg = "Ignoring deprecated padding option in install_tree root "
            msg += "because new syntax padding is present."
            tty.warn(msg)
        else:
            unpadded_root = unpadded_root.replace(old_pad.group(0), "")
            if old_pad.group(1) or old_pad.group(2):
                length_group = 2 if "{" in old_pad.group(0) else 1
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

    return root, unpadded_root, projections


class Store:
    """A store is a path full of installed Spack packages.

    Stores consist of packages installed according to a ``DirectoryLayout``, along with a database
    of their contents.

    The directory layout controls what paths look like and how Spack ensures that each unique spec
    gets its own unique directory (or not, though we don't recommend that).

    The database is a single file that caches metadata for the entire Spack installation. It
    prevents us from having to spider the install tree to figure out what's there.

    The store is also able to lock installation prefixes, and to mark installation failures.

    Args:
        root: path to the root of the install tree
        unpadded_root: path to the root of the install tree without padding. The sbang script has
            to be installed here to work with padded roots
        projections: expression according to guidelines that describes how to construct a path to
            a package prefix in this store
        hash_length: length of the hashes used in the directory layout. Spec hash suffixes will be
            truncated to this length
        upstreams: optional list of upstream databases
        lock_cfg: lock configuration for the database
    """

    def __init__(
        self,
        root: str,
        unpadded_root: Optional[str] = None,
        projections: Optional[Dict[str, str]] = None,
        hash_length: Optional[int] = None,
        upstreams: Optional[List[spack.database.Database]] = None,
        lock_cfg: spack.database.LockConfiguration = spack.database.NO_LOCK,
    ) -> None:
        self.root = root
        self.unpadded_root = unpadded_root or root
        self.projections = projections
        self.hash_length = hash_length
        self.upstreams = upstreams
        self.lock_cfg = lock_cfg
        self.layout = spack.directory_layout.DirectoryLayout(
            root, projections=projections, hash_length=hash_length
        )
        self.db = spack.database.Database(
            root, upstream_dbs=upstreams, lock_cfg=lock_cfg, layout=self.layout
        )

        timeout_format_str = (
            f"{str(lock_cfg.package_timeout)}s" if lock_cfg.package_timeout else "No timeout"
        )
        tty.debug("PACKAGE LOCK TIMEOUT: {0}".format(str(timeout_format_str)))

        self.prefix_locker = spack.database.SpecLocker(
            spack.database.prefix_lock_path(root), default_timeout=lock_cfg.package_timeout
        )
        self.failure_tracker = spack.database.FailureTracker(
            self.root, default_timeout=lock_cfg.package_timeout
        )

    def reindex(self) -> None:
        """Convenience function to reindex the store DB with its own layout."""
        return self.db.reindex()

    def __reduce__(self):
        return Store, (
            self.root,
            self.unpadded_root,
            self.projections,
            self.hash_length,
            self.upstreams,
            self.lock_cfg,
        )


def create(configuration: ConfigurationType) -> Store:
    """Create a store from the configuration passed as input.

    Args:
        configuration: configuration to create a store.
    """
    configuration = configuration or spack.config.CONFIG
    config_dict = configuration.get("config")
    root, unpadded_root, projections = parse_install_tree(config_dict)
    hash_length = configuration.get("config:install_hash_length")

    install_roots = [
        install_properties["install_tree"]
        for install_properties in configuration.get("upstreams", {}).values()
    ]
    upstreams = _construct_upstream_dbs_from_install_roots(install_roots)

    return Store(
        root=root,
        unpadded_root=unpadded_root,
        projections=projections,
        hash_length=hash_length,
        upstreams=upstreams,
        lock_cfg=spack.database.lock_configuration(configuration),
    )


def _create_global() -> Store:
    result = create(configuration=spack.config.CONFIG)
    return result


#: Singleton store instance
STORE: Union[Store, llnl.util.lang.Singleton] = llnl.util.lang.Singleton(_create_global)


def reinitialize():
    """Restore globals to the same state they would have at start-up. Return a token
    containing the state of the store before reinitialization.
    """
    global STORE

    token = STORE
    STORE = llnl.util.lang.Singleton(_create_global)

    return token


def restore(token):
    """Restore the environment from a token returned by reinitialize"""
    global STORE
    STORE = token


def _construct_upstream_dbs_from_install_roots(
    install_roots: List[str],
) -> List[spack.database.Database]:
    accumulated_upstream_dbs: List[spack.database.Database] = []
    for install_root in reversed(install_roots):
        upstream_dbs = list(accumulated_upstream_dbs)
        next_db = spack.database.Database(
            spack.util.path.canonicalize_path(install_root),
            is_upstream=True,
            upstream_dbs=upstream_dbs,
        )
        next_db._read()
        accumulated_upstream_dbs.insert(0, next_db)

    return accumulated_upstream_dbs


def find(
    constraints: Union[str, List[str], List["spack.spec.Spec"]],
    multiple: bool = False,
    query_fn: Optional[Callable[[Any], List["spack.spec.Spec"]]] = None,
    **kwargs,
) -> List["spack.spec.Spec"]:
    """Returns a list of specs matching the constraints passed as inputs.

    At least one spec per constraint must match, otherwise the function
    will error with an appropriate message.

    By default, this function queries the current store, but a custom query
    function can be passed to hit any other source of concretized specs
    (e.g. a binary cache).

    The query function must accept a spec as its first argument.

    Args:
        constraints: spec(s) to be matched against installed packages
        multiple: if True multiple matches per constraint are admitted
        query_fn (Callable): query function to get matching specs. By default,
            ``spack.store.STORE.db.query``
        **kwargs: keyword arguments forwarded to the query function
    """
    if isinstance(constraints, str):
        constraints = [spack.spec.Spec(constraints)]

    matching_specs: List[spack.spec.Spec] = []
    errors = []
    query_fn = query_fn or spack.store.STORE.db.query
    for spec in constraints:
        current_matches = query_fn(spec, **kwargs)

        # For each spec provided, make sure it refers to only one package.
        if not multiple and len(current_matches) > 1:
            msg_fmt = '"{0}" matches multiple packages: [{1}]'
            errors.append(msg_fmt.format(spec, ", ".join([m.format() for m in current_matches])))

        # No installed package matches the query
        if len(current_matches) == 0 and spec is not any:
            msg_fmt = '"{0}" does not match any installed packages'
            errors.append(msg_fmt.format(spec))

        matching_specs.extend(current_matches)

    if errors:
        raise MatchError(
            message="errors occurred when looking for specs in the store",
            long_message="\n".join(errors),
        )

    return matching_specs


def specfile_matches(filename: str, **kwargs) -> List["spack.spec.Spec"]:
    """Same as find but reads the query from a spec file.

    Args:
        filename: YAML or JSON file from which to read the query.
        **kwargs: keyword arguments forwarded to "find"
    """
    query = [spack.spec.Spec.from_specfile(filename)]
    return spack.store.find(query, **kwargs)


def ensure_singleton_created() -> None:
    """Ensures the lazily evaluated singleton is created"""
    _ = STORE.db


@contextlib.contextmanager
def use_store(
    path: Union[str, pathlib.Path], extra_data: Optional[Dict[str, Any]] = None
) -> Generator[Store, None, None]:
    """Use the store passed as argument within the context manager.

    Args:
        path: path to the store.
        extra_data: extra configuration under "config:install_tree" to be
            taken into account.

    Yields:
        Store object associated with the context manager's store
    """
    global STORE

    assert not isinstance(path, Store), "cannot pass a store anymore"
    scope_name = "use-store-{}".format(uuid.uuid4())
    data = {"root": str(path)}
    if extra_data:
        data.update(extra_data)

    # Swap the store with the one just constructed and return it
    spack.config.CONFIG.push_scope(
        spack.config.InternalConfigScope(name=scope_name, data={"config": {"install_tree": data}})
    )
    temporary_store = create(configuration=spack.config.CONFIG)
    original_store, STORE = STORE, temporary_store

    try:
        yield temporary_store
    finally:
        # Restore the original store
        STORE = original_store
        spack.config.CONFIG.remove_scope(scope_name=scope_name)


class MatchError(spack.error.SpackError):
    """Error occurring when trying to match specs in store against a constraint"""
