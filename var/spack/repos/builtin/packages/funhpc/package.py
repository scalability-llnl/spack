# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Funhpc(CMakePackage):
    """FunHPC: Functional HPC Programming"""

    homepage = "https://github.com/eschnett/FunHPC.cxx"
    url = "https://github.com/eschnett/FunHPC.cxx/archive/version/1.3.0.tar.gz"
    git = "https://github.com/eschnett/FunHPC.cxx.git"

    version("develop", branch="master")
    version("1.3.0", sha256="140e60f55a307f21117bd43fa16db35d60c0df5ef37e17a4da1cb3f5da5e29c1")

    depends_on("cxx", type="build")  # generated

    variant("pic", default=True, description="Produce position-independent code")

    depends_on("cereal")
    depends_on("googletest")
    depends_on("hwloc")
    depends_on("jemalloc")
    depends_on("mpi")
    depends_on("qthreads")

    def cmake_args(self):
        spec = self.spec
        options = ["-DGTEST_ROOT=%s" % spec["googletest"].prefix]
        if spec.satisfies("+pic"):
            options += ["-DCMAKE_POSITION_INDEPENDENT_CODE:BOOL=true"]
        return options

    def check(self):
        with working_dir(self.build_directory):
            make("test", "CTEST_OUTPUT_ON_FAILURE=1")
