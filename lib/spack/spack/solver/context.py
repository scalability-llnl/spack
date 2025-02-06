# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import List, NamedTuple, Set, Tuple

import archspec.cpu

from llnl.util import lang, tty

import spack.binary_distribution
import spack.config
import spack.platforms
import spack.repo
import spack.spec
import spack.store
from spack.error import SpackError

RUNTIME_TAG = "runtime"


class Context(NamedTuple):
    configuration: spack.config.Configuration
    repo: spack.repo.RepoPath
    store: spack.store.Store
    binary_index: spack.binary_distribution.BinaryCacheIndex


class ContextAnalyzer:
    """Analyze a Context, to provide information that is useful when setting up concretization"""

    def __init__(self, *, context: Context):
        self.context = context
        # Set aliases for convenience
        self.configuration = context.configuration
        self.repo = context.repo
        self.store = context.store

    @lang.memoized
    def buildcache_specs(self) -> List[spack.spec.Spec]:
        self.context.binary_index.update()
        return self.context.binary_index.get_all_built_specs()

    def runtime_pkgs(self) -> Tuple[Set[str], Set[str]]:
        """Returns the runtime packages for this context, and the virtuals they may provide"""
        runtime_pkgs = set(self.repo.packages_with_tags(RUNTIME_TAG))
        runtime_virtuals = set()
        for x in runtime_pkgs:
            pkg_class = self.repo.get_pkg_class(x)
            runtime_virtuals.update(pkg_class.provided_virtual_names())
        return runtime_pkgs, runtime_virtuals

    def is_virtual(self, name: str) -> bool:
        return self.repo.is_virtual(name)

    @lang.memoized
    def libc_pkgs(self) -> List[str]:
        try:
            return [x.name for x in self.providers_for("libc")]
        except spack.repo.UnknownPackageError:
            return []

    @lang.memoized
    def providers_for(self, virtual_str: str) -> List[spack.spec.Spec]:
        candidates = self.repo.providers_for(virtual_str)
        result = []
        for spec in candidates:
            if not self._is_provider_candidate(pkg_name=spec.name, virtual=virtual_str):
                continue
            result.append(spec)
        return result

    @lang.memoized
    def is_allowed_on_this_platform(self, *, pkg_name: str) -> bool:
        # Check the package recipe
        pkg_cls = self.repo.get_pkg_class(pkg_name)
        platform_condition = (
            f"platform={spack.platforms.host()} target={archspec.cpu.host().family}:"
        )
        for when_spec, conditions in pkg_cls.requirements.items():
            if not when_spec.intersects(platform_condition):
                continue
            for requirements, _, _ in conditions:
                if not any(x.intersects(platform_condition) for x in requirements):
                    tty.debug(f"[{__name__}] {pkg_name} is not for this platform")
                    return False
        return True

    @lang.memoized
    def can_be_installed(self, *, pkg_name) -> bool:
        if self.configuration.get(f"packages:{pkg_name}:buildable", True):
            return True

        if self.configuration.get(f"packages:{pkg_name}:externals", []):
            return True

        reuse = self.configuration.get("concretizer:reuse")
        if reuse is not False and self.store.db.query(pkg_name):
            return True

        if reuse is not False and any(x.name == pkg_name for x in self.buildcache_specs()):
            return True

        tty.debug(f"[{__name__}] {pkg_name} cannot be installed")
        return False

    @lang.memoized
    def _is_provider_candidate(self, *, pkg_name: str, virtual: str) -> bool:
        if self.configuration.get("concretizer:preferred_providers_only", False):
            virtual_spec = spack.spec.Spec(virtual)
            preferred_providers = self.configuration.get(
                f"packages:all:providers:{virtual_spec.name}"
            )
            preferred_providers = [spack.spec.Spec(x) for x in preferred_providers]
            if not any(x.intersects(pkg_name) for x in preferred_providers):
                tty.debug(f"[{__name__}] {pkg_name} is not among preferred {virtual} providers")
                return False

        if not self.is_allowed_on_this_platform(pkg_name=pkg_name):
            return False

        if not self.can_be_installed(pkg_name=pkg_name):
            return False

        return True

    @lang.memoized
    def unreachable(self, *, pkg_name: str, when_spec: spack.spec.Spec) -> bool:
        """Returns true if the context can determine that the condition cannot ever
        be met on pkg_name.
        """
        # TODO: extend to more complex requirements
        candidates = self.configuration.get(f"packages:{pkg_name}:require", [])
        if not candidates:
            return self._default_unreachable(when_spec=when_spec)

        if isinstance(candidates, str):
            candidates = [candidates]

        union_requirement = spack.spec.Spec()
        for c in candidates:
            if not isinstance(c, str):
                continue
            try:
                union_requirement.constrain(c)
            except SpackError:
                # Less optimized, but shouldn't fail
                pass

        if not union_requirement.intersects(when_spec):
            return True

        return False

    @lang.memoized
    def _default_unreachable(self, *, when_spec: spack.spec.Spec) -> bool:
        # TODO: extend to more complex requirements
        candidates = self.configuration.get("packages:all:require", [])
        if not candidates:
            return False

        if isinstance(candidates, str):
            candidates = [candidates]

        union_requirement = spack.spec.Spec()
        for c in candidates:
            if not isinstance(c, str):
                continue
            try:
                union_requirement.constrain(c)
            except SpackError:
                # Less optimized, but shouldn't fail
                pass

        if not union_requirement.intersects(when_spec):
            return True

        return False

    def candidate_targets(self) -> List[archspec.cpu.Microarchitecture]:
        """Returns a list of targets that are candidate for concretization"""
        platform = spack.platforms.host()
        default_target = archspec.cpu.TARGETS[platform.default]

        # Construct the list of targets which are compatible with the host
        candidate_targets = [default_target] + default_target.ancestors
        granularity = self.configuration.get("concretizer:targets:granularity")
        host_compatible = self.configuration.get("concretizer:targets:host_compatible")

        # Add targets which are not compatible with the current host
        if not host_compatible:
            additional_targets_in_family = sorted(
                [
                    t
                    for t in archspec.cpu.TARGETS.values()
                    if (t.family.name == default_target.family.name and t not in candidate_targets)
                ],
                key=lambda x: len(x.ancestors),
                reverse=True,
            )
            candidate_targets += additional_targets_in_family

        # Check if we want only generic architecture
        if granularity == "generic":
            candidate_targets = [t for t in candidate_targets if t.vendor == "generic"]

        return candidate_targets
