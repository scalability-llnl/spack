# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse
import os

import llnl.util.tty as tty

import spack.cmd
import spack.deptypes as dt
import spack.error
import spack.prompt
import spack.spec
import spack.store
from spack import build_environment, traverse
from spack.cmd.common import arguments
from spack.cmd.location import location_emulator
from spack.context import Context
from spack.util.environment import dump_environment, pickle_environment
from spack.util.shell_detection import active_shell_type


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["clean", "dirty"])
    arguments.add_concretizer_args(subparser)

    subparser.add_argument("--dump", metavar="FILE", help="dump a source-able environment to FILE")
    subparser.add_argument(
        "--pickle", metavar="FILE", help="dump a pickled source-able environment to FILE"
    )
    subparser.add_argument(
        "-d", "--dive", action="store_true", help="dive into the build-env in a subshell"
    )
    subparser.add_argument(
        "-c",
        "--cd",
        help="location to dive to or run command from (takes arguments from 'spack cd')",
    )
    subparser.add_argument(
        "--status", action="store_true", help="check shell for an active build environment"
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


def run_command_in_subshell(
    spec, context, cmd, prompt=False, dirty=False, cd_arg=None, shell=active_shell_type()
):
    mods = build_environment.setup_package(spec.package, dirty, context)

    if prompt:
        mods.extend(spack.prompt.prompt_modifications(f"{spec.name}-{str(context)}-env", shell))
    mods.apply_modifications()

    if cd_arg:
        prefix = "-" if len(cd_arg) == 1 else "--"
        loc_args = [f"{prefix}{cd_arg}"]

        # don't add spec for cd if using env since spec hash is not the env
        if not (cd_arg == "e" or cd_arg == "env"):
            loc_args.append(f"/{spec.dag_hash()}")

        location = location_emulator(*loc_args)
        os.chdir(location)

    os.execvp(cmd[0], cmd)


def emulate_env_utility(cmd_name, context: Context, args):
    if args.status:
        context_var = os.environ.get(f"SPACK_{str(context).upper()}_ENV", None)
        if context_var:
            tty.msg(f"In {str(context)} env {context_var}")
        else:
            tty.msg(f"{str(context)} environment not detected")
        exit(0)

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

    if args.dive:
        if cmd:
            tty.die("--dive and additional commands can't be run together")
        else:
            cmd = [active_shell_type()]

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
    # FIXME: this command is slow
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

    if cmd:
        run_command_in_subshell(spec, context, cmd, prompt=args.dive, cd_arg=args.cd)
    else:
        # setup build env if no command to run
        build_environment.setup_package(spec.package, args.dirty, context)

    if args.dump:
        # Dump a source-able environment to a text file.
        tty.msg("Dumping a source-able environment to {0}".format(args.dump))
        dump_environment(args.dump)

    if args.pickle:
        # Dump a source-able environment to a pickle file.
        tty.msg("Pickling a source-able environment to {0}".format(args.pickle))
        pickle_environment(args.pickle)

    elif not bool(args.pickle or args.dump):
        # If no command or dump/pickle option then act like the "env" command
        # and print out env vars.
        for key, val in os.environ.items():
            print("%s=%s" % (key, val))
