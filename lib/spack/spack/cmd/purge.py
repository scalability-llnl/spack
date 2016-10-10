##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import spack
import spack.stage as stage

description = "Remove temporary build files and/or downloaded archives"


def setup_parser(subparser):
    subparser.add_argument(
        '-s', '--stage', action='store_true', default=True,
        help="Remove all temporary build stages (default).")
    subparser.add_argument(
        '-d', '--downloads', action='store_true',
        help="Remove cached downloads.")
    subparser.add_argument(
        '-u', '--user-cache', action='store_true',
        help="Remove caches in user home directory. Includes virtual indices.")
    subparser.add_argument(
        '-a', '--all', action='store_true',
        help="Remove all of the above.")


def purge(parser, args):
    # Special case: no flags.
    if not any((args.stage, args.downloads, args.user_cache, args.all)):
        stage.purge()
        return

    # handle other flags with fall through.
    if args.stage or args.all:
        stage.purge()
    if args.downloads or args.all:
        spack.fetch_cache.destroy()
    if args.user_cache or args.all:
        spack.user_cache.destroy()
