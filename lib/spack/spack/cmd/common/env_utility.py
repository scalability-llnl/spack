# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse
import os

import llnl.util.tty as tty

import spack.cmd
import spack.deptypes as dt
import spack.error
import spack.spec
import spack.store
from spack import build_environment, traverse
from spack.cmd.common import arguments
from spack.context import Context
from spack.util.environment import dump_environment, pickle_environment


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["clean", "dirty"])
    arguments.add_concretizer_args(subparser)

    subparser.add_argument("--dump", metavar="FILE", help="dump a source-able environment to FILE")
    subparser.add_argument(
        "--pickle", metavar="FILE", help="dump a pickled source-able environment to FILE"
    )
    subparser.add_argument(
        "spec",
        nargs=argparse.REMAINDER,
        metavar="spec [--] [cmd]...",
        help="specs of package environment to emulate",
    )
    subparser.epilog = (
        "If a command is not specified, the environment will be printed "
        "to standard output (cf /usr/bin/env) unless --dump and/or --pickle "
        "are specified.\n\nIf a command is specified and spec is "
        "multi-word, then the -- separator is obligatory."
    )


class AreDepsInstalledVisitor:
    def __init__(self, context: Context = Context.BUILD):
        if context == Context.BUILD:
            # TODO: run deps shouldn't be required for build env.
            self.direct_deps = dt.BUILD | dt.LINK | dt.RUN
        elif context == Context.TEST:
            self.direct_deps = dt.BUILD | dt.TEST | dt.LINK | dt.RUN
        else:
            raise ValueError("context can only be Context.BUILD or Context.TEST")

        self.has_uninstalled_deps = False

    def accept(self, item):
        # The root may be installed or uninstalled.
        if item.depth == 0:
            return True

        # Early exit after we've seen an uninstalled dep.
        if self.has_uninstalled_deps:
            return False

        spec = item.edge.spec
        if not spec.external and not spec.installed:
            self.has_uninstalled_deps = True
            return False

        return True

    def neighbors(self, item):
        # Direct deps: follow build & test edges.
        # Transitive deps: follow link / run.
        depflag = self.direct_deps if item.depth == 0 else dt.LINK | dt.RUN
        return item.edge.spec.edges_to_dependencies(depflag=depflag)


def emulate_env_utility(cmd_name, context: Context, args):
    if not args.spec:
        tty.die("spack %s requires a spec." % cmd_name)

    # Specs may have spaces in them, so if they do, require that the
    # caller put a '--' between the spec and the command to be
    # executed.  If there is no '--', assume that the spec is the
    # first argument.
    sep = "--"
    if sep in args.spec:
        s = args.spec.index(sep)
        spec = args.spec[:s]
        cmd = args.spec[s + 1 :]
    else:
        spec = args.spec[0]
        cmd = args.spec[1:]

    if not spec:
        tty.die("spack %s requires a spec." % cmd_name)

    specs = spack.cmd.parse_specs(spec, concretize=False)
    if len(specs) > 1:
        tty.die("spack %s only takes one spec." % cmd_name)
    spec = specs[0]

    spec = spack.cmd.matching_spec_from_env(spec)

    # Require that dependencies are installed.
    visitor = AreDepsInstalledVisitor(context=context)

    # Mass install check needs read transaction.
    with spack.store.STORE.db.read_transaction():
        traverse.traverse_breadth_first_with_visitor([spec], traverse.CoverNodesVisitor(visitor))

    if visitor.has_uninstalled_deps:
        raise spack.error.SpackError(
            f"Not all dependencies of {spec.name} are installed. "
            f"Cannot setup {context} environment:",
            spec.tree(
                status_fn=spack.spec.Spec.install_status,
                hashlen=7,
                hashes=True,
                # This shows more than necessary, but we cannot dynamically change deptypes
                # in Spec.tree(...).
                deptypes="all" if context == Context.BUILD else ("build", "test", "link", "run"),
            ),
        )

    build_environment.setup_package(spec.package, args.dirty, context)

    if args.dump:
        # Dump a source-able environment to a text file.
        tty.msg("Dumping a source-able environment to {0}".format(args.dump))
        dump_environment(args.dump)

    if args.pickle:
        # Dump a source-able environment to a pickle file.
        tty.msg("Pickling a source-able environment to {0}".format(args.pickle))
        pickle_environment(args.pickle)

    if cmd:
        # Execute the command with the new environment
        os.execvp(cmd[0], cmd)

    elif not bool(args.pickle or args.dump):
        # If no command or dump/pickle option then act like the "env" command
        # and print out env vars.
        for key, val in os.environ.items():
            print("%s=%s" % (key, val))
