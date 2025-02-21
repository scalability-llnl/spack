# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import platform

import archspec.cpu

import spack.operating_systems

from ._platform import Platform


class Test(Platform):
    priority = 1000000

    if platform.system().lower() == "darwin":
        binary_formats = ["macho"]

    default_os = "debian6"
    default = "m1" if platform.machine() == "arm64" else "core2"

    def __init__(self, name=None):
        name = name or "test"
        super().__init__(name)
        self.add_operating_system("debian6", spack.operating_systems.OperatingSystem("debian", 6))
        self.add_operating_system("redhat6", spack.operating_systems.OperatingSystem("redhat", 6))

    def _init_targets(self):
        targets = ("aarch64", "m1") if platform.machine() == "arm64" else ("x86_64", "core2")
        for t in targets:
            self.add_target(t, archspec.cpu.TARGETS[t])

    @classmethod
    def detect(cls):
        return True
