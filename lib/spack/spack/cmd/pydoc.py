# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


description = "run pydoc from within spack"
section = "developer"
level = "long"


def setup_parser(subparser):
    subparser.add_argument("entity", help="run pydoc help on entity")


def pydoc(parser, args):
    help(args.entity)
