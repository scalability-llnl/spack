# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys
import textwrap
from itertools import zip_longest

import llnl.util.tty as tty
import llnl.util.tty.color as color
from llnl.util.tty.colify import colify

import spack.deptypes as dt
import spack.fetch_strategy as fs
import spack.install_test
import spack.repo
import spack.spec
import spack.variant
from spack.cmd.common import arguments
from spack.package_base import preferred_version

description = "get detailed information on a particular package"
section = "basic"
level = "short"

header_color = "@*b"
plain_format = "@."


def padder(str_list, extra=0):
    """Return a function to pad elements of a list."""
    length = max(len(str(s)) for s in str_list) + extra

    def pad(string):
        string = str(string)
        padding = max(0, length - len(string))
        return string + (padding * " ")

    return pad


def setup_parser(subparser):
    subparser.add_argument(
        "-a", "--all", action="store_true", default=False, help="output all package information"
    )

    options = [
        ("--detectable", print_detectable.__doc__),
        ("--maintainers", print_maintainers.__doc__),
        ("--namespace", print_namespace.__doc__),
        ("--no-dependencies", "do not " + print_dependencies.__doc__),
        ("--no-variants", "do not " + print_variants.__doc__),
        ("--no-versions", "do not " + print_versions.__doc__),
        ("--phases", print_phases.__doc__),
        ("--tags", print_tags.__doc__),
        ("--tests", print_tests.__doc__),
        ("--virtuals", print_virtuals.__doc__),
        ("--variants-by-name", "list variants in strict name order; don't group by condition"),
    ]
    for opt, help_comment in options:
        subparser.add_argument(opt, action="store_true", help=help_comment)

    arguments.add_common_arguments(subparser, ["package"])


def section_title(s):
    return header_color + s + plain_format


def version(s):
    return spack.spec.VERSION_COLOR + s + plain_format


def variant(s):
    return spack.spec.ENABLED_VARIANT_COLOR + s + plain_format


def license(s):
    return spack.spec.VERSION_COLOR + s + plain_format


class VariantFormatter:
    def __init__(self, pkg):
        self.variants = pkg.variants
        self.headers = ("Name [Default]", "When", "Allowed values", "Description")

        # Don't let name or possible values be less than max widths
        _, cols = tty.terminal_size()
        max_name = min(self.column_widths[0], 30)
        max_when = min(self.column_widths[1], 30)
        max_vals = min(self.column_widths[2], 20)

        # allow the description column to extend as wide as the terminal.
        max_description = min(
            self.column_widths[3],
            # min width 70 cols, 14 cols of margins and column spacing
            max(cols, 70) - max_name - max_vals - 14,
        )
        self.column_widths = (max_name, max_when, max_vals, max_description)

        # Compute the format
        self.fmt = "%%-%ss%%-%ss%%-%ss%%s" % (
            self.column_widths[0] + 4,
            self.column_widths[1] + 4,
            self.column_widths[2] + 4,
        )

    def default(self, v):
        s = "on" if v.default is True else "off"
        if not isinstance(v.default, bool):
            s = v.default
        return s

    @property
    def lines(self):
        if not self.variants:
            yield "    None"
            return

        else:
            yield "    " + self.fmt % self.headers
            underline = tuple([w * "=" for w in self.column_widths])
            yield "    " + self.fmt % underline
            yield ""
            for k, e in sorted(self.variants.items()):
                v, w = e
                name = textwrap.wrap(
                    "{0} [{1}]".format(k, self.default(v)), width=self.column_widths[0]
                )
                if all(spec == spack.spec.Spec() for spec in w):
                    w = "--"
                when = textwrap.wrap(str(w), width=self.column_widths[1])
                allowed = v.allowed_values.replace("True, False", "on, off")
                allowed = textwrap.wrap(allowed, width=self.column_widths[2])
                description = []
                for d_line in v.description.split("\n"):
                    description += textwrap.wrap(d_line, width=self.column_widths[3])
                for t in zip_longest(name, when, allowed, description, fillvalue=""):
                    yield "    " + self.fmt % t


def print_dependencies(pkg, args):
    """output build, link, and run package dependencies"""

    for deptype in ("build", "link", "run"):
        color.cprint("")
        color.cprint(section_title("%s Dependencies:" % deptype.capitalize()))
        deps = sorted(pkg.dependencies_of_type(dt.flag_from_string(deptype)))
        if deps:
            colify(deps, indent=4)
        else:
            color.cprint("    None")


def print_detectable(pkg, args):
    """output information on external detection"""

    color.cprint("")
    color.cprint(section_title("Externally Detectable: "))

    # If the package has an 'executables' of 'libraries' field, it
    # can detect an installation
    if hasattr(pkg, "executables") or hasattr(pkg, "libraries"):
        find_attributes = []
        if hasattr(pkg, "determine_version"):
            find_attributes.append("version")

        if hasattr(pkg, "determine_variants"):
            find_attributes.append("variants")

        # If the package does not define 'determine_version' nor
        # 'determine_variants', then it must use some custom detection
        # mechanism. In this case, just inform the user it's detectable somehow.
        color.cprint(
            "    True{0}".format(
                " (" + ", ".join(find_attributes) + ")" if find_attributes else ""
            )
        )
    else:
        color.cprint("    False")


def print_maintainers(pkg, args):
    """output package maintainers"""

    if len(pkg.maintainers) > 0:
        mnt = " ".join(["@@" + m for m in pkg.maintainers])
        color.cprint("")
        color.cprint(section_title("Maintainers: ") + mnt)


def print_namespace(pkg, args):
    """output package namespace"""

    repo = spack.repo.PATH.get_repo(pkg.namespace)
    color.cprint("")
    color.cprint(section_title("Namespace:"))
    color.cprint(f"    @c{{{repo.namespace}}} at {repo.root}")


def print_phases(pkg, args):
    """output installation phases"""

    if hasattr(pkg.builder, "phases") and pkg.builder.phases:
        color.cprint("")
        color.cprint(section_title("Installation Phases:"))
        phase_str = ""
        for phase in pkg.builder.phases:
            phase_str += "    {0}".format(phase)
        color.cprint(phase_str)


def print_tags(pkg, args):
    """output package tags"""

    color.cprint("")
    color.cprint(section_title("Tags: "))
    if hasattr(pkg, "tags"):
        tags = sorted(pkg.tags)
        colify(tags, indent=4)
    else:
        color.cprint("    None")


def print_tests(pkg, args):
    """output relevant build-time and stand-alone tests"""

    # Some built-in base packages (e.g., Autotools) define callback (e.g.,
    # check) inherited by descendant packages. These checks may not result
    # in build-time testing if the package's build does not implement the
    # expected functionality (e.g., a 'check' or 'test' targets).
    #
    # So the presence of a callback in Spack does not necessarily correspond
    # to the actual presence of built-time tests for a package.
    for callbacks, phase in [
        (getattr(pkg, "build_time_test_callbacks", None), "Build"),
        (getattr(pkg, "install_time_test_callbacks", None), "Install"),
    ]:
        color.cprint("")
        color.cprint(section_title("Available {0} Phase Test Methods:".format(phase)))
        names = []
        if callbacks:
            for name in callbacks:
                if getattr(pkg, name, False):
                    names.append(name)

        if names:
            colify(sorted(names), indent=4)
        else:
            color.cprint("    None")

    # PackageBase defines an empty install/smoke test but we want to know
    # if it has been overridden and, therefore, assumed to be implemented.
    color.cprint("")
    color.cprint(section_title("Stand-Alone/Smoke Test Methods:"))
    names = spack.install_test.test_function_names(pkg, add_virtuals=True)
    if names:
        colify(sorted(names), indent=4)
    else:
        color.cprint("    None")


def _fmt_value(v):
    if v is None or isinstance(v, bool):
        return str(v).lower()
    else:
        return str(v)


def _fmt_name_and_default(variant):
    """Print colorized name [default] for a variant."""
    return color.colorize(f"@c{{{variant.name}}} @C{{[{_fmt_value(variant.default)}]}}")


def _fmt_when(when: "spack.spec.Spec", indent: int):
    return color.colorize(f"{indent * ' '}@B{{when}} {color.cescape(str(when))}")


def _fmt_variant_description(variant, width, indent):
    """Format a variant's description, preserving explicit line breaks."""
    return "\n".join(
        textwrap.fill(
            line, width=width, initial_indent=indent * " ", subsequent_indent=indent * " "
        )
        for line in variant.description.split("\n")
    )


def _fmt_variant(variant, max_name_default_len, indent, when=None, out=None):
    out = out or sys.stdout

    _, cols = tty.terminal_size()

    name_and_default = _fmt_name_and_default(variant)
    name_default_len = color.clen(name_and_default)

    values = variant.values
    if not isinstance(variant.values, (tuple, list, spack.variant.DisjointSetsOfValues)):
        values = [variant.values]

    # put 'none' first, sort the rest by value
    sorted_values = sorted(values, key=lambda v: (v != "none", v))

    pad = 4  # min padding between 'name [default]' and values
    value_indent = (indent + max_name_default_len + pad) * " "  # left edge of values

    # This preserves any formatting (i.e., newlines) from how the description was
    # written in package.py, but still wraps long lines for small terminals.
    # This allows some packages to provide detailed help on their variants (see, e.g., gasnet).
    formatted_values = "\n".join(
        textwrap.wrap(
            f"{', '.join(_fmt_value(v) for v in sorted_values)}",
            width=cols - 2,
            initial_indent=value_indent,
            subsequent_indent=value_indent,
        )
    )
    formatted_values = formatted_values[indent + name_default_len + pad :]

    # name [default]   value1, value2, value3, ...
    padding = pad * " "
    color.cprint(f"{indent * ' '}{name_and_default}{padding}@c{{{formatted_values}}}", stream=out)

    # when <spec>
    description_indent = indent + 4
    if when is not None and when != spack.spec.Spec():
        out.write(_fmt_when(when, description_indent - 2))
        out.write("\n")

    # description, preserving explicit line breaks from the way it's written in the package file
    out.write(_fmt_variant_description(variant, cols - 2, description_indent))
    out.write("\n")


def _print_variants_header(pkg):
    """output variants"""

    if not pkg.variants:
        print("    None")
        return

    color.cprint("")
    color.cprint(section_title("Variants:"))

    # Calculate the max length of the "name [default]" part of the variant display
    # This lets us know where to print variant values.
    max_name_default_len = max(
        color.clen(_fmt_name_and_default(variant))
        for name in pkg.variant_names()
        for _, variant in pkg.variant_definitions(name)
    )

    return max_name_default_len


def print_variants_grouped_by_when(pkg):
    max_name_default_len = _print_variants_header(pkg)

    indent = 4
    for when, variants_by_name in pkg.variant_items():
        padded_values = max_name_default_len + 4
        start_indent = indent

        if when != spack.spec.Spec():
            sys.stdout.write("\n")
            sys.stdout.write(_fmt_when(when, indent))
            sys.stdout.write("\n")

            # indent names slightly inside 'when', but line up values
            padded_values -= 2
            start_indent += 2

        for name, variant in sorted(variants_by_name.items()):
            _fmt_variant(variant, padded_values, start_indent, None, out=sys.stdout)


def print_variants_by_name(pkg):
    max_name_default_len = _print_variants_header(pkg)
    max_name_default_len += 4

    indent = 4
    for name in pkg.variant_names():
        for when, variant in pkg.variant_definitions(name):
            _fmt_variant(variant, max_name_default_len, indent, when, out=sys.stdout)
            sys.stdout.write("\n")


def print_variants(pkg, args):
    """output variants"""
    if args.variants_by_name:
        print_variants_by_name(pkg)
    else:
        print_variants_grouped_by_when(pkg)


def print_versions(pkg, args):
    """output versions"""

    color.cprint("")
    color.cprint(section_title("Preferred version:  "))

    if not pkg.versions:
        color.cprint(version("    None"))
        color.cprint("")
        color.cprint(section_title("Safe versions:  "))
        color.cprint(version("    None"))
        color.cprint("")
        color.cprint(section_title("Deprecated versions:  "))
        color.cprint(version("    None"))
    else:
        pad = padder(pkg.versions, 4)

        preferred = preferred_version(pkg)

        def get_url(version):
            try:
                return fs.for_package_version(pkg, version)
            except spack.fetch_strategy.InvalidArgsError:
                return "No URL"

        url = get_url(preferred) if pkg.has_code else ""
        line = version("    {0}".format(pad(preferred))) + color.cescape(str(url))
        color.cwrite(line)

        print()

        safe = []
        deprecated = []
        for v in reversed(sorted(pkg.versions)):
            if pkg.has_code:
                url = get_url(v)
            if pkg.versions[v].get("deprecated", False):
                deprecated.append((v, url))
            else:
                safe.append((v, url))

        for title, vers in [("Safe", safe), ("Deprecated", deprecated)]:
            color.cprint("")
            color.cprint(section_title("{0} versions:  ".format(title)))
            if not vers:
                color.cprint(version("    None"))
                continue

            for v, url in vers:
                line = version("    {0}".format(pad(v))) + color.cescape(str(url))
                color.cprint(line)


def print_virtuals(pkg, args):
    """output virtual packages"""

    color.cprint("")
    color.cprint(section_title("Virtual Packages: "))
    if pkg.provided:
        for when, specs in reversed(sorted(pkg.provided.items())):
            line = "    %s provides %s" % (when.cformat(), ", ".join(s.cformat() for s in specs))
            print(line)

    else:
        color.cprint("    None")


def print_licenses(pkg, args):
    """Output the licenses of the project."""

    color.cprint("")
    color.cprint(section_title("Licenses: "))

    if len(pkg.licenses) == 0:
        color.cprint("    None")
    else:
        pad = padder(pkg.licenses, 4)
        for when_spec in pkg.licenses:
            license_identifier = pkg.licenses[when_spec]
            line = license("    {0}".format(pad(license_identifier))) + color.cescape(
                str(when_spec)
            )
            color.cprint(line)


def info(parser, args):
    spec = spack.spec.Spec(args.package)
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.fullname)
    pkg = pkg_cls(spec)

    # Output core package information
    header = section_title("{0}:   ").format(pkg.build_system_class) + pkg.name
    color.cprint(header)

    color.cprint("")
    color.cprint(section_title("Description:"))
    if pkg.__doc__:
        color.cprint(color.cescape(pkg.format_doc(indent=4)))
    else:
        color.cprint("    None")

    if getattr(pkg, "homepage"):
        color.cprint(section_title("Homepage: ") + pkg.homepage)

    # Now output optional information in expected order
    sections = [
        (args.all or args.maintainers, print_maintainers),
        (args.all or args.namespace, print_namespace),
        (args.all or args.detectable, print_detectable),
        (args.all or args.tags, print_tags),
        (args.all or not args.no_versions, print_versions),
        (args.all or not args.no_variants, print_variants),
        (args.all or args.phases, print_phases),
        (args.all or not args.no_dependencies, print_dependencies),
        (args.all or args.virtuals, print_virtuals),
        (args.all or args.tests, print_tests),
        (args.all or True, print_licenses),
    ]
    for print_it, func in sections:
        if print_it:
            func(pkg, args)

    color.cprint("")
