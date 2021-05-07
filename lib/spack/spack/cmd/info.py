# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from __future__ import print_function

import inspect
import textwrap
from six.moves import zip_longest

import llnl.util.tty as tty
import llnl.util.tty.color as color
from llnl.util.tty.colify import colify

import spack.cmd.common.arguments as arguments
import spack.repo
import spack.spec
import spack.fetch_strategy as fs
from spack.cmd.test import has_test_method


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
    arguments.add_common_arguments(subparser, ['package'])


def section_title(s):
    return header_color + s + plain_format


def version(s):
    return spack.spec.version_color + s + plain_format


def variant(s):
    return spack.spec.enabled_variant_color + s + plain_format


class VariantFormatter(object):
    def __init__(self, variants):
        self.variants = variants
        self.headers = ('Name [Default]', 'Allowed values', 'Description')

        # Formats
        fmt_name = '{0} [{1}]'

        # Initialize column widths with the length of the
        # corresponding headers, as they cannot be shorter
        # than that
        self.column_widths = [len(x) for x in self.headers]

        # Expand columns based on max line lengths
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

        # Don't let name or possible values be less than max widths
        _, cols = tty.terminal_size()
        max_name = min(self.column_widths[0], 30)
        max_vals = min(self.column_widths[1], 20)

        # allow the description column to extend as wide as the terminal.
        max_description = min(
            self.column_widths[2],
            # min width 70 cols, 14 cols of margins and column spacing
            max(cols, 70) - max_name - max_vals - 14,
        )
        self.column_widths = (max_name, max_vals, max_description)

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
            underline = tuple([w * "=" for w in self.column_widths])
            yield '    ' + self.fmt % underline
            yield ''
            for k, v in sorted(self.variants.items()):
                name = textwrap.wrap(
                    '{0} [{1}]'.format(k, self.default(v)),
                    width=self.column_widths[0]
                )
                allowed = v.allowed_values.replace('True, False', 'on, off')
                allowed = textwrap.wrap(allowed, width=self.column_widths[1])
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
        url = ''
        if pkg.has_code:
            url = fs.for_package_version(pkg, preferred)

        line = version('    {0}'.format(pad(preferred))) + color.cescape(url)
        color.cprint(line)
        color.cprint('')
        color.cprint(section_title('Safe versions:  '))

        for v in reversed(sorted(pkg.versions)):
            if not pkg.versions[v].get('deprecated', False):
                if pkg.has_code:
                    url = fs.for_package_version(pkg, v)
                line = version('    {0}'.format(pad(v))) + color.cescape(url)
                color.cprint(line)

    color.cprint('')
    color.cprint(section_title('Variants:'))

    formatter = VariantFormatter(pkg.variants)
    for line in formatter.lines:
        color.cprint(line)

    if hasattr(pkg, 'phases') and pkg.phases:
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

    # Some built-in base packages (e.g., Autotools) define callback (e.g.,
    # check) inherited by descendant packages. These checks may not result
    # in build-time testing if the package's build does not implement the
    # expected functionality (e.g., a 'check' or 'test' targets).
    #
    # So the presence of a callback in Spack does not necessarily correspond
    # to the actual presence of built-time tests for a package.
    for callbacks, phase in [(pkg.build_time_test_callbacks, 'Build'),
                             (pkg.install_time_test_callbacks, 'Install')]:
        color.cprint('')
        color.cprint(section_title('Available {0} Phase Test Methods:'
                                   .format(phase)))
        if callbacks:
            colify(sorted(callbacks), indent=4)
        else:
            color.cprint('    None')

    # PackageBase defines an empty install/smoke test but we want to know
    # if it has been overridden and, therefore, assumed to be implemented.
    color.cprint('')
    color.cprint(section_title('Stand-Alone/Smoke Test Methods:'))
    names = []
    if has_test_method(pkg):
        pkg_base = spack.package.PackageBase
        test_pkgs = [str(cls.test) for cls in inspect.getmro(pkg) if
                     issubclass(cls, pkg_base) and cls.test != pkg_base.test]
        test_pkgs = list(set(test_pkgs))
        names.extend([(test.split()[1]).lower() for test in test_pkgs])

    # TODO Refactor START
    # Use code from package.py's test_process IF this functionality is
    # accepted.
    v_names = list(set([vspec.name for vspec in pkg.virtuals_provided]))

    # hack for compilers that are not dependencies (yet)
    # TODO: this all eventually goes away
    c_names = ('gcc', 'intel', 'intel-parallel-studio', 'pgi')
    if pkg.name in c_names:
        v_names.extend(['c', 'cxx', 'fortran'])
    if pkg.spec.satisfies('llvm+clang'):
        v_names.extend(['c', 'cxx'])
    # TODO Refactor END

    v_specs = [spack.spec.Spec(v_name) for v_name in v_names]
    for v_spec in v_specs:
        try:
            if has_test_method(v_spec.package):
                names.append('{0}.test'.format(v_spec.package.name.lower()))
        except spack.repo.UnknownPackageError:
            pass

    if names:
        colify(sorted(names), indent=4)
    else:
        color.cprint('    None')

    color.cprint('')


def info(parser, args):
    pkg = spack.repo.get(args.package)
    print_text_info(pkg)
