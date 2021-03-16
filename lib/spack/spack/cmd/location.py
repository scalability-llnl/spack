# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import os
import llnl.util.tty as tty

import spack.environment as ev
import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment
import spack.paths
import spack.repo
import spack.stage

description = "print out locations of packages and spack directories"
section = "basic"
level = "long"


def setup_parser(subparser):
    global directories
    directories = subparser.add_mutually_exclusive_group()

    directories.add_argument(
        '-m', '--module-dir', action='store_true',
        help="spack python module directory")
    directories.add_argument(
        '-r', '--spack-root', action='store_true',
        help="spack installation root")

    directories.add_argument(
        '-i', '--install-dir', action='store_true',
        help="install prefix for spec (spec need not be installed)")
    directories.add_argument(
        '-p', '--package-dir', action='store_true',
        help="directory enclosing a spec's package.py file")
    directories.add_argument(
        '-P', '--packages', action='store_true',
        help="top-level packages directory for Spack")
    directories.add_argument(
        '-s', '--stage-dir', action='store_true',
        help="stage directory for a spec")
    directories.add_argument(
        '-S', '--stages', action='store_true',
        help="top level stage directory")
    directories.add_argument(
        '-c', '--source-dir', action='store_true',
        help="source directory for a spec "
             "(requires it to be staged first)")
    directories.add_argument(
        '-b', '--build-dir', action='store_true',
        help="build directory for a spec "
             "(requires it to be staged first)")
    directories.add_argument(
        '-e', '--env', action='store',
        help="location of an environment managed by spack")

    arguments.add_common_arguments(subparser, ['spec'])


def location(parser, args):
    if args.module_dir:
        return print(spack.paths.module_path)

    if args.spack_root:
        return print(spack.paths.prefix)

    if args.env:
        path = spack.environment.root(args.env)
        if not os.path.isdir(path):
            tty.die("no such environment: '%s'" % args.env)
        return print(path)

    if args.packages:
        return print(spack.repo.path.first_repo().root)

    if args.stages:
        return print(spack.stage.get_stage_root())

    specs = spack.cmd.parse_specs(args.spec)

    if not specs:
        tty.die("You must supply a spec.")

    if len(specs) != 1:
        tty.die("Too many specs.  Supply only one.")

    # install_dir command matches against installed specs.
    if args.install_dir:
        env = ev.get_env(args, 'location')
        spec = spack.cmd.disambiguate_spec(specs[0], env)
        return print(spec.prefix)

    spec = specs[0]

    # Package dir just needs the spec name
    if args.package_dir:
        return print(spack.repo.path.dirname_for_package_name(spec.name))

    # Either concretize or filter from already concretized environment
    spec = spack.cmd.matching_spec_from_env(spec)
    pkg = spec.package

    if args.stage_dir:
        return print(pkg.stage.path)

    if args.build_dir:
        # Out of source builds have build_directory defined
        if hasattr(pkg, 'build_directory'):
            # build_directory can be either absolute or relative to the stage path
            # in either case os.path.join makes it absolute
            return print(os.path.normpath(os.path.join(
                pkg.stage.path,
                pkg.build_directory
            )))

        # Otherwise assume in-source builds
        return print(pkg.stage.source_path)

    # source and build dir remain, they require the spec to be staged
    if not pkg.stage.expanded:
        tty.die("Source directory does not exist yet. "
                "Run this to create it:",
                "spack stage " + " ".join(args.spec))

    if args.source_dir:
        return print(pkg.stage.source_path)
