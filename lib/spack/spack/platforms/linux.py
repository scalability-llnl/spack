# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import platform

import archspec.cpu

from spack.architecture import Platform, Target
from spack.operating_systems.linux_distro import LinuxDistro


class Linux(Platform):
    priority    = 90

    def __init__(self):
        super(Linux, self).__init__('linux')

        for name in archspec.cpu.TARGETS:
            self.add_target(name, Target(name))

        # Get specific default
        self.default = archspec.cpu.host().name
        self.front_end = self.default
        self.back_end = self.default

        linux_dist = LinuxDistro()
        self.default_os = str(linux_dist)
        self.front_os = self.default_os
        self.back_os = self.default_os
        self.add_operating_system(str(linux_dist), linux_dist)

    @classmethod
    def detect(cls):
        return 'linux' in platform.system().lower()
