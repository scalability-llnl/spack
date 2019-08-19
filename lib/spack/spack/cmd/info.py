# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import textwrap
from six.moves import zip_longest

import llnl.util.tty.color as color
from llnl.util.tty.colify import colify

import spack.repo
import spack.spec
import spack.fetch_strategy as fs


description = 'get detailed information on a particular package'
section = 'basic'
level = 'short'

header_color = '@*b'
plain_format = '@.'


def padder(str_list, extra=0):
    """Return a function to pad elements of a list."""
    length = max(len(str(s)) for s in str_list) + extra

    def pad(string):
        string = str(string)
        padding = max(0, length - len(string))
        return string + (padding * ' ')
    return pad


def setup_parser(subparser):
    subparser.add_argument(
        'name', metavar='PACKAGE', help='name of package to get info for')


def section_title(s):
    return header_color + s + plain_format


def version(s):
    return spack.spec.version_color + s + plain_format


def variant(s):
    return spack.spec.enabled_variant_color + s + plain_format


class VariantFormatter(object):
    def __init__(self, variants, max_widths=(30, 20, 30)):
        self.variants = variants
        self.headers = ('Name [Default]', 'Allowed values', 'Description')
        # Set max headers lengths
        self.max_column_widths = max_widths

        # Formats
        fmt_name = '{0} [{1}]'

        # Initialize column widths with the length of the
        # corresponding headers, as they cannot be shorter
        # than that
        self.column_widths = [len(x) for x in self.headers]

        # Update according to line lengths
        for k, v in variants.items():
            candidate_max_widths = (
                len(fmt_name.format(k, self.default(v))),  # Name [Default]
                len(v.allowed_values),  # Allowed values
                len(v.description)  # Description
            )

            self.column_widths = (
                max(self.column_widths[0], candidate_max_widths[0]),
                max(self.column_widths[1], candidate_max_widths[1]),
                max(self.column_widths[2], candidate_max_widths[2])
            )

        # Reduce to at most the maximum allowed
        self.column_widths = (
            min(self.column_widths[0], self.max_column_widths[0]),
            min(self.column_widths[1], self.max_column_widths[1]),
            min(self.column_widths[2], self.max_column_widths[2])
        )

        # Compute the format
        self.fmt = "%%-%ss%%-%ss%%s" % (
            self.column_widths[0] + 4,
            self.column_widths[1] + 4
        )

    def default(self, v):
        s = 'on' if v.default is True else 'off'
        if not isinstance(v.default, bool):
            s = v.default
        return s

    @property
    def lines(self):
        if not self.variants:
            yield '    None'
        else:
            yield '    ' + self.fmt % self.headers
            yield '\n'
            for k, v in sorted(self.variants.items()):
                name = textwrap.wrap(
                    '{0} [{1}]'.format(k, self.default(v)),
                    width=self.column_widths[0]
                )
                allowed = textwrap.wrap(
                    v.allowed_values,
                    width=self.column_widths[1]
                )
                description = textwrap.wrap(
                    v.description,
                    width=self.column_widths[2]
                )
                for t in zip_longest(
                        name, allowed, description, fillvalue=''
                ):
                    yield "    " + self.fmt % t


def print_text_info(pkg):
    """Print out a plain text description of a package."""

    header = section_title(
        '{0}:   '
    ).format(pkg.build_system_class) + pkg.name
    color.cprint(header)

    color.cprint('')
    color.cprint(section_title('Description:'))
    if pkg.__doc__:
        color.cprint(color.cescape(pkg.format_doc(indent=4)))
    else:
        color.cprint("    None")

    color.cprint(section_title('Caveats:'))
    if pkg.caveats():
        color.cprint(color.cescape(pkg.format_caveats(indent=4)))
    else:
        color.cprint("    None")
    print("")                   # consistent line spacing, caveat or not

    color.cprint(section_title('Homepage: ') + pkg.homepage)

    if len(pkg.maintainers) > 0:
        mnt = " ".join(['@@' + m for m in pkg.maintainers])
        color.cprint('')
        color.cprint(section_title('Maintainers: ') + mnt)

    color.cprint('')
    color.cprint(section_title("Tags: "))
    if hasattr(pkg, 'tags'):
        tags = sorted(pkg.tags)
        colify(tags, indent=4)
    else:
        color.cprint("    None")

    color.cprint('')
    color.cprint(section_title('Preferred version:  '))

    if not pkg.versions:
        color.cprint(version('    None'))
        color.cprint('')
        color.cprint(section_title('Safe versions:  '))
        color.cprint(version('    None'))
    else:
        pad = padder(pkg.versions, 4)

        # Here we sort first on the fact that a version is marked
        # as preferred in the package, then on the fact that the
        # version is not develop, then lexicographically
        key_fn = lambda v: (pkg.versions[v].get('preferred', False),
                            not v.isdevelop(),
                            v)
        preferred = sorted(pkg.versions, key=key_fn).pop()

        f = fs.for_package_version(pkg, preferred)
        line = version('    {0}'.format(pad(preferred))) + color.cescape(f)
        color.cprint(line)
        color.cprint('')
        color.cprint(section_title('Safe versions:  '))

        for v in reversed(sorted(pkg.versions)):
            f = fs.for_package_version(pkg, v)
            line = version('    {0}'.format(pad(v))) + color.cescape(f)
            color.cprint(line)

    color.cprint('')
    color.cprint(section_title('Variants:'))

    formatter = VariantFormatter(pkg.variants)
    for line in formatter.lines:
        color.cprint(line)

    color.cprint('')
    color.cprint(section_title('Installation Phases:'))
    phase_str = ''
    for phase in pkg.phases:
        phase_str += "    {0}".format(phase)
    color.cprint(phase_str)

    for deptype in ('build', 'link', 'run'):
        color.cprint('')
        color.cprint(section_title('%s Dependencies:' % deptype.capitalize()))
        deps = sorted(pkg.dependencies_of_type(deptype))
        if deps:
            colify(deps, indent=4)
        else:
            color.cprint('    None')

    color.cprint('')
    color.cprint(section_title('Virtual Packages: '))
    if pkg.provided:
        inverse_map = {}
        for spec, whens in pkg.provided.items():
            for when in whens:
                if when not in inverse_map:
                    inverse_map[when] = set()
                inverse_map[when].add(spec)
        for when, specs in reversed(sorted(inverse_map.items())):
            line = "    %s provides %s" % (
                when.colorized(), ', '.join(s.colorized() for s in specs)
            )
            print(line)

    else:
        color.cprint("    None")

    color.cprint('')


def info(parser, args):
    pkg = spack.repo.get(args.name)
    print_text_info(pkg)
