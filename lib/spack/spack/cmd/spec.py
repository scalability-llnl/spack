# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import llnl.util.lang as lang
import llnl.util.tty as tty

import spack
import spack.cmd
import spack.environment as ev
import spack.hash_types as ht
import spack.spec
import spack.store
import spack.traverse
from spack.cmd.common import arguments

description = "show what would be installed, given a spec"
section = "build"
level = "short"


def setup_parser(subparser):
    subparser.epilog = """\
when an environment is active and no specs are provided, the environment root \
specs are used instead

for further documentation regarding the spec syntax, see:
    spack help --spec
"""
    arguments.add_common_arguments(subparser, ["long", "very_long", "namespaces"])

    install_status_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(install_status_group, ["install_status", "no_install_status"])

    format_group = subparser.add_mutually_exclusive_group()
    format_group.add_argument(
        "-y",
        "--yaml",
        action="store_const",
        dest="format",
        default=None,
        const="yaml",
        help="print concrete spec as YAML",
    )
    format_group.add_argument(
        "-j",
        "--json",
        action="store_const",
        dest="format",
        default=None,
        const="json",
        help="print concrete spec as JSON",
    )
    format_group.add_argument(
        "--format",
        action="store",
        default=None,
        help="print concrete spec with the specified format string",
    )
    subparser.add_argument(
        "-c",
        "--cover",
        action="store",
        default="nodes",
        choices=["nodes", "edges", "paths"],
        help="how extensively to traverse the DAG (default: nodes)",
    )
    subparser.add_argument(
        "-t", "--types", action="store_true", default=False, help="show dependency types"
    )
    arguments.add_common_arguments(subparser, ["specs"])
    arguments.add_concretizer_args(subparser)


def spec(parser, args):
    install_status_fn = spack.spec.Spec.install_status

    fmt = spack.spec.DISPLAY_FORMAT
    if args.namespaces:
        fmt = "{namespace}." + fmt

    # use a read transaction if we are getting install status for every
    # spec in the DAG.  This avoids repeatedly querying the DB.
    tree_context = lang.nullcontext
    if args.install_status:
        tree_context = spack.store.STORE.db.read_transaction

    env = ev.active_environment()

    if args.specs:
        concrete_specs = spack.cmd.parse_specs(args.specs, concretize=True)
    elif env:
        env.concretize()
        concrete_specs = env.concrete_roots()
    else:
        tty.die("spack spec requires at least one spec or an active environment")

    # With --yaml, --json, or --format, just print the raw specs to output
    if args.format:
        for spec in concrete_specs:
            if args.format == "yaml":
                # use write because to_yaml already has a newline.
                sys.stdout.write(spec.to_yaml(hash=ht.dag_hash))
            elif args.format == "json":
                print(spec.to_json(hash=ht.dag_hash))
            else:
                print(spec.format(args.format))
        return

    with tree_context():
        print(
            spack.spec.tree(
                concrete_specs,
                cover=args.cover,
                format=fmt,
                hashlen=None if args.very_long else 7,
                show_types=args.types,
                status_fn=install_status_fn if args.install_status else None,
                hashes=args.long or args.very_long,
                key=spack.traverse.by_dag_hash,
            )
        )
