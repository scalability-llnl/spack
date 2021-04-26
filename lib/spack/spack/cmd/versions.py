# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import sys

from llnl.util.tty.colify import colify
import llnl.util.tty as tty

import spack.cmd.common.arguments as arguments
import spack.repo
from spack.version import ver, infinity_versions

description = "list available versions of a package"
section = "packaging"
level = "long"


def setup_parser(subparser):
    output = subparser.add_mutually_exclusive_group()
    output.add_argument('-s', '--safe', action='store_true',
                        help='only list safe versions of the package')
    output.add_argument('--safe-only', action='store_true',
                        help='[deprecated] only list safe versions '
                        'of the package')
    output.add_argument('-r', '--remote', action='store_true',
                        help='only list remote versions of the package')
    output.add_argument('-n', '--new', action='store_true',
                        help='only list remote versions newer than '
                        'the latest checksummed version')
    subparser.add_argument(
        '-c', '--concurrency', default=32, type=int,
        help='number of concurrent requests'
    )
    arguments.add_common_arguments(subparser, ['package'])


def versions(parser, args):
    pkg = spack.repo.get(args.package)

    safe_versions = pkg.versions

    if args.safe_only:
        tty.warn('"--safe-only" is deprecated. Use "--safe" instead.')
        args.safe = args.safe_only

    if not (args.remote or args.new):
        if sys.stdout.isatty():
            tty.msg('Safe versions (already checksummed):')

        if not safe_versions:
            if sys.stdout.isatty():
                tty.warn('Found no versions for {0}'.format(pkg.name))
                tty.debug('Manually add versions to the package.')
        else:
            colify(sorted(safe_versions, reverse=True), indent=2)

        if args.safe:
            return

    fetched_versions = pkg.fetch_remote_versions(args.concurrency)

    if args.new:
        if sys.stdout.isatty():
            tty.msg('New remote versions (not yet checksummed):')
        numeric_safe_versions = list(filter(
            lambda v: str(v) not in infinity_versions,
            safe_versions))
        highest_safe_version = max(numeric_safe_versions)
        remote_versions  = set([ver(v) for v in set(fetched_versions)
                                if v > highest_safe_version])
    else:
        if sys.stdout.isatty():
            tty.msg('Remote versions (not yet checksummed):')
        remote_versions = set(fetched_versions).difference(safe_versions)

    if not remote_versions:
        if sys.stdout.isatty():
            if not fetched_versions:
                tty.warn('Found no versions for {0}'.format(pkg.name))
                tty.debug('Check the list_url and list_depth attributes of '
                          'the package to help Spack find versions.')
            else:
                tty.warn('Found no unchecksummed versions for {0}'.format(
                    pkg.name))
    else:
        colify(sorted(remote_versions, reverse=True), indent=2)
