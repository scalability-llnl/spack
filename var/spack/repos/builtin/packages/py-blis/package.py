# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBlis(PythonPackage):
    """Cython BLIS: Fast BLAS-like operations from Python and Cython,
    without the tears"""

    homepage = "https://github.com/explosion/cython-blis"
    pypi = "blis/blis-0.4.1.tar.gz"

    license("BSD-3-Clause")

    version("0.9.1", sha256="7ceac466801f9d97ecb34e10dded8c24cf5e0927ea7e834da1cc9d2ed3fc366f")
    version("0.7.9", sha256="29ef4c25007785a90ffc2f0ab3d3bd3b75cd2d7856a9a482b7d0dac8d511a09d")
    version("0.4.1", sha256="d69257d317e86f34a7f230a2fd1f021fd2a1b944137f40d8cdbb23bd334cd0c4")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-cython@0.25:", when="@0.7.9:", type="build")
    depends_on("py-numpy@1.15:", type=("build", "run"))

    def setup_build_environment(self, env):
        env.set("BLIS_COMPILER", spack_cc)
        env.set("BLIS_ARCH", "generic")
