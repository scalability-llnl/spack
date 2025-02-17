# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import platform

from spack.operating_systems.linux_distro import LinuxDistro

from ._platform import Platform


class Linux(Platform):
    priority = 90

    def __init__(self):
        super().__init__("linux")
        linux_dist = LinuxDistro()
        self.default_os = str(linux_dist)
        self.add_operating_system(str(linux_dist), linux_dist)

    @classmethod
    def detect(cls):
        return "linux" in platform.system().lower()
