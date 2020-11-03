# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

import archspec.cpu

from spack.architecture import Platform, Target
from spack.operating_systems.mac_os import MacOs


class Darwin(Platform):
    priority    = 89

    binary_formats = ['macho']

    def __init__(self):
        super(Darwin, self).__init__('darwin')

        for name in archspec.cpu.TARGETS:
            self.add_target(name, Target(name))

        self.default = archspec.cpu.host().name
        self.front_end = self.default
        self.back_end = self.default

        mac_os = MacOs()

        self.default_os = str(mac_os)
        self.front_os   = str(mac_os)
        self.back_os    = str(mac_os)

        self.add_operating_system(str(mac_os), mac_os)

    @classmethod
    def detect(cls):
        return 'darwin' in platform.system().lower()
