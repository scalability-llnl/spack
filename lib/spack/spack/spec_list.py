# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import itertools
from typing import List

import spack.spec
import spack.variant
from spack.error import SpackError
from spack.spec import Spec


class SpecList:
    def __init__(self, name="specs", yaml_list=None, reference=None):
        # Normalize input arguments
        yaml_list = yaml_list or []
        reference = reference or {}

        self.name = name
        self._reference = reference  # TODO: Do we need defensive copy here?

        # Validate yaml_list before assigning
        if not all(isinstance(s, str) or isinstance(s, (list, dict)) for s in yaml_list):
            raise ValueError(
                "yaml_list can contain only valid YAML types!  Found:\n  %s"
                % [type(s) for s in yaml_list]
            )
        self.yaml_list = yaml_list[:]

        # Expansions can be expensive to compute and difficult to keep updated
        # We cache results and invalidate when self.yaml_list changes
        self._expanded_list = None
        self._constraints = None
        self._specs = None

    @property
    def is_matrix(self):
        for item in self.specs_as_yaml_list:
            if isinstance(item, dict):
                return True
        return False

    @property
    def specs_as_yaml_list(self):
        if self._expanded_list is None:
            self._expanded_list = self._expand_references(self.yaml_list)
        return self._expanded_list

    @property
    def specs_as_constraints(self):
        if self._constraints is None:
            constraints = []
            for item in self.specs_as_yaml_list:
                if isinstance(item, dict):  # matrix of specs
                    constraints.extend(_expand_matrix_constraints(item))
                else:  # individual spec
                    constraints.append([Spec(item)])
            self._constraints = constraints

        return self._constraints

    @property
    def specs(self) -> List[Spec]:
        if self._specs is None:
            specs = []
            # This could be slightly faster done directly from yaml_list,
            # but this way is easier to maintain.
            for constraint_list in self.specs_as_constraints:
                spec = constraint_list[0].copy()
                for const in constraint_list[1:]:
                    spec.constrain(const)
                specs.append(spec)
            self._specs = specs

        return self._specs

    def add(self, spec):
        self.yaml_list.append(str(spec))

        # expanded list can be updated without invalidation
        if self._expanded_list is not None:
            self._expanded_list.append(str(spec))

        # Invalidate cache variables when we change the list
        self._constraints = None
        self._specs = None

    def remove(self, spec):
        # Get spec to remove from list
        remove = [
            s
            for s in self.yaml_list
            if (isinstance(s, str) and not s.startswith("$")) and Spec(s) == Spec(spec)
        ]
        if not remove:
            msg = f"Cannot remove {spec} from SpecList {self.name}.\n"
            msg += f"Either {spec} is not in {self.name} or {spec} is "
            msg += "expanded from a matrix and cannot be removed directly."
            raise SpecListError(msg)

        # Remove may contain more than one string representation of the same spec
        for item in remove:
            self.yaml_list.remove(item)

        # invalidate cache variables when we change the list
        self._expanded_list = None
        self._constraints = None
        self._specs = None

    def replace(self, idx: int, spec: str):
        """Replace the existing spec at the index with the new one.

        Args:
            idx: index of the spec to replace in the speclist
            spec: new spec
        """
        self.yaml_list[idx] = spec

        # invalidate cache variables when we change the list
        self._expanded_list = None
        self._constraints = None
        self._specs = None

    def extend(self, other, copy_reference=True):
        self.yaml_list.extend(other.yaml_list)
        self._expanded_list = None
        self._constraints = None
        self._specs = None

        if copy_reference:
            self._reference = other._reference

    def update_reference(self, reference):
        self._reference = reference
        self._expanded_list = None
        self._constraints = None
        self._specs = None

    def _parse_reference(self, name):
        sigil = ""
        name = name[1:]

        # Parse specs as constraints
        if name.startswith("^") or name.startswith("%"):
            sigil = name[0]
            name = name[1:]

        # Make sure the reference is valid
        if name not in self._reference:
            msg = f"SpecList '{self.name}' refers to named list '{name}'"
            msg += " which does not appear in its reference dict."
            raise UndefinedReferenceError(msg)

        return (name, sigil)

    def _expand_references(self, yaml):
        if isinstance(yaml, list):
            ret = []

            for item in yaml:
                # if it's a reference, expand it
                if isinstance(item, str) and item.startswith("$"):
                    # replace the reference and apply the sigil if needed
                    name, sigil = self._parse_reference(item)

                    referent = [
                        _sigilify(item, sigil) for item in self._reference[name].specs_as_yaml_list
                    ]
                    ret.extend(referent)
                else:
                    # else just recurse
                    ret.append(self._expand_references(item))
            return ret
        elif isinstance(yaml, dict):
            # There can't be expansions in dicts
            return dict((name, self._expand_references(val)) for (name, val) in yaml.items())
        else:
            # Strings are just returned
            return yaml

    def __len__(self):
        return len(self.specs)

    def __getitem__(self, key):
        return self.specs[key]

    def __iter__(self):
        return iter(self.specs)


def _expand_matrix_constraints(matrix_config):
    # recurse so we can handle nested matrices
    expanded_rows = []
    for row in matrix_config["matrix"]:
        new_row = []
        for r in row:
            if isinstance(r, dict):
                # Flatten the nested matrix into a single row of constraints
                new_row.extend(
                    [
                        [" ".join([str(c) for c in expanded_constraint_list])]
                        for expanded_constraint_list in _expand_matrix_constraints(r)
                    ]
                )
            else:
                new_row.append([r])
        expanded_rows.append(new_row)

    excludes = matrix_config.get("exclude", [])  # only compute once
    sigil = matrix_config.get("sigil", "")

    results = []
    for combo in itertools.product(*expanded_rows):
        # Construct a combined spec to test against excludes
        flat_combo = [Spec(constraint) for constraints in combo for constraint in constraints]

        test_spec = flat_combo[0].copy()
        for constraint in flat_combo[1:]:
            test_spec.constrain(constraint)

        # Abstract variants don't have normal satisfaction semantics
        # Convert all variants to concrete types.
        # This method is best effort, so all existing variants will be
        # converted before any error is raised.
        # Catch exceptions because we want to be able to operate on
        # abstract specs without needing package information
        try:
            spack.spec.substitute_abstract_variants(test_spec)
        except spack.variant.UnknownVariantError:
            pass

        # Resolve abstract hashes for exclusion criteria
        if any(test_spec.lookup_hash().satisfies(x) for x in excludes):
            continue

        if sigil:
            flat_combo[0] = Spec(sigil + str(flat_combo[0]))

        # Add to list of constraints
        results.append(flat_combo)

    return results


def _sigilify(item, sigil):
    if isinstance(item, dict):
        if sigil:
            item["sigil"] = sigil
        return item
    else:
        return sigil + item


class SpecListError(SpackError):
    """Error class for all errors related to SpecList objects."""


class UndefinedReferenceError(SpecListError):
    """Error class for undefined references in Spack stacks."""


class InvalidSpecConstraintError(SpecListError):
    """Error class for invalid spec constraints at concretize time."""
