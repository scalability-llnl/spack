# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.operating_systems.windows_os import WindowsOs

from ._platform import Platform


class Windows(Platform):
    priority = 101

    def __init__(self):
        super().__init__("windows")
        windows_os = WindowsOs()
        self.default_os = str(windows_os)
        self.add_operating_system(str(windows_os), windows_os)

    @classmethod
    def detect(cls):
        plat = platform.system().lower()
        return "cygwin" in plat or "win32" in plat or "windows" in plat
