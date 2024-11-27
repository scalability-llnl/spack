# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libhbaapi(AutotoolsPackage):
    """The SNIA HBA API library"""

    homepage = "https://github.com/cleech/libHBAAPI"
    url = "https://github.com/cleech/libHBAAPI/archive/v3.11.tar.gz"

    license("SNIA")

    version("3.11", sha256="c7b2530d616fd7bee46e214e7eb91c91803aec3297a7c6bbf73467a1edad4e10")
    version("3.10", sha256="ca4f4ec3defa057c1b51bc87cc749efe5d54579e055d7a51688d18cc35166462")
    version("3.9", sha256="8e60616abde44488fed05254988f9b41653d2204a7218072714d6623e099c863")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
