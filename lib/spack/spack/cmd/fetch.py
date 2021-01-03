# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.config
import spack.repo

description = "fetch archives for packages"
section = "build"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ['no_checksum'])
    subparser.add_argument(
        '-m', '--missing', action='store_true',
        help="fetch only missing (not yet installed) dependencies")
    subparser.add_argument(
        '-D', '--dependencies', action='store_true',
        help="also fetch all dependencies")
    subparser.add_argument(
        '-f', '--file', action='append', default=[],
        dest='specfiles', metavar='SPEC_YAML_FILE',
        help="fetch from file. Read specs to fetch from .yaml files")
    arguments.add_common_arguments(subparser, ['specs'])


def fetch(parser, args):
    if not args.specs and not args.specfiles:
        tty.die("fetch requires at least one package argument or specfile")

    if args.no_checksum:
        spack.config.set('config:checksum', False, scope='command_line')

    # specs from cli
    specs = spack.cmd.parse_specs(args.specs, concretize=True)

    # specs via specfiles
    for file in args.specfiles:
        with open(file, 'r') as f:
            s = spack.spec.Spec.from_yaml(f)

        if s.concretized().dag_hash() != s.dag_hash():
            msg = 'skipped invalid file "{0}". '
            msg += 'The file does not contain a concrete spec.'
            tty.warn(msg.format(file))
            continue

        specs.append(s.concretized())

    for spec in specs:
        if args.missing or args.dependencies:
            for s in spec.traverse():
                package = spack.repo.get(s)

                # Skip already-installed packages with --missing
                if args.missing and package.installed:
                    continue

                # Do not attempt to fetch externals (they're local)
                if package.spec.external:
                    continue

                package.do_fetch()

        package = spack.repo.get(spec)
        package.do_fetch()
