# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ray(CMakePackage, SourceforgePackage):
    """Parallel genome assemblies for parallel DNA sequencing"""

    homepage = "https://denovoassembler.sourceforge.net/"
    sourceforge_mirror_path = "denovoassembler/Ray-2.3.1.tar.bz2"

    license("GPL-3.0-or-later")

    version("2.3.1", sha256="3122edcdf97272af3014f959eab9a0f0e5a02c8ffc897d842b06b06ccd748036")

    depends_on("cxx", type="build")  # generated

    depends_on("mpi")

    @run_after("build")
    def make(self):
        mkdirp(prefix.bin)
        make("PREFIX=%s" % prefix.bin)

    def install(self, spec, prefix):
        make("install")
