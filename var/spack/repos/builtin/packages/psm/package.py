# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Psm(MakefilePackage):
    """Intel Performance scaled messaging library"""

    homepage = "https://github.com/intel/psm"
    url = "https://github.com/intel/psm/archive/v3.3.tar.gz"
    git = "https://github.com/intel/psm.git"

    license("GPL-2.0-only")

    version(
        "3.3",
        sha256="034b10e24d9f2967ef0f8d0f828572295e89cdfa1ba30c35e288b9b23c3dab8f",
        preferred=True,
    )
    version("2017-04-28", commit="604758e76dc31e68d1de736ccf5ddf16cb22355b")

    depends_on("c", type="build")  # generated

    conflicts("%gcc@6:", when="@3.3")

    depends_on("uuid")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("{DESTDIR}/usr/", "{LOCAL_PREFIX}/")

    def install(self, spec, prefix):
        make("LOCAL_PREFIX=%s" % prefix, "install")
