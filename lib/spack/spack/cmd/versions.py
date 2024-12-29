# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack.repo
import spack.spec
from spack.cmd.common import arguments
from spack.version import infinity_versions, ver

description = "list available versions of a package"
section = "packaging"
level = "long"


def setup_parser(subparser):
    output = subparser.add_mutually_exclusive_group()
    output.add_argument(
        "-s", "--safe", action="store_true", help="only list safe versions of the package"
    )
    output.add_argument(
        "-r", "--remote", action="store_true", help="only list remote versions of the package"
    )
    output.add_argument(
        "-n",
        "--new",
        action="store_true",
        help="only list remote versions newer than the latest checksummed version",
    )
    arguments.add_common_arguments(subparser, ["package", "jobs"])


def versions(parser, args):
    spec = spack.spec.Spec(args.package)
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    pkg = pkg_cls(spec)

    safe_versions = pkg.versions

    if not (args.remote or args.new):
        if sys.stdout.isatty():
            tty.msg("Safe versions (already checksummed):")

        if not safe_versions:
            if sys.stdout.isatty():
                tty.warn(f"Found no versions for {pkg.name}")
                tty.debug("Manually add versions to the package.")
        else:
            colify(sorted(safe_versions, reverse=True), indent=2)

        if args.safe:
            return

    fetched_versions = pkg.fetch_remote_versions(args.jobs)

    if args.new:
        if sys.stdout.isatty():
            tty.msg("New remote versions (not yet checksummed):")
        numeric_safe_versions = list(
            filter(lambda v: str(v) not in infinity_versions, safe_versions)
        )
        highest_safe_version = max(numeric_safe_versions)
        remote_versions = set([ver(v) for v in set(fetched_versions) if v > highest_safe_version])
    else:
        if sys.stdout.isatty():
            tty.msg("Remote versions (not yet checksummed):")
        remote_versions = set(fetched_versions).difference(safe_versions)

    if not remote_versions:
        if sys.stdout.isatty():
            if not fetched_versions:
                tty.warn(f"Found no versions for {pkg.name}")
                tty.debug(
                    "Check the list_url and list_depth attributes of "
                    "the package to help Spack find versions."
                )
            else:
                tty.warn(f"Found no unchecksummed versions for {pkg.name}")
    else:
        colify(sorted(remote_versions, reverse=True), indent=2)
