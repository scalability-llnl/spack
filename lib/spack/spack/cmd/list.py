# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function
from __future__ import division

import argparse
import fnmatch
import os
import re
import sys
import math
import json

import llnl.util.tty as tty
from llnl.util.tty.colify import colify

import spack.dependency
import spack.repo
import spack.cmd.common.arguments as arguments
from spack.version import VersionList

if sys.version_info > (3, 1):
    from html import escape  # novm
else:
    from cgi import escape

description = "list and search available packages"
section = "basic"
level = "short"


formatters = {}


def formatter(func):
    """Decorator used to register formatters"""
    formatters[func.__name__] = func
    return func


def setup_parser(subparser):
    subparser.add_argument(
        'filter', nargs=argparse.REMAINDER,
        help='optional case-insensitive glob patterns to filter results')
    subparser.add_argument(
        '-d', '--search-description', action='store_true', default=False,
        help='filtering will also search the description for a match')
    subparser.add_argument(
        '--format', default='name_only', choices=formatters,
        help='format to be used to print the output [default: name_only]')
    subparser.add_argument(
        '--update', metavar='FILE', default=None, action='store',
        help='write output to the specified file, if any package is newer')
    subparser.add_argument(
        '-v', '--virtuals', action='store_true', default=False,
        help='include virtual packages in list')

    arguments.add_common_arguments(subparser, ['tags'])


def filter_by_name(pkgs, args):
    """
    Filters the sequence of packages according to user prescriptions

    Args:
        pkgs: sequence of packages
        args: parsed command line arguments

    Returns:
        filtered and sorted list of packages
    """
    if args.filter:
        res = []
        for f in args.filter:
            if '*' not in f and '?' not in f:
                r = fnmatch.translate('*' + f + '*')
            else:
                r = fnmatch.translate(f)

            rc = re.compile(r, flags=re.IGNORECASE)
            res.append(rc)

        if args.search_description:
            def match(p, f):
                if f.match(p):
                    return True

                pkg = spack.repo.get(p)
                if pkg.__doc__:
                    return f.match(pkg.__doc__)
                return False
        else:
            def match(p, f):
                return f.match(p)
        pkgs = [p for p in pkgs if any(match(p, f) for f in res)]

    return sorted(pkgs, key=lambda s: s.lower())


@formatter
def name_only(pkgs, out):
    indent = 0
    if out.isatty():
        tty.msg("%d packages." % len(pkgs))
    colify(pkgs, indent=indent, output=out)


def github_url(pkg):
    """Link to a package file on github."""
    url = 'https://github.com/spack/spack/blob/develop/var/spack/repos/builtin/packages/{0}/package.py'
    return url.format(pkg.name)


def rows_for_ncols(elts, ncols):
    """Print out rows in a table with ncols of elts laid out vertically."""
    clen = int(math.ceil(len(elts) / ncols))
    for r in range(clen):
        row = []
        for c in range(ncols):
            i = c * clen + r
            row.append(elts[i] if i < len(elts) else None)
        yield row


def get_dependencies(pkg):
    all_deps = {}
    for deptype in spack.dependency.all_deptypes:
        deps = pkg.dependencies_of_type(deptype)
        all_deps[deptype] = [d for d in deps]

    return all_deps


@formatter
def version_json(pkg_names, out):
    """Print all packages with their latest versions."""
    pkgs = [spack.repo.get(name) for name in pkg_names]

    out.write('[\n')

    # output name and latest version for each package
    pkg_latest = ",\n".join([
        '  {{"name": "{0}",\n'
        '   "latest_version": "{1}",\n'
        '   "versions": {2},\n'
        '   "homepage": "{3}",\n'
        '   "file": "{4}",\n'
        '   "maintainers": {5},\n'
        '   "dependencies": {6}'
        '}}'.format(
            pkg.name,
            VersionList(pkg.versions).preferred(),
            json.dumps([str(v) for v in reversed(sorted(pkg.versions))]),
            pkg.homepage,
            github_url(pkg),
            json.dumps(pkg.maintainers),
            json.dumps(get_dependencies(pkg))
        ) for pkg in pkgs
    ])
    out.write(pkg_latest)
    # important: no trailing comma in JSON arrays
    out.write('\n]\n')


@formatter
def html(pkg_names, out):
    """Print out information on all packages in Sphinx HTML.

    This is intended to be inlined directly into Sphinx documentation.
    We write HTML instead of RST for speed; generating RST from *all*
    packages causes the Sphinx build to take forever. Including this as
    raw HTML is much faster.
    """

    # Read in all packages
    pkgs = [spack.repo.get(name) for name in pkg_names]

    # Start at 2 because the title of the page from Sphinx is id1.
    span_id = 2

    # HTML header with an increasing id span
    def head(n, span_id, title, anchor=None):
        if anchor is None:
            anchor = title
        out.write(('<span id="id%d"></span>'
                   '<h1>%s<a class="headerlink" href="#%s" '
                   'title="Permalink to this headline">&para;</a>'
                   '</h1>\n') % (span_id, title, anchor))

    # Start with the number of packages, skipping the title and intro
    # blurb, which we maintain in the RST file.
    out.write('<p>\n')
    out.write('Spack currently has %d mainline packages:\n' % len(pkgs))
    out.write('</p>\n')

    # Table of links to all packages
    out.write('<table border="1" class="docutils">\n')
    out.write('<tbody valign="top">\n')
    for i, row in enumerate(rows_for_ncols(pkg_names, 3)):
        out.write('<tr class="row-odd">\n' if i % 2 == 0 else
                  '<tr class="row-even">\n')
        for name in row:
            out.write('<td>\n')
            out.write('<a class="reference internal" href="#%s">%s</a></td>\n'
                      % (name, name))
            out.write('</td>\n')
        out.write('</tr>\n')
    out.write('</tbody>\n')
    out.write('</table>\n')
    out.write('<hr class="docutils"/>\n')

    # Output some text for each package.
    for pkg in pkgs:
        out.write('<div class="section" id="%s">\n' % pkg.name)
        head(2, span_id, pkg.name)
        span_id += 1

        out.write('<dl class="docutils">\n')

        out.write('<dt>Homepage:</dt>\n')
        out.write('<dd><ul class="first last simple">\n')
        out.write(('<li>'
                   '<a class="reference external" href="%s">%s</a>'
                   '</li>\n') % (pkg.homepage, escape(pkg.homepage, True)))
        out.write('</ul></dd>\n')

        out.write('<dt>Spack package:</dt>\n')
        out.write('<dd><ul class="first last simple">\n')
        out.write(('<li>'
                   '<a class="reference external" href="%s">%s/package.py</a>'
                   '</li>\n') % (github_url(pkg), pkg.name))
        out.write('</ul></dd>\n')

        if pkg.versions:
            out.write('<dt>Versions:</dt>\n')
            out.write('<dd>\n')
            out.write(', '.join(
                str(v) for v in reversed(sorted(pkg.versions))))
            out.write('\n')
            out.write('</dd>\n')

        for deptype in spack.dependency.all_deptypes:
            deps = pkg.dependencies_of_type(deptype)
            if deps:
                out.write('<dt>%s Dependencies:</dt>\n' % deptype.capitalize())
                out.write('<dd>\n')
                out.write(', '.join(
                    d if d not in pkg_names else
                    '<a class="reference internal" href="#%s">%s</a>' % (d, d)
                    for d in deps))
                out.write('\n')
                out.write('</dd>\n')

        out.write('<dt>Description:</dt>\n')
        out.write('<dd>\n')
        out.write(escape(pkg.format_doc(indent=2), True))
        out.write('\n')
        out.write('</dd>\n')
        out.write('</dl>\n')

        out.write('<hr class="docutils"/>\n')
        out.write('</div>\n')


def list(parser, args):
    # retrieve the formatter to use from args
    formatter = formatters[args.format]

    # Retrieve the names of all the packages
    pkgs = set(spack.repo.all_package_names(args.virtuals))
    # Filter the set appropriately
    sorted_packages = filter_by_name(pkgs, args)

    # Filter by tags
    if args.tags:
        packages_with_tags = set(
            spack.repo.path.packages_with_tags(*args.tags))
        sorted_packages = set(sorted_packages) & packages_with_tags
        sorted_packages = sorted(sorted_packages)

    if args.update:
        # change output stream if user asked for update
        if os.path.exists(args.update):
            if os.path.getmtime(args.update) > spack.repo.path.last_mtime():
                tty.msg('File is up to date: %s' % args.update)
                return

        tty.msg('Updating file: %s' % args.update)
        with open(args.update, 'w') as f:
            formatter(sorted_packages, f)

    else:
        # Print to stdout
        formatter(sorted_packages, sys.stdout)
