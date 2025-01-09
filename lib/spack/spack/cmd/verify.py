# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import argparse

import llnl.util.tty as tty

import spack.cmd
import spack.environment as ev
import spack.store
import spack.verify

description = "check that all spack packages are on disk as installed"
section = "admin"
level = "long"


def setup_parser(subparser):
    setup_parser.parser = subparser

    subparser.add_argument(
        "-l", "--local", action="store_true", help="verify only locally installed packages"
    )
    subparser.add_argument(
        "-j", "--json", action="store_true", help="ouptut json-formatted errors"
    )
    subparser.add_argument("-a", "--all", action="store_true", help="verify all packages")
    subparser.add_argument(
        "specs_or_files", nargs=argparse.REMAINDER, help="specs or files to verify"
    )

    type = subparser.add_mutually_exclusive_group()
    type.add_argument(
        "-s",
        "--specs",
        action="store_const",
        const="specs",
        dest="type",
        default="specs",
        help="treat entries as specs (default)",
    )
    type.add_argument(
        "-f",
        "--files",
        action="store_const",
        const="files",
        dest="type",
        default="specs",
        help="treat entries as absolute filenames\n\ncannot be used with '-a'",
    )


def verify(parser, args):
    local = args.local

    if args.type == "files":
        if args.all:
            setup_parser.parser.print_help()
            return 1

        for file in args.specs_or_files:
            results = spack.verify.check_file_manifest(file)
            if results.has_errors():
                if args.json:
                    print(results.json_string())
                else:
                    print(results)

        return 0
    else:
        spec_args = spack.cmd.parse_specs(args.specs_or_files)

    if args.all:
        query = spack.store.STORE.db.query_local if local else spack.store.STORE.db.query

        # construct spec list
        if spec_args:
            spec_list = spack.cmd.parse_specs(args.specs_or_files)
            specs = []
            for spec in spec_list:
                specs += query(spec, installed=True)
        else:
            specs = query(installed=True)

    elif args.specs_or_files:
        # construct disambiguated spec list
        env = ev.active_environment()
        specs = list(map(lambda x: spack.cmd.disambiguate_spec(x, env, local=local), spec_args))
    else:
        setup_parser.parser.print_help()
        return 1

    for spec in specs:
        tty.debug("Verifying package %s")
        results = spack.verify.check_spec_manifest(spec)
        if results.has_errors():
            if args.json:
                print(results.json_string())
            else:
                tty.msg("In package %s" % spec.format("{name}/{hash:7}"))
                print(results)
            return 1
        else:
            tty.debug(results)
