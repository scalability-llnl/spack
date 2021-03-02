# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.cmd
import spack.store
import llnl.util.tty as tty


description = "creates pointer to install tree" \
              " for use as an upstream"
section = "upstream"
level = "long"


def setup_parser(subparser):
    subparser.add_argument(
        metavar='tree_name', dest='tree_name',
        help='name of environment to activate')


def init_upstream(parser, args):
    shared_install_trees = spack.config.get('config:shared_install_trees')
    if shared_install_trees:
        root = spack.store.store.root
        init_upstream_path = shared_install_trees[args.tree_name]['root']
        spack.store.initialize_upstream_pointer_if_unset(root,
                                                         init_upstream_path)
    else:
        tty.die("Specified upstream must be defined"
                " as shared install tree.")
