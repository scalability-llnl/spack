# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class HwProbe(MakefilePackage):
    """Hardware Probe Tool (hw-probe)."""

    homepage = "https://github.com/linuxhw/hw-probe"
    url = "https://github.com/linuxhw/hw-probe/archive/1.5.tar.gz"

    license("LGPL-2.1-or-later OR BSD-4-Clause")

    version("1.6", sha256="de048be6aef357d3142c9e2327d6f79d205a42aa3396ad381ed319115d1c9a22")
    version("1.5", sha256="8bb7d6ff272c1412e26fcfd86e9df5c3e34e1584552404b930c281b8498b25ea")
    version("1.4", sha256="90f3ea83bf641348b209e4a2a910f65d836ae7828c0be0f660236ea413bc46bb")
    version("1.3", sha256="820ada4f16cb827e0990eb918e75423845fef54a863fdd88aa5bd23127354229")

    def install(self, spec, prefix):
        make("install", f"prefix={prefix}")
