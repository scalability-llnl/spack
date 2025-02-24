# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from functools import cmp_to_key
from typing import Dict, List, NamedTuple

import spack.deptypes as dt
from spack.spec import Spec
from spack.traverse import by_dag_hash, traverse_nodes


class Splice(NamedTuple):
    #: The spec being spliced into a parent
    splice_spec: Spec
    #: The name of the child that splice spec is replacing
    child_name: str
    #: The hash of the child that `splice_spec` is replacing
    child_hash: str


def _resolve_collected_splices(
    specs: List[Spec], splices: Dict[Spec, List[Splice]]
) -> Dict[Spec, Spec]:
    """After all of the specs have been concretized, apply all immediate splices.
    Returns a dict mapping original specs to their resolved counterparts
    """

    def splice_cmp(s1: Spec, s2: Spec):
        """This function can be used to sort a list of specs such that that any
        spec which will be spliced into a parent comes after the parent it will
        be spliced into. This order ensures that transitive splices will be
        executed in the correct order.
        """

        s1_splices = splices.get(s1, [])
        s2_splices = splices.get(s2, [])
        if any([s2.dag_hash() == splice.splice_spec.dag_hash() for splice in s1_splices]):
            return -1
        elif any([s1.dag_hash() == splice.splice_spec.dag_hash() for splice in s2_splices]):
            return 1
        else:
            return 0

    splice_order = sorted(specs, key=cmp_to_key(splice_cmp))
    reverse_topo_order = reversed(
        [x for x in traverse_nodes(splice_order, order="topo", key=by_dag_hash) if x in specs]
    )

    already_resolved: Dict[Spec, Spec] = {}
    for spec in reverse_topo_order:
        immediate = splices.get(spec, [])
        if not immediate and not any(
            edge.spec in already_resolved for edge in spec.edges_to_dependencies()
        ):
            continue
        new_spec = spec.copy(deps=False)
        new_spec.clear_caches(ignore=("package_hash",))
        new_spec.build_spec = spec
        for edge in spec.edges_to_dependencies():
            depflag = edge.depflag & ~dt.BUILD
            if any(edge.spec.dag_hash() == splice.child_hash for splice in immediate):
                splice = [s for s in immediate if s.child_hash == edge.spec.dag_hash()][0]
                # If the spec being splice in is also spliced
                splice_spec = already_resolved.get(splice.splice_spec, splice.splice_spec)
                new_spec.add_dependency_edge(splice_spec, depflag=depflag, virtuals=edge.virtuals)
            elif edge.spec in already_resolved:
                new_spec.add_dependency_edge(
                    already_resolved[edge.spec], depflag=depflag, virtuals=edge.virtuals
                )
            else:
                new_spec.add_dependency_edge(edge.spec, depflag=depflag, virtuals=edge.virtuals)
        already_resolved[spec] = new_spec
    return already_resolved
