# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import enum
from typing import List, NamedTuple, Optional, Sequence

from llnl.util import tty

import spack.config
import spack.error
import spack.package_base
import spack.spec
from spack.config import get_mark_from_yaml_data


class RequirementKind(enum.Enum):
    """Purpose / provenance of a requirement"""

    #: Default requirement expressed under the 'all' attribute of packages.yaml
    DEFAULT = enum.auto()
    #: Requirement expressed on a virtual package
    VIRTUAL = enum.auto()
    #: Requirement expressed on a specific package
    PACKAGE = enum.auto()


class RequirementRule(NamedTuple):
    """Data class to collect information on a requirement"""

    pkg_name: str
    policy: str
    requirements: Sequence[spack.spec.Spec]
    condition: spack.spec.Spec
    kind: RequirementKind
    message: Optional[str]


class RequirementParser:
    """Parses requirements from package.py files and configuration, and returns rules."""

    def __init__(self, configuration: spack.config.Configuration):
        self.config = configuration

    def rules(self, pkg: spack.package_base.PackageBase) -> List[RequirementRule]:
        result = []
        result.extend(self.rules_from_package_py(pkg))
        result.extend(self.rules_from_require(pkg))
        result.extend(self.rules_from_prefer(pkg))
        result.extend(self.rules_from_conflict(pkg))
        return result

    def rules_from_package_py(self, pkg: spack.package_base.PackageBase) -> List[RequirementRule]:
        rules = []
        for when_spec, requirement_list in pkg.requirements.items():
            for requirements, policy, message in requirement_list:
                rules.append(
                    RequirementRule(
                        pkg_name=pkg.name,
                        policy=policy,
                        requirements=requirements,
                        kind=RequirementKind.PACKAGE,
                        condition=when_spec,
                        message=message,
                    )
                )
        return rules

    def rules_from_virtual(self, virtual_str: str) -> List[RequirementRule]:
        requirements = self.config.get("packages", {}).get(virtual_str, {}).get("require", [])
        return self._rules_from_requirements(
            virtual_str, requirements, kind=RequirementKind.VIRTUAL
        )

    def rules_from_require(self, pkg: spack.package_base.PackageBase) -> List[RequirementRule]:
        kind, requirements = self._raw_yaml_data(pkg, section="require")
        return self._rules_from_requirements(pkg.name, requirements, kind=kind)

    def rules_from_prefer(self, pkg: spack.package_base.PackageBase) -> List[RequirementRule]:
        result = []
        kind, preferences = self._raw_yaml_data(pkg, section="prefer")
        for item in preferences:
            spec, condition, message = self._parse_prefer_conflict_item(item)
            result.append(
                # A strong preference is defined as:
                #
                # require:
                # - any_of: [spec_str, "@:"]
                RequirementRule(
                    pkg_name=pkg.name,
                    policy="any_of",
                    requirements=[spec, spack.spec.Spec("@:")],
                    kind=kind,
                    message=message,
                    condition=condition,
                )
            )
        return result

    def rules_from_conflict(self, pkg: spack.package_base.PackageBase) -> List[RequirementRule]:
        result = []
        kind, conflicts = self._raw_yaml_data(pkg, section="conflict")
        for item in conflicts:
            spec, condition, message = self._parse_prefer_conflict_item(item)
            result.append(
                # A conflict is defined as:
                #
                # require:
                # - one_of: [spec_str, "@:"]
                RequirementRule(
                    pkg_name=pkg.name,
                    policy="one_of",
                    requirements=[spec, spack.spec.Spec("@:")],
                    kind=kind,
                    message=message,
                    condition=condition,
                )
            )
        return result

    def _parse_prefer_conflict_item(self, item):
        # The item is either a string or an object with at least a "spec" attribute
        if isinstance(item, str):
            spec = parse_spec_from_yaml_string(item)
            condition = spack.spec.Spec()
            message = None
        else:
            spec = parse_spec_from_yaml_string(item["spec"])
            condition = spack.spec.Spec(item.get("when"))
            message = item.get("message")
        return spec, condition, message

    def _raw_yaml_data(self, pkg: spack.package_base.PackageBase, *, section: str):
        config = self.config.get("packages")
        data = config.get(pkg.name, {}).get(section, [])
        kind = RequirementKind.PACKAGE
        if not data:
            data = config.get("all", {}).get(section, [])
            kind = RequirementKind.DEFAULT
        return kind, data

    def _rules_from_requirements(
        self, pkg_name: str, requirements, *, kind: RequirementKind
    ) -> List[RequirementRule]:
        """Manipulate requirements from packages.yaml, and return a list of tuples
        with a uniform structure (name, policy, requirements).
        """
        if isinstance(requirements, str):
            requirements = [requirements]

        rules = []
        for requirement in requirements:
            # A string is equivalent to a one_of group with a single element
            if isinstance(requirement, str):
                requirement = {"one_of": [requirement]}

            for policy in ("spec", "one_of", "any_of"):
                if policy not in requirement:
                    continue

                constraints = requirement[policy]
                # "spec" is for specifying a single spec
                if policy == "spec":
                    constraints = [constraints]
                    policy = "one_of"

                # validate specs from YAML first, and fail with line numbers if parsing fails.
                constraints = [
                    parse_spec_from_yaml_string(constraint) for constraint in constraints
                ]
                when_str = requirement.get("when")
                when = parse_spec_from_yaml_string(when_str) if when_str else spack.spec.Spec()

                constraints = [
                    x
                    for x in constraints
                    if not self.reject_requirement_constraint(pkg_name, constraint=x, kind=kind)
                ]
                if not constraints:
                    continue

                rules.append(
                    RequirementRule(
                        pkg_name=pkg_name,
                        policy=policy,
                        requirements=constraints,
                        kind=kind,
                        message=requirement.get("message"),
                        condition=when,
                    )
                )
        return rules

    def reject_requirement_constraint(
        self, pkg_name: str, *, constraint: spack.spec.Spec, kind: RequirementKind
    ) -> bool:
        """Returns True if a requirement constraint should be rejected"""
        if kind == RequirementKind.DEFAULT:
            # Requirements under all: are applied only if they are satisfiable considering only
            # package rules, so e.g. variants must exist etc. Otherwise, they are rejected.
            try:
                s = spack.spec.Spec(pkg_name)
                s.constrain(constraint)
                s.validate_or_raise()
            except spack.error.SpackError as e:
                tty.debug(
                    f"[SETUP] Rejecting the default '{constraint}' requirement "
                    f"on '{pkg_name}': {str(e)}",
                    level=2,
                )
                return True
        return False


def parse_spec_from_yaml_string(string: str) -> spack.spec.Spec:
    """Parse a spec from YAML and add file/line info to errors, if it's available.

    Parse a ``Spec`` from the supplied string, but also intercept any syntax errors and
    add file/line information for debugging using file/line annotations from the string.

    Arguments:
        string: a string representing a ``Spec`` from config YAML.

    """
    try:
        return spack.spec.Spec(string)
    except spack.error.SpecSyntaxError as e:
        mark = get_mark_from_yaml_data(string)
        if mark:
            msg = f"{mark.name}:{mark.line + 1}: {str(e)}"
            raise spack.error.SpecSyntaxError(msg) from e
        raise e
