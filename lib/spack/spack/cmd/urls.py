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
import spack.url

description = "Inspect urls used by packages in spack."


def setup_parser(subparser):
    subparser.add_argument(
        '-c', '--color', action='store_true',
        help="Color the parsed version and name in the urls shown.  "
             "Version will be cyan, name red.")
    subparser.add_argument(
        '-e', '--extrapolation', action='store_true',
        help="Color the versions used for extrapolation as well."
             "Additional versions are green, names magenta.")


def urls(parser, args):
    urls = set()
    for pkg in spack.repo.all_packages():
        url = getattr(pkg.__class__, 'url', None)
        if url:
            urls.add(url)

        for params in pkg.versions.values():
            url = params.get('url', None)
            if url:
                urls.add(url)

    for url in sorted(urls):
        if args.color or args.extrapolation:
            print spack.url.color_url(
                url, subs=args.extrapolation, errors=True)
        else:
            print url
