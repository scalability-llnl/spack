# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cpuinfo(CMakePackage):
    """cpuinfo is a library to detect essential
    for performance optimization information about host CPU."""

    homepage = "https://github.com/Maratyszcza/cpuinfo/"
    git      = "https://github.com/Maratyszcza/cpuinfo.git"

    version('master')
