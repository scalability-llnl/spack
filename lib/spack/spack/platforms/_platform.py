# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from typing import Optional

import archspec.cpu

import llnl.util.lang

import spack.error


class NoPlatformError(spack.error.SpackError):
    def __init__(self):
        msg = "Could not determine a platform for this machine"
        super().__init__(msg)


@llnl.util.lang.lazy_lexicographic_ordering
class Platform:
    """Platform is an abstract class extended by subclasses.

    To add a new type of platform (such as cray_xe), create a subclass and set all the
    class attributes such as priority, front_target, back_target, front_os, back_os.

    Platform also contain a priority class attribute. A lower number signifies higher
    priority. These numbers are arbitrarily set and can be changed though often there
    isn't much need unless a new platform is added and the user wants that to be
    detected first.

    Targets are created inside the platform subclasses. Most architecture (like linux,
    and darwin) will have only one target family (x86_64) but in the case of Cray
    machines, there is both a frontend and backend processor. The user can specify
    which targets are present on front-end and back-end architecture.

    Depending on the platform, operating systems are either autodetected or are
    set. The user can set the frontend and backend operating setting by the class
    attributes front_os and back_os. The operating system will be responsible for
    compiler detection.
    """

    # Subclass sets number. Controls detection order
    priority: Optional[int] = None

    #: binary formats used on this platform; used by relocation logic
    binary_formats = ["elf"]

    front_end: Optional[str] = None
    back_end: Optional[str] = None
    default: Optional[str] = None  # The default back end target.

    front_os: Optional[str] = None
    back_os: Optional[str] = None
    default_os: Optional[str] = None

    reserved_targets = ["default_target", "frontend", "fe", "backend", "be"]
    reserved_oss = ["default_os", "frontend", "fe", "backend", "be"]

    def __init__(self, name):
        self.targets = {}
        self.operating_sys = {}
        self.name = name

    def add_target(self, name: str, target: archspec.cpu.Microarchitecture) -> None:
        """Used by the platform specific subclass to list available targets.
        Raises an error if the platform specifies a name
        that is reserved by spack as an alias.
        """
        if name in Platform.reserved_targets:
            msg = "{0} is a spack reserved alias and cannot be the name of a target"
            raise ValueError(msg.format(name))
        self.targets[name] = target

    def _add_archspec_targets(self):
        for name, microarchitecture in archspec.cpu.TARGETS.items():
            self.add_target(name, microarchitecture)

    def target(self, name):
        """This is a getter method for the target dictionary
        that handles defaulting based on the values provided by default,
        front-end, and back-end. This can be overwritten
        by a subclass for which we want to provide further aliasing options.
        """
        # TODO: Check if we can avoid using strings here
        name = str(name)
        if name == "default_target":
            name = self.default
        elif name == "frontend" or name == "fe":
            name = self.front_end
        elif name == "backend" or name == "be":
            name = self.back_end

        return self.targets.get(name, None)

    def add_operating_system(self, name, os_class):
        """Add the operating_system class object into the
        platform.operating_sys dictionary.
        """
        if name in Platform.reserved_oss:
            msg = "{0} is a spack reserved alias and cannot be the name of an OS"
            raise ValueError(msg.format(name))
        self.operating_sys[name] = os_class

    def operating_system(self, name):
        if name == "default_os":
            name = self.default_os
        if name == "frontend" or name == "fe":
            name = self.front_os
        if name == "backend" or name == "be":
            name = self.back_os

        return self.operating_sys.get(name, None)

    def setup_platform_environment(self, pkg, env):
        """Subclass can override this method if it requires any
        platform-specific build environment modifications.
        """
        pass

    @classmethod
    def detect(cls):
        """Return True if the the host platform is detected to be the current
        Platform class, False otherwise.

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
        yield self.front_end
        yield self.back_end
        yield self.default_os
        yield self.front_os
        yield self.back_os

        def targets():
            for t in sorted(self.targets.values()):
                yield t._cmp_iter

        yield targets

        def oses():
            for o in sorted(self.operating_sys.values()):
                yield o._cmp_iter

        yield oses
