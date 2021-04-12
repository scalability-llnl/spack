# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import spack.cmd
import spack.cmd.common.arguments as arguments
import spack.environment as ev
import spack.util.environment
import spack.solver.asp as asp

import llnl.util.tty as tty
import llnl.util.tty.color as color
import spack.util.spack_json as sjson
import operator
import spack.cmd
import sys

description = "compare two specs"
section = "basic"
level = "long"


def setup_parser(subparser):
    arguments.add_common_arguments(
        subparser, ['specs'])

    subparser.add_argument(
        '--json',
        action='store_true',
        default=False,
        dest='dump_json',
        help="Dump json output instead of pretty printing."
    )
    subparser.add_argument(
        '--first',
        action='store_true',
        default=False,
        dest='load_first',
        help="load the first match if multiple packages match the spec"
    )
    subparser.add_argument(
        '-a',
        dest='attributes',
        action='append',
        choices=[
            'all', 'version', 'concrete', 'node', 'node_compiler_set',
            'node_compiler_version_set', 'node_os_set', 'node_platform_set',
            'node_target_set', 'variant_set'
        ],
        help="select the attributes to show (defaults to all)"
    )


def bold(string):
    """
    Make a header string bold so we can easily see it
    """
    return color.colorize("@*{%s}" % string)


def compare_specs(a, b, to_string=False, colorful=True):
    """
    Generate a comparison, including diffs (for each side) and an intersection.

    We can either print the result to the console, or parse
    into a json object for the user to save. We return an object that shows
    the differences, intersection, and names for a pair of specs a and b.

    Arguments:
        a (spec): the first spec to compare
        b (spec): the second spec to compare
        a_name (str): the name of spec a
        b_name (str): the name of spec b
        to_string (bool): return an object that can be json dumped
        colorful (bool): do not format the names for the console
    """
    # Prepare a solver setup to parse differences
    setup = asp.SpackSolverSetup()

    a_facts = set(to_tuple(t) for t in setup.spec_clauses(a))
    b_facts = set(to_tuple(t) for t in setup.spec_clauses(b))

    # We want to present them to the user as simple key: values
    intersect = list(a_facts.intersection(b_facts))
    spec1_not_spec2 = list(a_facts.difference(b_facts))
    spec2_not_spec1 = list(b_facts.difference(a_facts))

    # Format the spec names to be colored
    fmt = "{name}{@version}{/hash:7}"
    a_name = a.format(fmt, color=color.get_color_when())
    b_name = a.format(fmt, color=color.get_color_when())

    # We want to show what is the same, and then difference for each
    return {
        "intersect": flatten(intersect) if to_string else intersect,
        "a_not_b": flatten(spec1_not_spec2) if to_string else spec1_not_spec2,
        "b_not_a": flatten(spec2_not_spec1) if to_string else spec2_not_spec1,
        "a_name": a_name if colorful else a.format("{name}{@version}{/hash:7}"),
        "b_name": b_name if colorful else b.format("{name}{@version}{/hash:7}")
    }


def to_tuple(asp_function):
    """
    Prepare tuples of objects.

    If we need to save to json, convert to strings
    See https://gist.github.com/tgamblin/83eba3c6d27f90d9fa3afebfc049ceaf
    """
    args = []
    for arg in asp_function.args:
        if isinstance(arg, str):
            args.append(arg)
            continue
        args.append("%s(%s)" % (type(arg).__name__, str(arg)))
    return tuple([asp_function.name] + args)


def flatten(tuple_list):
    """
    Given a list of tuples, convert into a list of key: value tuples.

    We are squashing whatever is after the first index into one string for
    easier parsing in the interface
    """
    updated = []
    for item in tuple_list:
        updated.append([item[0], " ".join(item[1:])])
    return updated


def print_difference(diffset, attributes="all", out=None):
    """
    Print the difference.

    Given a diffset and a user preference (e.g., print versions or print all)
    print a tabular, organized version of the diffset
    """
    # Default to standard out unless another stream is provided
    out = out or sys.stdout

    # Cut out early if we don't have any differences!
    if not diffset:
        print("No differences\n")
        return

    # Sort by name so they are grouped together
    sorted_diffset = sorted(diffset, key=operator.itemgetter(0))

    # Always print a new category
    category = None
    for entry in sorted_diffset:
        if "all" in attributes or entry[0] in attributes:

            # If we have a new category, create a new section
            if category != entry[0]:
                category = entry[0]

                # print category in bold, colorized
                out.write(bold("%s\n" % category.upper()))

            # Write the attribute
            out.write("%s\n" % entry[1])


def diff(parser, args):
    env = ev.get_env(args, 'diff')

    if len(args.specs) != 2:
        tty.die("You must provide two specs to diff.")

    specs = [spack.cmd.disambiguate_spec(spec, env, first=args.load_first)
             for spec in spack.cmd.parse_specs(args.specs)]

    # Calculate the comparison (c)
    c = compare_specs(specs[0], specs[1], to_string=True,
                      colorful=not args.dump_json)

    # Default to all attributes
    attributes = args.attributes or ["all"]

    if args.dump_json:
        print(sjson.dump(c))
    else:
        tty.warn("This interface is subject to change.\n")

        # For each spec, print the differences wanted by the user
        tty.info("diff(%s, %s)" % (c['a_name'], c['b_name']))
        print_difference(c['a_not_b'], attributes)
        tty.info("diff(%s, %s)" % (c['b_name'], c['a_name']))
        print_difference(c['b_not_a'], attributes)
