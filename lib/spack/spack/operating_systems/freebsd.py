# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import platform as py_platform

from spack.version import Version

from ._operating_system import OperatingSystem


class FreeBSDOs(OperatingSystem):
    def __init__(self):
        release = py_platform.release().split("-", 1)[0]
        super().__init__("freebsd", Version(release))
