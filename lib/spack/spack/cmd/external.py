# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from __future__ import print_function

import argparse
import os
import sys

import llnl.util.tty as tty
import llnl.util.tty.colify as colify

import spack
import spack.cmd
import spack.cmd.common.arguments
import spack.cray_manifest as cray_manifest
import spack.detection
import spack.error
import spack.util.environment

description = "manage external packages in Spack configuration"
section = "config"
level = "short"


def setup_parser(subparser):
    sp = subparser.add_subparsers(
        metavar='SUBCOMMAND', dest='external_command')

    scopes = spack.config.scopes()
    scopes_metavar = spack.config.scopes_metavar

    find_parser = sp.add_parser(
        'find', help='add external packages to packages.yaml'
    )
    find_parser.add_argument(
        '--not-buildable', action='store_true', default=False,
        help="packages with detected externals won't be built with Spack")
    find_parser.add_argument(
        '--scope', choices=scopes, metavar=scopes_metavar,
        default=spack.config.default_modify_scope('packages'),
        help="configuration scope to modify")
    spack.cmd.common.arguments.add_common_arguments(find_parser, ['tags'])
    find_parser.add_argument('packages', nargs=argparse.REMAINDER)

    sp.add_parser(
        'list', help='list detectable packages, by repository and name'
    )

    read_cray_manifest = sp.add_parser(
        'read-cray-manifest', help="read a spack.json file"
    )
    read_cray_manifest.add_argument(
        '--file', default=None,
        help="specify a location other than the default")


def external_find(args):
    # Construct the list of possible packages to be detected
    packages_to_check = []

    # Add the packages that have been required explicitly
    if args.packages:
        packages_to_check = list(spack.repo.get(pkg) for pkg in args.packages)
        if args.tags:
            allowed = set(spack.repo.path.packages_with_tags(*args.tags))
            packages_to_check = [x for x in packages_to_check if x in allowed]

    if args.tags and not packages_to_check:
        # If we arrived here we didn't have any explicit package passed
        # as argument, which means to search all packages.
        # Since tags are cached it's much faster to construct what we need
        # to search directly, rather than filtering after the fact
        packages_to_check = [
            spack.repo.get(pkg) for pkg in
            spack.repo.path.packages_with_tags(*args.tags)
        ]

    # If the list of packages is empty, search for every possible package
    if not args.tags and not packages_to_check:
        packages_to_check = spack.repo.path.all_packages()

    detected_packages = spack.detection.by_executable(packages_to_check)
    new_entries = spack.detection.update_configuration(
        detected_packages, scope=args.scope, buildable=not args.not_buildable
    )
    if new_entries:
        path = spack.config.config.get_config_filename(args.scope, 'packages')
        msg = ('The following specs have been detected on this system '
               'and added to {0}')
        tty.msg(msg.format(path))
        spack.cmd.display_specs(new_entries)
    else:
        tty.msg('No new external packages detected')


def external_read_cray_manifest(args):
    if args.file:
        path = args.file
    elif os.path.exists(cray_manifest.default_path):
        path = cray_manifest.default_path
    else:
        raise ValueError(
            "No --file specified, and no manifest found at {0}"
            .format(cray_manifest.default_path))

    cray_manifest.read(path, True)


def external_list(args):
    # Trigger a read of all packages, might take a long time.
    list(spack.repo.path.all_packages())
    # Print all the detectable packages
    tty.msg("Detectable packages per repository")
    for namespace, pkgs in sorted(spack.package.detectable_packages.items()):
        print("Repository:", namespace)
        colify.colify(pkgs, indent=4, output=sys.stdout)


def external(parser, args):
    action = {'find': external_find, 'list': external_list,
              'read-cray-manifest': external_read_cray_manifest}
    action[args.external_command](args)
