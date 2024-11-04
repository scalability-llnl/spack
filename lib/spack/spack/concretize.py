# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""
(DEPRECATED) Used to contain the code for the original concretizer
"""
import sys
import time
from contextlib import contextmanager
from itertools import chain
from typing import Tuple

import llnl.util.tty as tty

import spack.config
import spack.error
from spack.spec import Spec

CHECK_COMPILER_EXISTENCE = True


@contextmanager
def disable_compiler_existence_check():
    global CHECK_COMPILER_EXISTENCE
    CHECK_COMPILER_EXISTENCE, saved = False, CHECK_COMPILER_EXISTENCE
    yield
    CHECK_COMPILER_EXISTENCE = saved


@contextmanager
def enable_compiler_existence_check():
    global CHECK_COMPILER_EXISTENCE
    CHECK_COMPILER_EXISTENCE, saved = True, CHECK_COMPILER_EXISTENCE
    yield
    CHECK_COMPILER_EXISTENCE = saved


def find_spec(spec, condition, default=None):
    """Searches the dag from spec in an intelligent order and looks
    for a spec that matches a condition"""
    # First search parents, then search children
    deptype = ("build", "link")
    dagiter = chain(
        spec.traverse(direction="parents", deptype=deptype, root=False),
        spec.traverse(direction="children", deptype=deptype, root=False),
    )
    visited = set()
    for relative in dagiter:
        if condition(relative):
            return relative
        visited.add(id(relative))

    # Then search all other relatives in the DAG *except* spec
    for relative in spec.root.traverse(deptype="all"):
        if relative is spec:
            continue
        if id(relative) in visited:
            continue
        if condition(relative):
            return relative

    # Finally search spec itself.
    if condition(spec):
        return spec

    return default  # Nothing matched the condition; return default.


def concretize_specs_together(*abstract_specs, **kwargs):
    """Given a number of specs as input, tries to concretize them together.

    Args:
        tests (bool or list or set): False to run no tests, True to test
            all packages, or a list of package names to run tests for some
        *abstract_specs: abstract specs to be concretized, given either
            as Specs or strings

    Returns:
        List of concretized specs
    """
    import spack.solver.asp

    allow_deprecated = spack.config.get("config:deprecated", False)
    solver = spack.solver.asp.Solver()
    result = solver.solve(
        abstract_specs, tests=kwargs.get("tests", False), allow_deprecated=allow_deprecated
    )
    return [s.copy() for s in result.specs]


def concretize_together(*spec_list, **kwargs):
    """Given a number of specs as input, tries to concretize them together.

    Args:
        tests (bool or list or set): False to run no tests, True to test
            all packages, or a list of package names to run tests for some
        *spec_list: list of tuples to concretize. First entry is abstract spec, second entry is
            already concrete spec or None if not yet concretized

    Returns:
        List of tuples of abstract and concretized specs
    """
    to_concretize = [concrete if concrete else abstract for abstract, concrete in spec_list]
    abstract_specs = [abstract for abstract, _ in spec_list]
    concrete_specs = concretize_specs_together(*to_concretize, **kwargs)
    return list(zip(abstract_specs, concrete_specs))


def concretize_together_when_possible(*spec_list, **kwargs):
    """Given a number of specs as input, tries to concretize them together to the extent possible.

    See documentation for ``unify: when_possible`` concretization for the precise definition of
    "to the extent possible".

    Args:
        tests (bool or list or set): False to run no tests, True to test
            all packages, or a list of package names to run tests for some
        *spec_list: list of tuples to concretize. First entry is abstract spec, second entry is
            already concrete spec or None if not yet concretized

    Returns:
        List of tuples of abstract and concretized specs
    """
    to_concretize = [concrete if concrete else abstract for abstract, concrete in spec_list]
    old_concrete_to_abstract = {
        concrete: abstract for (abstract, concrete) in spec_list if concrete
    }

    result_by_user_spec = {}
    solver = spack.solver.asp.Solver()
    allow_deprecated = spack.config.get("config:deprecated", False)
    for result in solver.solve_in_rounds(
        to_concretize, tests=kwargs.get("tests", False), allow_deprecated=allow_deprecated
    ):
        result_by_user_spec.update(result.specs_by_input)

    # If the "abstract" spec is a concrete spec from the previous concretization
    # translate it back to an abstract spec. Otherwise, keep the abstract spec
    return [
        (old_concrete_to_abstract.get(abstract, abstract), concrete)
        for abstract, concrete in sorted(result_by_user_spec.items())
    ]


def concretize_separately(*spec_list, **kwargs):
    """Given a number of specs as input, tries to concretize them together.

    Args:
        tests (bool or list or set): False to run no tests, True to test
            all packages, or a list of package names to run tests for some
        *spec_list: list of tuples to concretize. First entry is abstract spec, second entry is
            already concrete spec or None if not yet concretized

    Returns:
        List of tuples of abstract and concretized specs
    """
    tests = kwargs.get("tests", False)
    to_concretize = [abstract for abstract, concrete in spec_list if not concrete]
    args = [
        (i, str(abstract), tests)
        for i, abstract in enumerate(to_concretize)
        if not abstract.concrete
    ]
    ret = [(i, abstract) for i, abstract in enumerate(to_concretize) if abstract.concrete]
    # Ensure we don't try to bootstrap clingo in parallel
    with spack.bootstrap.ensure_bootstrap_configuration():
        spack.bootstrap.ensure_clingo_importable_or_raise()

    # Ensure all the indexes have been built or updated, since
    # otherwise the processes in the pool may timeout on waiting
    # for a write lock. We do this indirectly by retrieving the
    # provider index, which should in turn trigger the update of
    # all the indexes if there's any need for that.
    _ = spack.repo.PATH.provider_index

    # Ensure we have compilers in compilers.yaml to avoid that
    # processes try to write the config file in parallel
    _ = spack.compilers.all_compilers_config(spack.config.CONFIG)

    # Early return if there is nothing to do
    if len(args) == 0:
        # Still have to combine the things that were passed in as abstract with the things
        # that were passed in as pairs
        return [(abstract, concrete) for abstract, (_, concrete) in zip(to_concretize, ret)] + [
            (abstract, concrete) for abstract, concrete in spec_list if concrete
        ]

    # Solve the environment in parallel on Linux
    # TODO: support parallel concretization on macOS and Windows
    num_procs = min(len(args), spack.config.determine_number_of_jobs(parallel=True))

    for j, (i, concrete, duration) in enumerate(
        spack.util.parallel.imap_unordered(
            spack.concretize._concretize_task,
            args,
            processes=num_procs,
            debug=tty.is_debug(),
            maxtaskperchild=1,
        )
    ):
        ret.append((i, concrete))
        percentage = (j + 1) / len(args) * 100
        tty.verbose(
            f"{duration:6.1f}s [{percentage:3.0f}%] {concrete.cformat('{hash:7}')} "
            f"{to_concretize[i].colored_str}"
        )
        sys.stdout.flush()

    # Add specs in original order
    ret.sort(key=lambda x: x[0])

    return [(abstract, concrete) for abstract, (_, concrete) in zip(to_concretize, ret)] + [
        (abstract, concrete) for abstract, concrete in spec_list if concrete
    ]


def _concretize_task(packed_arguments) -> Tuple[int, Spec, float]:
    index, spec_str, tests = packed_arguments
    with tty.SuppressOutput(msg_enabled=False):
        start = time.time()
        spec = Spec(spec_str).concretized(tests=tests)
        return index, spec, time.time() - start


class UnavailableCompilerVersionError(spack.error.SpackError):
    """Raised when there is no available compiler that satisfies a
    compiler spec."""

    def __init__(self, compiler_spec, arch=None):
        err_msg = "No compilers with spec {0} found".format(compiler_spec)
        if arch:
            err_msg += " for operating system {0} and target {1}.".format(arch.os, arch.target)

        super().__init__(
            err_msg,
            "Run 'spack compiler find' to add compilers or "
            "'spack compilers' to see which compilers are already recognized"
            " by spack.",
        )
