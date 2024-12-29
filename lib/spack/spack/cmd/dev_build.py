# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

import llnl.util.tty as tty

import spack.build_environment
import spack.cmd
import spack.cmd.common.arguments
import spack.config
import spack.repo
from spack.cmd.common import arguments
from spack.installer import PackageInstaller

description = "developer build: build from code in current working directory"
section = "build"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["jobs", "no_checksum", "spec"])
    subparser.add_argument(
        "-d",
        "--source-path",
        dest="source_path",
        default=None,
        help="path to source directory (defaults to the current directory)",
    )
    subparser.add_argument(
        "-i",
        "--ignore-dependencies",
        action="store_true",
        dest="ignore_deps",
        help="do not try to install dependencies of requested packages",
    )
    subparser.add_argument(
        "--keep-prefix",
        action="store_true",
        help="do not remove the install prefix if installation fails",
    )
    subparser.add_argument(
        "--skip-patch", action="store_true", help="skip patching for the developer build"
    )
    subparser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        dest="quiet",
        help="do not display verbose build output while installing",
    )
    subparser.add_argument(
        "--drop-in",
        type=str,
        dest="shell",
        default=None,
        help="drop into a build environment in a new shell, e.g., bash",
    )
    subparser.add_argument(
        "--test",
        default=None,
        choices=["root", "all"],
        help="run tests on only root packages or all packages",
    )

    stop_group = subparser.add_mutually_exclusive_group()
    stop_group.add_argument(
        "-b",
        "--before",
        type=str,
        dest="before",
        default=None,
        help="phase to stop before when installing (default None)",
    )
    stop_group.add_argument(
        "-u",
        "--until",
        type=str,
        dest="until",
        default=None,
        help="phase to stop after when installing (default None)",
    )

    cd_group = subparser.add_mutually_exclusive_group()
    arguments.add_common_arguments(cd_group, ["clean", "dirty"])

    spack.cmd.common.arguments.add_concretizer_args(subparser)


def dev_build(self, args):
    if not args.spec:
        tty.die("spack dev-build requires a package spec argument.")

    specs = spack.cmd.parse_specs(args.spec)
    if len(specs) > 1:
        tty.die("spack dev-build only takes one spec.")

    spec = specs[0]
    if not spack.repo.PATH.exists(spec.name):
        raise spack.repo.UnknownPackageError(spec.name)

    if not spec.versions.concrete_range_as_version:
        tty.die(
            "spack dev-build spec must have a single, concrete version. "
            "Did you forget a package version number?"
        )

    source_path = args.source_path
    if source_path is None:
        source_path = os.getcwd()
    source_path = os.path.abspath(source_path)

    # Forces the build to run out of the source directory.
    spec.constrain("dev_path=%s" % source_path)
    spec.concretize()

    if spec.installed:
        tty.error("Already installed in %s" % spec.prefix)
        tty.msg("Uninstall or try adding a version suffix for this dev build.")
        sys.exit(1)

    # disable checksumming if requested
    if args.no_checksum:
        spack.config.set("config:checksum", False, scope="command_line")

    tests = False
    if args.test == "all":
        tests = True
    elif args.test == "root":
        tests = [spec.name for spec in specs]

    PackageInstaller(
        [spec.package],
        tests=tests,
        keep_prefix=args.keep_prefix,
        install_deps=not args.ignore_deps,
        verbose=not args.quiet,
        dirty=args.dirty,
        stop_before=args.before,
        skip_patch=args.skip_patch,
        stop_at=args.until,
    ).install()

    # drop into the build environment of the package?
    if args.shell is not None:
        spack.build_environment.setup_package(spec.package, dirty=False)
        os.execvp(args.shell, [args.shell])
