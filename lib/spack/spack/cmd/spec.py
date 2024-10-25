# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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

    tree_kwargs = {
        "cover": args.cover,
        "format": fmt,
        "hashlen": None if args.very_long else 7,
        "show_types": args.types,
        "status_fn": install_status_fn if args.install_status else None,
    }

    # use a read transaction if we are getting install status for every
    # spec in the DAG.  This avoids repeatedly querying the DB.
    tree_context = lang.nullcontext
    if args.install_status:
        tree_context = spack.store.STORE.db.read_transaction

    # Use command line specified specs, otherwise try to use environment specs.
    if args.specs:
        input_specs = spack.cmd.parse_specs(args.specs)
        concretized_specs = spack.cmd.parse_specs(args.specs, concretize=True)
        specs = list(zip(input_specs, concretized_specs))
    else:
        env = ev.active_environment()
        if env:
            env.concretize()
            specs = env.concretized_specs()

            # environments are printed together in a combined tree() invocation,
            # except when using --yaml or --json, which we print spec by spec below.
            if not args.format:
                tree_kwargs["key"] = spack.traverse.by_dag_hash
                tree_kwargs["hashes"] = args.long or args.very_long
                print(spack.spec.tree([concrete for _, concrete in specs], **tree_kwargs))
                return
        else:
            tty.die("spack spec requires at least one spec or an active environment")

    for input, output in specs:
        # With --yaml or --json, just print the raw specs to output
        if args.format:
            if args.format == "yaml":
                # use write because to_yaml already has a newline.
                sys.stdout.write(output.to_yaml(hash=ht.dag_hash))
            elif args.format == "json":
                print(output.to_json(hash=ht.dag_hash))
            else:
                print(output.format(args.format))
            continue

        with tree_context():
            # Only show the headers for input specs that are not concrete to avoid
            # repeated output. This happens because parse_specs outputs concrete
            # specs for `/hash` inputs.
            if not input.concrete:
                tree_kwargs["hashes"] = False  # Always False for input spec
                print("Input spec")
                print("--------------------------------")
                print(input.tree(**tree_kwargs))
                print("Concretized")
                print("--------------------------------")

            tree_kwargs["hashes"] = args.long or args.very_long
            print(output.tree(**tree_kwargs))
