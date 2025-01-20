# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import spack.binary_distribution
import spack.environment
import spack.error
import spack.spec
import spack.store

from .enums import InstallRecordStatus


def _lookup_hash(spec: spack.spec.Spec):
    """Lookup just one spec with an abstract hash, returning a spec from the the environment,
    store, or finally, binary caches."""

    active_env = spack.environment.active_environment()

    # First env, then store, then binary cache
    matches = (
        (active_env.all_matching_specs(spec) if active_env else [])
        or spack.store.STORE.db.query(spec, installed=InstallRecordStatus.ANY)
        or spack.binary_distribution.BinaryCacheQuery(True)(spec)
    )

    if not matches:
        raise spack.error.InvalidHashError(spec, spec.abstract_hash)

    if len(matches) != 1:
        raise AmbiguousHashError(
            f"Multiple packages specify hash beginning '{spec.abstract_hash}'.", *matches
        )

    return matches[0]


def lookup_hash(spec: spack.spec.Spec) -> spack.spec.Spec:
    """Given a spec with an abstract hash, return a copy of the spec with all properties and
    dependencies by looking up the hash in the environment, store, or finally, binary caches.
    This is non-destructive."""
    if spec.concrete or not any(node.abstract_hash for node in spec.traverse()):
        return spec

    spec = spec.copy(deps=False)
    # root spec is replaced
    if spec.abstract_hash:
        spec._dup(_lookup_hash(spec))
        return spec

    # Get dependencies that need to be replaced
    for node in spec.traverse(root=False):
        if node.abstract_hash:
            spec._add_dependency(_lookup_hash(node), depflag=0, virtuals=())

    # reattach nodes that were not otherwise satisfied by new dependencies
    for node in spec.traverse(root=False):
        if not any(n.satisfies(node) for n in spec.traverse()):
            spec._add_dependency(node.copy(), depflag=0, virtuals=())

    return spec


def replace_hash(spec: spack.spec.Spec) -> None:
    """Given a spec with an abstract hash, attempt to populate all properties and dependencies
    by looking up the hash in the environment, store, or finally, binary caches.
    This is destructive."""

    if not any(node for node in spec.traverse(order="post") if node.abstract_hash):
        return

    spec._dup(lookup_hash(spec))


class AmbiguousHashError(spack.error.SpecError):
    def __init__(self, msg, *specs):
        spec_fmt = "{namespace}.{name}{@version}{%compiler}{compiler_flags}"
        spec_fmt += "{variants}{ arch=architecture}{/hash:7}"
        specs_str = "\n  " + "\n  ".join(spec.format(spec_fmt) for spec in specs)
        super().__init__(msg + specs_str)
