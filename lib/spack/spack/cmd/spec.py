# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import contextlib
import sys

import llnl.util.tty as tty

import spack
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.spec
import spack.store
import spack.hash_types as ht

description = "show what would be installed, given a spec"
section = "build"
level = "short"


def setup_parser(subparser):
    subparser.epilog = """\
for further documentation regarding the spec syntax, see:
    spack help --spec
"""
    arguments.add_common_arguments(
        subparser, ['long', 'very_long', 'install_status'])
    subparser.add_argument(
        '-y', '--yaml', action='store_const', dest='format', default=None,
        const='yaml', help='print concrete spec as YAML')
    subparser.add_argument(
        '-j', '--json', action='store_const', dest='format', default=None,
        const='json', help='print concrete spec as JSON')
    subparser.add_argument(
        '-c', '--cover', action='store',
        default='nodes', choices=['nodes', 'edges', 'paths'],
        help='how extensively to traverse the DAG (default: nodes)')
    subparser.add_argument(
        '-N', '--namespaces', action='store_true', default=False,
        help='show fully qualified package names')
    subparser.add_argument(
        '--hash-type', default="build_hash",
        choices=['build_hash', 'full_hash', 'dag_hash'],
        help='generate spec with a particular hash type.')
    subparser.add_argument(
        '-t', '--types', action='store_true', default=False,
        help='show dependency types')
    arguments.add_common_arguments(subparser, ['specs'])


@contextlib.contextmanager
def nullcontext():
    """Empty context manager.
    TODO: replace with contextlib.nullcontext() if we ever require python 3.7.
    """
    yield


def spec(parser, args):
    name_fmt = '{namespace}.{name}' if args.namespaces else '{name}'
    fmt = '{@version}{%compiler}{compiler_flags}{variants}{arch=architecture}'
    install_status_fn = spack.spec.Spec.install_status
    kwargs = {
        'cover': args.cover,
        'format': name_fmt + fmt,
        'hashlen': None if args.very_long else 7,
        'show_types': args.types,
        'status_fn': install_status_fn if args.install_status else None
    }

    # use a read transaction if we are getting install status for every
    # spec in the DAG.  This avoids repeatedly querying the DB.
    tree_context = nullcontext
    if args.install_status:
        tree_context = spack.store.db.read_transaction

    if not args.specs:
        tty.die("spack spec requires at least one spec")

    for spec in spack.cmd.parse_specs(args.specs):
        # With -y, just print YAML to output.
        if args.format:
            if spec.name in spack.repo.path or spec.virtual:
                spec.concretize()

            # The user can specify the hash type to use
            hash_type = getattr(ht, args.hash_type)

            if args.format == 'yaml':
                # use write because to_yaml already has a newline.
                sys.stdout.write(spec.to_yaml(hash=hash_type))
            else:
                print(spec.to_json(hash=hash_type))
            continue

        with tree_context():
            kwargs['hashes'] = False  # Always False for input spec
            print("Input spec")
            print("--------------------------------")
            print(spec.tree(**kwargs))

            kwargs['hashes'] = args.long or args.very_long
            print("Concretized")
            print("--------------------------------")
            spec.concretize()
            print(spec.tree(**kwargs))
