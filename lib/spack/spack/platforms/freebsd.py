# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import platform

from spack.operating_systems.freebsd import FreeBSDOs

from ._platform import Platform


class FreeBSD(Platform):
    priority = 102

    def __init__(self):
        super().__init__("freebsd")
        os = FreeBSDOs()
        self.default_os = str(os)
        self.add_operating_system(str(os), os)

    @classmethod
    def detect(cls):
        return platform.system().lower() == "freebsd"
