# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import warnings
from typing import Optional

import archspec.cpu

import llnl.util.lang


@llnl.util.lang.lazy_lexicographic_ordering
class Platform:
    """Platform is an abstract class extended by subclasses.

    Platform also contain a priority class attribute. A lower number signifies higher
    priority. These numbers are arbitrarily set and can be changed though often there
    isn't much need unless a new platform is added and the user wants that to be
    detected first.
    """

    # Subclass sets number. Controls detection order
    priority: Optional[int] = None

    #: binary formats used on this platform; used by relocation logic
    binary_formats = ["elf"]

    default: str
    default_os: str

    reserved_targets = ["default_target", "frontend", "fe", "backend", "be"]
    reserved_oss = ["default_os", "frontend", "fe", "backend", "be"]
    deprecated_names = ["frontend", "fe", "backend", "be"]

    def __init__(self, name):
        self.targets = {}
        self.operating_sys = {}
        self.name = name
        self._init_targets()

    def add_target(self, name: str, target: archspec.cpu.Microarchitecture) -> None:
        if name in Platform.reserved_targets:
            msg = f"{name} is a spack reserved alias and cannot be the name of a target"
            raise ValueError(msg)
        self.targets[name] = target

    def _init_targets(self):
        self.default = archspec.cpu.host().name
        for name, microarchitecture in archspec.cpu.TARGETS.items():
            self.add_target(name, microarchitecture)

    def target(self, name):
        name = str(name)
        if name in Platform.deprecated_names:
            warnings.warn(f"target={name} is deprecated, use target={self.default} instead")

        if name in Platform.reserved_targets:
            name = self.default

        return self.targets.get(name, None)

    def add_operating_system(self, name, os_class):
        if name in Platform.reserved_oss + Platform.deprecated_names:
            msg = f"{name} is a spack reserved alias and cannot be the name of an OS"
            raise ValueError(msg)
        self.operating_sys[name] = os_class

    def default_target(self):
        return self.target(self.default)

    def default_operating_system(self):
        return self.operating_system(self.default_os)

    def operating_system(self, name):
        if name in Platform.deprecated_names:
            warnings.warn(f"os={name} is deprecated, use os={self.default_os} instead")

        if name in Platform.reserved_oss:
            name = self.default_os

        return self.operating_sys.get(name, None)

    def setup_platform_environment(self, pkg, env):
        """Platform-specific build environment modifications.

        This method is meant toi be overridden by subclasses, when needed.
        """
        pass

    @classmethod
    def detect(cls):
        """Returns True if the host platform is detected to be the current Platform class,
        False otherwise.

        Derived classes are responsible for implementing this method.
        """
        raise NotImplementedError()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def _cmp_iter(self):
        yield self.name
        yield self.default
        yield self.default_os

        def targets():
            for t in sorted(self.targets.values()):
                yield t._cmp_iter

        yield targets

        def oses():
            for o in sorted(self.operating_sys.values()):
                yield o._cmp_iter

        yield oses
