# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
from spack.architecture import Platform, Target
from spack.operating_systems.linux_distro import LinuxDistro
import llnl.util.cpu as cpu


class SpackCross(Platform):
    priority    = 10

    def __init__(self):
        ''' Cross Compiler Environment.'''

        super(SpackCross, self).__init__('SpackCross')
        for name in cpu.targets:
            self.add_target(name, Target(name))

        self.back_end = os.environ.get('SPACK_BACKEND_TARGET')
        backend_os = os.environ.get('SPACK_BACKEND_OS')
        backend_os_version = os.environ.get('SPACK_BACKEND_OS_VERSION')
        self.front_end = cpu.host().name
        self.add_target("front_end", Target(self.front_end))
        self.add_target(self.back_end, Target(self.back_end))
        self.add_target("back_end", Target(self.back_end))
        self.add_target(self.default, Target(self.back_end))

        front_distro = LinuxDistro()
        back_distro = LinuxDistro()
        if backend_os is not None:
            back_distro.name = backend_os
        if backend_os_version is not None:
            back_distro.version = backend_os_version

        self.front_os = str(front_distro)
        self.back_os = str(back_distro)
        self.default_os = self.back_os

        self.add_operating_system(str(front_distro), front_distro)
        self.add_operating_system(str(back_distro), back_distro)

    @classmethod
    def detect(cls):
        return os.environ.get('SPACK_BACKEND_TARGET') is not None
