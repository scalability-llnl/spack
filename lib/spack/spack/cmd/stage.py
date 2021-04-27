# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

import spack.environment as ev
import spack.repo
import spack.cmd
import spack.cmd.common.arguments as arguments

description = "expand downloaded archive in preparation for install"
section = "build"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(
        subparser, ['no_checksum', 'deprecated', 'specs'])
    subparser.add_argument(
        '-p', '--path', dest='path',
        help="path to stage package, does not add to spack tree")


def stage(parser, args):
    if not args.specs:
        env = ev.get_env(args, 'stage')
        if env:
            tty.msg("Staging specs from environment %s" % env.name)
            for spec in env.specs_by_hash.values():
                for dep in spec.traverse():
                    dep.package.do_stage()
            return
        else:
            tty.die("`spack stage` requires a spec or an active environment")

    if args.no_checksum:
        spack.config.set('config:checksum', False, scope='command_line')

    if args.deprecated:
        spack.config.set('config:deprecated', True, scope='command_line')

    specs = spack.cmd.parse_specs(args.specs, concretize=False)

    # prevent multiple specs from extracting in the same folder
    if len(specs) > 1 and args.path:
        tty.die("`--path` requires a single spec, but multiple were provided")

    for spec in specs:
        spec = spack.cmd.matching_spec_from_env(spec)
        package = spack.repo.get(spec)
        if args.path:
            package.path = args.path
        package.do_stage()
