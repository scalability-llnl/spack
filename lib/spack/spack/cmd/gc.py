# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd.common.arguments
import spack.cmd.uninstall
import spack.environment
import spack.store

description = "remove specs that are now no longer needed"
section = "build"
level = "short"


def setup_parser(subparser):
    spack.cmd.common.arguments.add_common_arguments(subparser, ['yes_to_all'])


def gc(parser, args):
    specs = spack.store.store.db.unused_specs

    # Restrict garbage collection to the active environment
    # speculating over roots that are yet to be installed
    env = spack.environment.get_env(args=None, cmd_name='gc')
    if env:
        msg = 'Restricting the garbage collection to the "{0}" environment'
        tty.msg(msg.format(env.name))
        env.concretize()
        roots = [s for s in env.roots()]
        all_hashes = set([s.dag_hash() for r in roots for s in r.traverse()])
        lr_hashes = set([s.dag_hash() for r in roots
                         for s in r.traverse(deptype=('link', 'run'))])
        maybe_to_be_removed = all_hashes - lr_hashes
        specs = [s for s in specs if s.dag_hash() in maybe_to_be_removed]

    if not specs:
        msg = "There are no unused specs. Spack's store is clean."
        tty.msg(msg)
        return

    if not args.yes_to_all:
        spack.cmd.uninstall.confirm_removal(specs)

    spack.cmd.uninstall.do_uninstall(None, specs, force=False)
