# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Diffing functions for pairs of specs (and eventually other classes).
If you create a diff class, it should be named <Object>Diff and take as input
the two objects of that type to compare, with the first being the older
of the two (a) to compare against a newer object (b).
"""

import spack
import spack.main
import spack.spec
import spack.solver.asp as asp
import spack.store
import llnl.util.lang as lang
import llnl.util.tty.color as clr
import llnl.util.tty as tty


class SpecDiff:
    """
    A SpecDiff calculates a diff of two specs.

    The user should provide both specs on init, and then is able to look
    at the diff via facts (e.g., intersecting and difference sets) or to
    dump as json, or to print as a diff string (a single colored line)
    or an entire tree.
    """
    # Assume we look for all attributes of the default format string
    # This is also in the correct order. See spack.spec default_format
    attrs = ['name', 'version', 'compiler.name', 'compiler.version',
             'compiler_flags', 'variants', 'architecture']

    # Prefixes depend on variable name
    prefixes = {'version': "@", "compiler.name": '%',
                'compiler.version': '@', 'architecture': ' arch='}

    def __init__(self, a, b, fmt=None):
        """Compare an old spec (a) against a new spec (b).

        We honor the direction of the diff, so a TO b (with a as the first
        argument) says "Show me differences from the old a TO the new b.
        """
        # Load each spec into the class
        self.a = self._load_spec(a)
        self.b = self._load_spec(b)

        # Prepare facts for each spec
        setup = asp.SpackSolverSetup()

        # Format the spec names to be colored
        self.fmt = fmt or "{name}{@version}{/hash:7}"

        self.a_facts = set(to_tuple(t) for t in setup.spec_clauses(self.a))
        self.b_facts = set(to_tuple(t) for t in setup.spec_clauses(self.b))

    @property
    def a_name(self):
        return self.a.format(self.fmt, color=clr.get_color_when())

    @property
    def b_name(self):
        return self.b.format(self.fmt, color=clr.get_color_when())

    def __str__(self):
        return "[spec-diff: %s TO %s]" % (self.a_name, self.b_name)

    def _load_spec(self, spec):
        """
        Load a spec, whether it's a string or already correct.

        The user can either provide a string, or a spec object itself.
        If we find anything else, we exit with error.
        """
        # Load the specs if it's a provided string
        if isinstance(spec, str):
            spec = spack.spec.Spec(spec)

        # Not allowed to provide anything else
        if not isinstance(spec, spack.spec.Spec):
            tty.fail("%s is not a spack.Spec." % spec)

        return spec.concretized()

    @property
    def intersect(self):
        """
        Given two loaded specs, return the intersecting facts.
        """
        # We want to present them to the user as simple key: values
        return list(self.a_facts.intersection(self.b_facts))

    @property
    def a_not_b(self):
        """Return list of facts in a but not b
        """
        return list(self.a_facts.difference(self.b_facts))

    @property
    def b_not_a(self):
        """Return list of facts in a but not b
        """
        return list(self.b_facts.difference(self.a_facts))

    def to_json(self, to_str=False, colorful=True):
        """
        Dump a json comparison, including diffs and an intersection.

        This generates a json object for the user to save, either with "terminal
        pretty" output (not colorful) or not. We return an object that shows the
        differences, intersection, and names for a pair of specs a and b.

        Arguments:
            to_str (bool): return an object that can be json dumped
            colorful (bool): do not format the names for the console
        """
        # We want to show what is the same, and then difference for each
        return {
            "intersect": flatten(self.intersect) if to_str else self.intersect,
            "a_not_b": flatten(self.a_not_b) if to_str else self.a_not_b,
            "b_not_a": flatten(self.b_not_a) if to_str else self.b_not_a,
            "a_name": self.a_name if colorful else self.a.format(self.fmt),
            "b_name": self.b_name if colorful else self.b.format(self.fmt)
        }

    def colored_diff(self, spec1=None, spec2=None):
        """A colored diff is a single line to print to show differences.

        By default, we assume the user wants a for spec1, b for spec2.
        However we can also accept custom specs, in the case of needing them
        to build a diff tree.
        """
        spec1 = spec1 or self.a
        spec2 = spec2 or self.b

        atts1 = spec1.format(return_lookup=True)
        atts2 = spec2.format(return_lookup=True)

        # Our final string to print
        final = ""

        # Loop through attributes (changes from one to the next) and prepare
        # string that shows second as newer, first as older
        for attr in self.attrs:
            att1 = atts1.get(attr)
            att2 = atts2.get(attr)

            # Printing prefix
            prefix = "" if attr not in self.prefixes else self.prefixes[attr]

            # Case 1: it's in neither
            if not att1 and not att2:
                continue

            # Case 2: it's missing entirely in our first, this is new (GREEN)
            elif not att1 and att2:
                final += clr.colorize("@G{%s%s}" % (prefix, att2))

            # Case 3: it's missing entirely in our second, not present first (RED)
            elif not att2 and att1:
                final += clr.colorize("@-R{%s%s}" % (prefix, att1))

            # Case 4: both are defined and equal (keep as regular color)
            elif att1 == att2:
                final += "%s%s" % (prefix, att1)

            # Case 5: both are defined and different
            elif att1 != att2:
                # TODO: we could do another level of comparison here
                final += clr.colorize("@-R{%s%s}@G{%s}" % (prefix, att1, att2))

        return final

    def colored_spec(self, spec, fmt="@G"):
        """Color a single spec to be entirely missing or present (red, green).

        By default, the format string we use (@G) is bright green to indicate
        present. Change to (@-R) to indicate missing (red strikethrough).
        If you need to compare two specs (with different colors) you should
        use the colored_diff function instead.
        """
        atts = spec.format(return_lookup=True)

        # Our final string to print
        final = ""

        for attr in self.attrs:
            att = atts.get(attr)

            # Printing prefix
            prefix = "" if attr not in self.prefixes else self.prefixes[attr]

            # Attribute is not present in the spec
            if not att:
                continue

            final += clr.colorize("%s{%s%s}" % (fmt, prefix, att))

        return final

    def _get_edges(self, spec):
        """Given a spec, traverse it's dependency edges.

        We return a lookup of specs, and depth in the graph.
        """
        lookup = {}
        a_edges = spec.traverse_edges(order='pre', cover="nodes", depth=True,
                                      deptypes="all")
        for depth, edge in a_edges:
            lookup[edge.spec.name] = {"edge": edge, "depth": depth}
        return lookup

    def tree(self, **kwargs):
        """
        Print out the spec diff as a tree, which includes dependencies.

        This is a modified verison of spec.tree().
        """
        indent = kwargs.pop('indent', 0)
        lang.check_kwargs(kwargs, self.tree)

        # For each of a and b, get edges and depths
        a_edges = self._get_edges(self.a)
        b_edges = self._get_edges(self.b)

        # output
        out = ""

        def print_spacing(out, depth):
            """shared function to print spacing
            """
            out += " " * indent
            out += ("    " * depth)
            if depth > 0:
                out += "^"
            return out

        # We are going to show differences from a TO b (b is newer)
        for name, meta in b_edges.items():
            node = meta['edge'].spec
            out = print_spacing(out, meta['depth'])

            # If we have the spec in the second, generate the colored output
            if node.name in a_edges:
                anode = a_edges[node.name]['edge'].spec
                out += self.colored_diff(spec1=node, spec2=anode) + "\n"

            # If we don't have the spec in the second, it's all new (green)
            else:
                out += self.colored_spec(node, fmt="@G") + "\n"

        # Finally, we need to add the specs in b not in a
        for name, meta in a_edges.items():
            node = meta['edge'].spec

            # Don't print what we've already seen
            if node.name in b_edges:
                continue

            # Print in red
            out = print_spacing(out, meta['depth'])
            out += self.colored_spec(node, fmt="@-R") + "\n"

        return out


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
