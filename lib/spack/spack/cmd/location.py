# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

import spack.builder
import spack.cmd
import spack.environment as ev
import spack.paths
import spack.repo
import spack.stage
from spack.cmd.common import arguments

description = "print out locations of packages and spack directories"
section = "basic"
level = "long"


def setup_parser(subparser):
    global directories
    directories = subparser.add_mutually_exclusive_group()

    directories.add_argument(
        "-m", "--module-dir", action="store_true", help="spack python module directory"
    )
    directories.add_argument(
        "-r", "--spack-root", action="store_true", help="spack installation root"
    )

    directories.add_argument(
        "-i",
        "--install-dir",
        action="store_true",
        help="install prefix for spec (spec need not be installed)",
    )
    directories.add_argument(
        "-p",
        "--package-dir",
        action="store_true",
        help="directory enclosing a spec's package.py file",
    )
    directories.add_argument(
        "-P", "--packages", action="store_true", help="top-level packages directory for Spack"
    )
    directories.add_argument(
        "-s", "--stage-dir", action="store_true", help="stage directory for a spec"
    )
    directories.add_argument(
        "-S", "--stages", action="store_true", help="top level stage directory"
    )
    directories.add_argument(
        "-c",
        "--source-dir",
        action="store_true",
        help="source directory for a spec (requires it to be staged first)",
    )
    directories.add_argument(
        "-b",
        "--build-dir",
        action="store_true",
        help="build directory for a spec (requires it to be staged first)",
    )
    directories.add_argument(
        "-e",
        "--env",
        action="store",
        dest="location_env",
        nargs="?",
        metavar="name",
        default=False,
        help="location of the named or current environment",
    )

    subparser.add_argument(
        "--first",
        action="store_true",
        default=False,
        dest="find_first",
        help="use the first match if multiple packages match the spec",
    )

    arguments.add_common_arguments(subparser, ["spec"])


def location(parser, args):
    if args.module_dir:
        print(spack.paths.module_path)
        return

    if args.spack_root:
        print(spack.paths.prefix)
        return

    # no -e corresponds to False, -e without arg to None, -e name to the string name.
    if args.location_env is not False:
        if args.location_env is None:
            # Get current environment path
            spack.cmd.require_active_env("location -e")
            path = ev.active_environment().path
        else:
            # Get path of requested environment
            if not ev.exists(args.location_env):
                tty.die("no such environment: '%s'" % args.location_env)
            path = ev.root(args.location_env)
        print(path)
        return

    if args.packages:
        print(spack.repo.PATH.first_repo().root)
        return

    if args.stages:
        print(spack.stage.get_stage_root())
        return

    specs = spack.cmd.parse_specs(args.spec)

    if not specs:
        tty.die("You must supply a spec.")

    if len(specs) != 1:
        tty.die("Too many specs.  Supply only one.")

    # install_dir command matches against installed specs.
    if args.install_dir:
        env = ev.active_environment()
        spec = spack.cmd.disambiguate_spec(specs[0], env, first=args.find_first)
        print(spec.prefix)
        return

    spec = specs[0]

    # Package dir just needs the spec name
    if args.package_dir:
        print(spack.repo.PATH.dirname_for_package_name(spec.name))
        return

    # Either concretize or filter from already concretized environment
    spec = spack.cmd.matching_spec_from_env(spec)
    pkg = spec.package
    builder = spack.builder.create(pkg)

    if args.stage_dir:
        print(pkg.stage.path)
        return

    if args.build_dir:
        # Out of source builds have build_directory defined
        if hasattr(builder, "build_directory"):
            # build_directory can be either absolute or relative to the stage path
            # in either case os.path.join makes it absolute
            print(os.path.normpath(os.path.join(pkg.stage.path, builder.build_directory)))
            return

        # Otherwise assume in-source builds
        print(pkg.stage.source_path)
        return

    # source dir remains, which requires the spec to be staged
    if not pkg.stage.expanded:
        tty.die(
            "Source directory does not exist yet. Run this to create it:",
            "spack stage " + " ".join(args.spec),
        )

    # Default to source dir.
    print(pkg.stage.source_path)
