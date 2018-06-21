##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
"""Components that manage Spack's installation tree.

An install tree, or "build store" consists of two parts:

  1. A package database that tracks what is installed.
  2. A directory layout that determines how the installations
     are laid out.

The store contains all the install prefixes for packages installed by
Spack.  The simplest store could just contain prefixes named by DAG hash,
but we use a fancier directory layout to make browsing the store and
debugging easier.

The directory layout is currently hard-coded to be a YAMLDirectoryLayout,
so called because it stores build metadata within each prefix, in
`spec.yaml` files. In future versions of Spack we may consider allowing
install trees to define their own layouts with some per-tree
configuration.

"""
import os

import llnl.util.lang

import spack.paths
import spack.config
import spack.util.path
import spack.database
import spack.directory_layout

#: default installation root, relative to the Spack install path
default_root = os.path.join(spack.paths.opt_path, 'spack')


class Store(object):
    """A store is a path full of installed Spack packages.

    Stores consist of packages installed according to a
    ``DirectoryLayout``, along with an index, or _database_ of their
    contents.  The directory layout controls what paths look like and how
    Spack ensures that each uniqe spec gets its own unique directory (or
    not, though we don't recommend that). The database is a signle file
    that caches metadata for the entire Spack installation.  It prevents
    us from having to spider the install tree to figure out what's there.

    Args:
        root (str): path to the root of the install tree
        path_scheme (str): expression according to guidelines in
            ``spack.util.path`` that describes how to construct a path to
            a package prefix in this store
        hash_length (int): length of the hashes used in the directory
            layout; spec hash suffixes will be truncated to this length
    """
    def __init__(self, root, path_scheme=None, hash_length=None):
        self.root = root
        self.layout = spack.directory_layout.YamlDirectoryLayout(
            root, hash_len=hash_length, path_scheme=path_scheme)
        self.extensions = spack.directory_layout.YamlExtensionsLayout(
            root, self.layout)

        self.chain_prefixes = spack.config.get('config:chain_prefixes', [])
        self.parent_prefixes = []
        for prefix in self.chain_prefixes:
            if prefix == spack.prefix:
                break
            self.parent_prefixes.append(prefix)
        self.parent_install_trees = spack.config.get('config:parent_install_trees',
                                  [os.path.join(prefix, 'opt', 'spack') for prefix in self.parent_prefixes])
        if not isinstance(self.parent_install_trees, (list, tuple)):
            self.parent_install_trees = [self.parent_install_trees]
        if self.parent_install_trees == [None]:
            self.parent_install_trees = []
        self.parent_dbs = [None]
        self.parent_layouts = [None]
        for parent_install_tree in self.parent_install_trees:
            parent_root = spack.util.path.canonicalize_path(parent_install_tree)
            if parent_root == self.root:
                break
            self.parent_dbs.append(Database(parent_root, parent_db=parent_dbs[-1]))
            self.parent_layouts.append(
                spack.directory_layout.YamlDirectoryLayout(parent_root,
                                    hash_len=spack.config.get('config:install_hash_length'),
                                    path_scheme=spack.config.get('config:install_path_scheme'),
                                    parent_layout=parent_layouts[-1]))
        self.db = spack.database.Database(root, parent_db=parent_dbs[-1])

    def reindex(self):
        """Convenience function to reindex the store DB with its own layout."""
        return self.db.reindex(self.layout)


def _store():
    """Get the singleton store instance."""
    root = spack.config.get('config:install_tree', default_root)
    root = spack.util.path.canonicalize_path(root)

    return Store(root,
                 spack.config.get('config:install_path_scheme'),
                 spack.config.get('config:install_hash_length'))


#: Singleton store instance
store = llnl.util.lang.Singleton(_store)

# convenience accessors for parts of the singleton store
root = llnl.util.lang.LazyReference(lambda: store.root)
db = llnl.util.lang.LazyReference(lambda: store.db)
layout = llnl.util.lang.LazyReference(lambda: store.layout)
extensions = llnl.util.lang.LazyReference(lambda: store.extensions)
