# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------

from spack.package import *


class Clblast(CMakePackage):
    """CLBlast is a modern, lightweight, performant and tunable OpenCL BLAS
    library written in C++11. It is designed to leverage the full performance
    potential of a wide variety of OpenCL devices from different vendors,
    including desktop and laptop GPUs, embedded GPUs, and other accelerators.
    CLBlast implements BLAS routines: basic linear algebra subprograms
    operating on vectors and matrices."""

    homepage = "https://cnugteren.github.io/clblast/clblast.html"
    git = "https://github.com/CNugteren/CLBlast"
    url = "https://github.com/CNugteren/CLBlast/archive/refs/tags/1.5.2.zip"

    maintainers("umar456")

    license("Apache-2.0")

    version("master", branch="master")
    version("1.5.2", sha256="0e3a017c3aa352e0bf94ea65cfc9609beb2c22204d31c2ef43d0478178cfee00")
    version("1.5.1", sha256="a0f0cb7308b59a495c23beaef1674093ed26996f66d439623808755dbf568c3f")
    version("1.5.0", sha256="1bf8584ee4370d5006a467a1206276ab23e32ba03fd1bd0f1c6da6a6c9f03bc9")
    version("1.4.1", sha256="c22dab892641301b24bd90f5a6916a10b5a877c5f5f90c2dc348a58d39a278a7")
    version("1.4.0", sha256="ae00393fab7f7a85a6058ffb336670d1a529213eea288af4d657a32f2834564a")
    version("1.3.0", sha256="cf314e976329dd2dfd467b713247c020b06c0fc17d4261d94c4aabbf34f5827f")
    version("1.2.0", sha256="3adfd5b5ffa2725e3c172de7cde8cc7019cd295fac4e37d39839e176db0db652")
    version("1.1.0", sha256="2896f5c8ac6580b1adf026770ef5a664b209484c47189c55466f8884ffd33052")
    version("1.0.1", sha256="6c9415a1394c554debce85c47349ecaaebdc9d5baa187d3ecb84be00ae9c70f0")
    version("1.0.0", sha256="230a55a868bdd21425867cbd0dcb7ec046aa5ca522fb5694e42740b5b16d0f59")

    depends_on("opencl")
    depends_on("pocl+icd", when="^[virtuals=opencl] pocl")

    variant("shared", description="Build a shared libraries", default=True)
    variant("tuners", description="Enable compilation of the tuners", default=False)
    variant("netlib", description="Enable compilation of the CBLAS Netlib API", default=False)

    provides("blas", when="+netlib")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("TESTS", self.run_tests),
            self.define_from_variant("TUNERS"),
            self.define_from_variant("NETLIB"),
        ]
        return args
