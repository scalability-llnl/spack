# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil

import llnl.util.tty as tty

import spack.caches
import spack.config
import spack.cmd.test
import spack.cmd.common.arguments as arguments
import spack.main
import spack.repo
import spack.stage
from spack.paths import lib_path, var_path


description = "remove temporary build files and/or downloaded archives"
section = "build"
level = "long"


class AllClean(argparse.Action):
    """Activates flags -s -d -f -m and -p simultaneously"""
    def __call__(self, parser, namespace, values, option_string=None):
        parser.parse_args(['-sdfmpb'], namespace=namespace)


def setup_parser(subparser):
    subparser.add_argument(
        '-s', '--stage', action='store_true',
        help="remove all temporary build stages (default)")
    subparser.add_argument(
        '-d', '--downloads', action='store_true',
        help="remove cached downloads")
    subparser.add_argument(
        '-f', '--failures', action='store_true',
        help="force removal of all install failure tracking markers")
    subparser.add_argument(
        '-m', '--misc-cache', action='store_true',
        help="remove long-lived caches, like the virtual package index")
    subparser.add_argument(
        '-p', '--python-cache', action='store_true',
        help="remove .pyc, .pyo files and __pycache__ folders")
    subparser.add_argument(
        '-b', '--bootstrap', action='store_true',
        help="remove software needed to bootstrap Spack")
    subparser.add_argument(
        '-a', '--all', action=AllClean, help="equivalent to -sdfmpb", nargs=0
    )
    arguments.add_common_arguments(subparser, ['specs'])


def clean(parser, args):
    # If nothing was set, activate the default
    if not any([args.specs, args.stage, args.downloads, args.failures,
                args.misc_cache, args.python_cache, args.bootstrap]):
        args.stage = True

    # Then do the cleaning falling through the cases
    if args.specs:
        specs = spack.cmd.parse_specs(args.specs, concretize=True)
        for spec in specs:
            msg = 'Cleaning build stage [{0}]'
            tty.msg(msg.format(spec.short_spec))
            package = spack.repo.get(spec)
            package.do_clean()

    if args.stage:
        tty.msg('Removing all temporary build stages')
        spack.stage.purge()

    if args.downloads:
        tty.msg('Removing cached downloads')
        spack.caches.fetch_cache.destroy()

    if args.failures:
        tty.msg('Removing install failure marks')
        spack.installer.clear_failures()

    if args.misc_cache:
        tty.msg('Removing cached information on repositories')
        spack.caches.misc_cache.destroy()

    if args.python_cache:
        tty.msg('Removing python cache files')
        for directory in [lib_path, var_path]:
            for root, dirs, files in os.walk(directory):
                for f in files:
                    if f.endswith('.pyc') or f.endswith('.pyo'):
                        fname = os.path.join(root, f)
                        tty.debug('Removing {0}'.format(fname))
                        os.remove(fname)
                for d in dirs:
                    if d == '__pycache__':
                        dname = os.path.join(root, d)
                        tty.debug('Removing {0}'.format(dname))
                        shutil.rmtree(dname)

    if args.bootstrap:
        msg = 'Removing software in "{0}"'
        tty.msg(msg.format(spack.paths.user_bootstrap_store))
        with spack.store.use_store(spack.paths.user_bootstrap_store):
            uninstall = spack.main.SpackCommand('uninstall')
            uninstall('-a', '-y')
