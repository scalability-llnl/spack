# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dtbuild1(Package):
    """Package for use as a build tool for deptypes testing which has its own
    deptree"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dtbuild1-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")
    version("0.5", md5="fedcba9876543210fedcba9876543210")

    depends_on("vdtbuild2", type="build")
    depends_on("dtlink2")
    depends_on("dtrun2", type="run")
