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
import cgi
from StringIO import StringIO
from llnl.util.tty.colify import *
import spack

description = "Print a list of all packages in reStructuredText."


def github_url(pkg):
    """Link to a package file on github."""
    url = "https://github.com/LLNL/spack/blob/develop/var/spack/repos/builtin/packages/{0}/package.py"
    return url.format(pkg.name)


def rst_table(elts):
    """Print out a RST-style table."""
    cols = StringIO()
    ncol, widths = colify(elts, output=cols, tty=True)
    header = " ".join("=" * (w - 1) for w in widths)
    return "%s\n%s%s" % (header, cols.getvalue(), header)


def print_rst_package_list():
    """Print out information on all packages in restructured text."""
    pkgs = sorted(spack.repo.all_packages(), key=lambda s: s.name.lower())
    pkg_names = [p.name for p in pkgs]

    print ".. _package-list:"
    print
    print "============"
    print "Package List"
    print "============"
    print
    print "This is a list of things you can install using Spack.  It is"
    print "automatically generated based on the packages in the latest Spack"
    print "release."
    print
    print "Spack currently has %d mainline packages:" % len(pkgs)
    print
    print rst_table("`%s`_" % p for p in pkg_names)
    print

    # Output some text for each package.
    for pkg in pkgs:
        print "-----"
        print
        print ".. _%s:" % pkg.name
        print
        # Must be at least 2 long, breaks for single letter packages like R.
        print "-" * max(len(pkg.name), 2)
        print pkg.name
        print "-" * max(len(pkg.name), 2)
        print
        print "Homepage:"
        print "  * `%s <%s>`__" % (cgi.escape(pkg.homepage), pkg.homepage)
        print
        print "Spack package:"
        print "  * `%s/package.py <%s>`__" % (pkg.name, github_url(pkg))
        print
        if pkg.versions:
            print "Versions:"
            print "  " + ", ".join(str(v) for v in
                                   reversed(sorted(pkg.versions)))
            print

        for deptype in spack.alldeps:
            deps = pkg.dependencies_of_type(deptype)
            if deps:
                print "%s Dependencies" % deptype.capitalize()
                print "  " + ", ".join("%s_" % d if d in pkg_names
                                       else d for d in deps)
                print

        print "Description:"
        print pkg.format_doc(indent=2)
        print


def package_list(parser, args):
    print_rst_package_list()
