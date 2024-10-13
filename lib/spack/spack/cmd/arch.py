# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import collections

import archspec.cpu

import llnl.util.tty.colify as colify
import llnl.util.tty.color as color

import spack.platforms
import spack.spec

description = "print architecture information about this machine"
section = "system"
level = "short"


def setup_parser(subparser):
    subparser.add_argument(
        "-g", "--generic-target", action="store_true", help="show the best generic target"
    )
    subparser.add_argument(
        "--known-targets", action="store_true", help="show a list of all known targets and exit"
    )
    parts = subparser.add_mutually_exclusive_group()
    parts2 = subparser.add_mutually_exclusive_group()
    parts.add_argument(
        "-p", "--platform", action="store_true", default=False, help="print only the platform"
    )
    parts.add_argument(
        "-o",
        "--operating-system",
        action="store_true",
        default=False,
        help="print only the operating system",
    )
    parts.add_argument(
        "-t", "--target", action="store_true", default=False, help="print only the target"
    )
    parts2.add_argument(
        "-f", "--frontend", action="store_true", default=False, help="print frontend"
    )
    parts2.add_argument(
        "-b", "--backend", action="store_true", default=False, help="print backend"
    )


def display_targets(targets):
    """Prints a human readable list of the targets passed as argument."""
    by_vendor = collections.defaultdict(list)
    for _, target in targets.items():
        by_vendor[target.vendor].append(target)

    def display_target_group(header, target_group):
        print(header)
        colify.colify(target_group, indent=4)
        print("")

    generic_architectures = by_vendor.pop("generic", None)
    if generic_architectures:
        header = color.colorize(r"@*B{Generic architectures (families)}")
        group = sorted(generic_architectures, key=lambda x: str(x))
        display_target_group(header, group)

    for vendor, vendor_targets in by_vendor.items():
        by_family = collections.defaultdict(list)
        for t in vendor_targets:
            by_family[str(t.family)].append(t)

        for family, group in by_family.items():
            vendor = color.colorize(r"@*B{" + vendor + r"}")
            family = color.colorize(r"@*B{" + family + r"}")
            header = " - ".join([vendor, family])
            group = sorted(group, key=lambda x: len(x.ancestors))
            display_target_group(header, group)


def arch(parser, args):
    if args.generic_target:
        print(archspec.cpu.host().generic)
        return

    if args.known_targets:
        display_targets(archspec.cpu.TARGETS)
        return

    os_args, target_args = "default_os", "default_target"
    if args.frontend:
        os_args, target_args = "frontend", "frontend"
    elif args.backend:
        os_args, target_args = "backend", "backend"

    host_platform = spack.platforms.host()
    host_os = host_platform.operating_system(os_args)
    host_target = host_platform.target(target_args)
    architecture = spack.spec.ArchSpec((str(host_platform), str(host_os), str(host_target)))

    if args.platform:
        print(architecture.platform)
    elif args.operating_system:
        print(architecture.os)
    elif args.target:
        print(architecture.target)
    else:
        print(architecture)
