# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

import spack
import spack.platforms
import spack.spec

description = "debugging commands for troubleshooting Spack"
section = "developer"
level = "long"


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="debug_command")
    sp.add_parser("report", help="print information useful for bug reports")


def report(args):
    host_platform = spack.platforms.host()
    host_os = host_platform.default_operating_system()
    host_target = host_platform.default_target()
    architecture = spack.spec.ArchSpec((str(host_platform), str(host_os), str(host_target)))
    print("* **Spack:**", spack.get_version())
    print("* **Python:**", platform.python_version())
    print("* **Platform:**", architecture)


def debug(parser, args):
    if args.debug_command == "report":
        report(args)
