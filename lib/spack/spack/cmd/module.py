# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from typing import Callable, Dict

import spack.cmd.modules.lmod
import spack.cmd.modules.tcl

description = "generate/manage module files"
section = "user environment"
level = "short"


_subcommands: Dict[str, Callable] = {}


def setup_parser(subparser):
    sp = subparser.add_subparsers(metavar="SUBCOMMAND", dest="module_command")
    spack.cmd.modules.lmod.add_command(sp, _subcommands)
    spack.cmd.modules.tcl.add_command(sp, _subcommands)


def module(parser, args):
    _subcommands[args.module_command](parser, args)
