# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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

    if platform.machine() == "arm64":
        front_end = "aarch64"
        back_end = "m1"
        default = "m1"
    else:
        front_end = "x86_64"
        back_end = "core2"
        default = "core2"

    front_os = "redhat6"
    back_os = "debian6"
    default_os = "debian6"

    def __init__(self, name=None):
        name = name or "test"
        super().__init__(name)
        self.add_target(self.default, archspec.cpu.TARGETS[self.default])
        self.add_target(self.front_end, archspec.cpu.TARGETS[self.front_end])

        self.add_operating_system(
            self.default_os, spack.operating_systems.OperatingSystem("debian", 6)
        )
        self.add_operating_system(
            self.front_os, spack.operating_systems.OperatingSystem("redhat", 6)
        )

    @classmethod
    def detect(cls):
        return True
