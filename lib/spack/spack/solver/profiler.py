# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Profiling propagator for clingo solves."""

import re
from typing import Any, Dict, List

import llnl.util.tty as tty


class Data:
    """Counters for propagations and undos of an atom."""

    __slots__ = ["atom", "literal", "prop", "undo"]

    # currently we use Any for clingo types because clingo has a bunch of import
    # wrappers around it that make typing difficult (see spack.solver.core for details)
    def __init__(self, atom: Any, literal: int, prop: int, undo: int):
        self.atom = atom
        self.literal = literal
        self.prop = prop
        self.undo = undo


class AggregatedData:
    """Aggregated data for a profile, constructed from ``Data``.

    We coarsen from atom granularity to string keys when aggregating.
    """

    __slots__ = ["name", "prop", "undo"]

    def __init__(self, name: str, prop: int, undo: int):
        self.name = name
        self.prop = prop
        self.undo = undo


class ProfilePropagator:
    """Profiling propagator for `spack solve --profile`.

    Register this with the ``clingo.Control`` object to profile a solve.
    """

    _literal_to_atom: Dict
    _profile: Dict[int, Data]

    def init(self, init) -> None:
        self._literal_to_atom = {}
        self._profile = {}
        for atom in init.symbolic_atoms:
            solver_literal = init.solver_literal(atom.literal)
            self._profile[solver_literal] = Data(atom, solver_literal, 0, 0)
            init.add_watch(solver_literal)

    def propagate(self, ctl, changes: List[int]) -> bool:
        """Record a propagation in the solve."""
        for literal in changes:
            data = self._profile[literal]
            data.prop += 1
        return True

    def undo(self, solver_id: int, assign, undo: List[int]) -> None:
        """Record an undo in the solve."""
        for literal in undo:
            data = self._profile[literal]
            data.undo += 1

    def color_sym(self, string: str) -> str:
        """Colorize a symbol for profile output"""
        string = re.sub(r"^(\w+)", r"@C{\1}", string)
        string = re.sub(r'("[^"]*")', r"@G{\1}", string)
        string = re.sub(r"([\(\)])", r"@b{\1}", string)
        return tty.color.colorize(string)

    def key(self, atom) -> str:
        """Convert an atom into an aggregate key for our profile.

        Currently this compresses most things to their function name, and expands
        ``attr("name", ...)`` to ``attr("name")`` so we can see which attributes affect
        the solve most.

        """
        sym = atom.symbol
        return f"attr({sym.arguments[0]})" if sym.name == "attr" else sym.name

    def print_profile(self, n_atoms: int) -> None:
        """Aggregate and print nicely formatted profile data."""
        aggregated = {}
        for data in self._profile.values():
            name = self.key(data.atom)
            if name not in aggregated:
                aggregated[name] = AggregatedData(name, data.prop, data.undo)
            else:
                agg = aggregated[name]
                agg.prop += data.prop
                agg.undo += data.undo

        values = sorted(
            (x for x in aggregated.values() if x.prop), key=lambda x: x.prop, reverse=True
        )

        # format the output nicely
        w = 10  # width for number fields
        print(tty.color.colorize(f"  @*{{{'Prop':<{w}}{'Undo':<{w}}{'Symbol'}}}"))
        for a in values[:n_atoms]:
            print(f"  {a.prop:<{w}}{a.undo:<{w}}{self.color_sym(a.name)}")
        if len(values) > n_atoms:
            print("  ...")
