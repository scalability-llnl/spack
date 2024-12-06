# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys

import llnl.util.tty as tty
from llnl.util.tty.color import cprint, get_color_when

import spack.cmd
import spack.environment as ev
import spack.solver.asp as asp
import spack.util.spack_json as sjson
from spack.cmd.common import arguments

description = "compare two specs"
section = "basic"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(subparser, ["specs"])

    subparser.add_argument(
        "--json",
        action="store_true",
        default=False,
        dest="dump_json",
        help="dump json output instead of pretty printing",
    )
    subparser.add_argument(
        "--first",
        action="store_true",
        default=False,
        dest="load_first",
        help="load the first match if multiple packages match the spec",
    )
    subparser.add_argument(
        "-a",
        "--attribute",
        action="append",
        help="select the attributes to show (defaults to all)",
    )
    subparser.add_argument(
        "--ignore", action="append", help="omit diffs related to these dependencies"
    )


def shift(asp_function):
    """Transforms ``attr("foo", "bar")`` into ``foo("bar")``."""
    if not asp_function.args:
        raise ValueError(f"Can't shift ASP function with no arguments: {str(asp_function)}")
    first, *rest = asp_function.args
    return asp.AspFunction(first, rest)


def compare_specs(a, b, to_string=False, color=None, ignore_packages=None):
    """
    Generate a comparison, including diffs (for each side) and an intersection.

    We can either print the result to the console, or parse
    into a json object for the user to save. We return an object that shows
    the differences, intersection, and names for a pair of specs a and b.

    Arguments:
        a (spack.spec.Spec): the first spec to compare
        b (spack.spec.Spec): the second spec to compare
        a_name (str): the name of spec a
        b_name (str): the name of spec b
        to_string (bool): return an object that can be json dumped
        color (bool): whether to format the names for the console
    """
    if color is None:
        color = get_color_when()

    a = a.copy()
    b = b.copy()

    if ignore_packages:
        for pkg_name in ignore_packages:
            a.trim(pkg_name)
            b.trim(pkg_name)

    # Prepare a solver setup to parse differences
    setup = asp.SpackSolverSetup()

    # get facts for specs, making sure to include build dependencies of concrete
    # specs and to descend into dependency hashes so we include all facts.
    a_facts = set(
        shift(func)
        for func in setup.spec_clauses(a, body=True, expand_hashes=True, concrete_build_deps=True)
        if func.name == "attr"
    )
    b_facts = set(
        shift(func)
        for func in setup.spec_clauses(b, body=True, expand_hashes=True, concrete_build_deps=True)
        if func.name == "attr"
    )

    # We want to present them to the user as simple key: values
    intersect = sorted(a_facts.intersection(b_facts))
    spec1_not_spec2 = sorted(a_facts.difference(b_facts))
    spec2_not_spec1 = sorted(b_facts.difference(a_facts))

    # Format the spec names to be colored
    fmt = "{name}{@version}{/hash}"
    a_name = a.format(fmt, color=color)
    b_name = b.format(fmt, color=color)

    # We want to show what is the same, and then difference for each
    return {
        "intersect": flatten(intersect) if to_string else intersect,
        "a_not_b": flatten(spec1_not_spec2) if to_string else spec1_not_spec2,
        "b_not_a": flatten(spec2_not_spec1) if to_string else spec2_not_spec1,
        "a_name": a_name,
        "b_name": b_name,
    }


def flatten(functions):
    """
    Given a list of ASP functions, convert into a list of key: value tuples.

    We are squashing whatever is after the first index into one string for
    easier parsing in the interface
    """
    updated = []
    for fun in functions:
        updated.append([fun.name, " ".join(str(a) for a in fun.args)])
    return updated


def print_difference(c, attributes="all", out=None):
    """
    Print the difference.

    Given a diffset for A and a diffset for B, print red/green diffs to show
    the differences.
    """
    # Default to standard out unless another stream is provided
    out = out or sys.stdout

    A = c["b_not_a"]
    B = c["a_not_b"]

    cprint("@R{--- %s}" % c["a_name"])  # bright red
    cprint("@G{+++ %s}" % c["b_name"])  # bright green

    # Cut out early if we don't have any differences!
    if not A and not B:
        print("No differences\n")
        return

    def group_by_type(diffset):
        grouped = {}
        for entry in diffset:
            if entry[0] not in grouped:
                grouped[entry[0]] = []
            grouped[entry[0]].append(entry[1])

        # Sort by second value to make comparison slightly closer
        for key, values in grouped.items():
            values.sort()
        return grouped

    A = group_by_type(A)
    B = group_by_type(B)

    # print a directionally relevant diff
    keys = list(A) + list(B)

    category = None
    for key in keys:
        if "all" not in attributes and key not in attributes:
            continue

        # Write the attribute, B is subtraction A is addition
        subtraction = [] if key not in B else B[key]
        addition = [] if key not in A else A[key]

        # Bail out early if we don't have any entries
        if not subtraction and not addition:
            continue

        # If we have a new category, create a new section
        if category != key:
            category = key

            # print category in bold, colorized
            cprint("@*b{@@ %s @@}" % category)  # bold blue

        # Print subtractions first
        while subtraction:
            cprint("@R{-  %s}" % subtraction.pop(0))  # bright red
            if addition:
                cprint("@G{+  %s}" % addition.pop(0))  # bright green

        # Any additions left?
        while addition:
            cprint("@G{+  %s}" % addition.pop(0))


def diff(parser, args):
    env = ev.active_environment()

    if len(args.specs) != 2:
        tty.die("You must provide two specs to diff.")

    specs = []
    for spec in spack.cmd.parse_specs(args.specs):
        # If the spec has a hash, check it before disambiguating
        spec.replace_hash()
        if spec.concrete:
            specs.append(spec)
        else:
            specs.append(spack.cmd.disambiguate_spec(spec, env, first=args.load_first))

    # Calculate the comparison (c)
    color = False if args.dump_json else get_color_when()
    c = compare_specs(specs[0], specs[1], to_string=True, color=color, ignore_packages=args.ignore)

    # Default to all attributes
    attributes = args.attribute or ["all"]

    if args.dump_json:
        print(sjson.dump(c))
    else:
        tty.warn("This interface is subject to change.\n")
        print_difference(c, attributes)
