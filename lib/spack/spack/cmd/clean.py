# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import os
import shutil

import llnl.util.filesystem
import llnl.util.tty as tty

import spack.caches
import spack.cmd
import spack.config
import spack.stage
import spack.store
import spack.util.path
from spack.cmd.common import arguments
from spack.paths import lib_path, var_path

description = "remove temporary build files and/or downloaded archives"
section = "build"
level = "long"


class AllClean(argparse.Action):
    """Activates flags -s -d -f -m and -p simultaneously"""

    def __call__(self, parser, namespace, values, option_string=None):
        parser.parse_args(["-sdfmp"], namespace=namespace)


def setup_parser(subparser):
    subparser.add_argument(
        "-s", "--stage", action="store_true", help="remove all temporary build stages (default)"
    )
    subparser.add_argument(
        "-d", "--downloads", action="store_true", help="remove cached downloads"
    )
    subparser.add_argument(
        "-f",
        "--failures",
        action="store_true",
        help="force removal of all install failure tracking markers",
    )
    subparser.add_argument(
        "-m",
        "--misc-cache",
        action="store_true",
        help="remove long-lived caches, like the virtual package index",
    )
    subparser.add_argument(
        "-p",
        "--python-cache",
        action="store_true",
        help="remove .pyc, .pyo files and __pycache__ folders",
    )
    subparser.add_argument(
        "-b",
        "--bootstrap",
        action="store_true",
        help="remove software and configuration needed to bootstrap Spack",
    )
    subparser.add_argument(
        "-a",
        "--all",
        action=AllClean,
        help="equivalent to -sdfmp (does not include --bootstrap)",
        nargs=0,
    )
    arguments.add_common_arguments(subparser, ["specs"])


def remove_python_cache():
    for directory in [lib_path, var_path]:
        for root, dirs, files in os.walk(directory):
            for f in files:
                if f.endswith(".pyc") or f.endswith(".pyo"):
                    fname = os.path.join(root, f)
                    tty.debug("Removing {0}".format(fname))
                    os.remove(fname)
            for d in dirs:
                if d == "__pycache__":
                    dname = os.path.join(root, d)
                    tty.debug("Removing {0}".format(dname))
                    shutil.rmtree(dname)


def clean(parser, args):
    # If nothing was set, activate the default
    if not any(
        [
            args.specs,
            args.stage,
            args.downloads,
            args.failures,
            args.misc_cache,
            args.python_cache,
            args.bootstrap,
        ]
    ):
        args.stage = True

    # Then do the cleaning falling through the cases
    if args.specs:
        specs = spack.cmd.parse_specs(args.specs, concretize=False)
        specs = list(spack.cmd.matching_spec_from_env(x) for x in specs)
        for spec in specs:
            msg = "Cleaning build stage [{0}]"
            tty.msg(msg.format(spec.short_spec))
            spec.package.do_clean()

    if args.stage:
        tty.msg("Removing all temporary build stages")
        spack.stage.purge()

    if args.downloads:
        tty.msg("Removing cached downloads")
        spack.caches.FETCH_CACHE.destroy()

    if args.failures:
        tty.msg("Removing install failure marks")
        spack.store.STORE.failure_tracker.clear_all()

    if args.misc_cache:
        tty.msg("Removing cached information on repositories")
        spack.caches.MISC_CACHE.destroy()

    if args.python_cache:
        tty.msg("Removing python cache files")
        remove_python_cache()

    if args.bootstrap:
        bootstrap_prefix = spack.util.path.canonicalize_path(spack.config.get("bootstrap:root"))
        msg = 'Removing bootstrapped software and configuration in "{0}"'
        tty.msg(msg.format(bootstrap_prefix))
        llnl.util.filesystem.remove_directory_contents(bootstrap_prefix)
