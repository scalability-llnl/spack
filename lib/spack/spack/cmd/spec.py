##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack.util import argparse
import spack.cmd

import llnl.util.tty as tty

import spack
import spack.url as url

description = "print out abstract and concrete versions of a spec."

def setup_parser(subparser):
    subparser.add_argument('-i', '--ids', action='store_true',
                           help="show numerical ids for dependencies.")
    subparser.add_argument('specs', nargs=argparse.REMAINDER, help="specs of packages")


def spec(parser, args):
    kwargs = { 'ids'    : args.ids,
               'indent' : 2,
               'color'  : True }

    for spec in spack.cmd.parse_specs(args.specs):
        print "Input spec"
        print "------------------------------"
        print spec.tree(**kwargs)

        print "Normalized"
        print "------------------------------"
        spec.normalize()
        print spec.tree(**kwargs)

        print "Concretized"
        print "------------------------------"
        spec.concretize()
        print spec.tree(**kwargs)
