# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JsonFortran(CMakePackage):
    """A Fortran 2008 JSON API"""

    homepage = "https://jacobwilliams.github.io/json-fortran/"
    url = "https://github.com/jacobwilliams/json-fortran/archive/8.3.0.tar.gz"
    git = "https://github.com/jacobwilliams"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("8.3.0", sha256="5fe9ad709a726416cec986886503e0526419742e288c4e43f63c1c22026d1e8a")
    version("8.2.5", sha256="16eec827f64340c226ba9a8463f001901d469bc400a1e88b849f258f9ef0d100")
    version("8.2.4", sha256="7b4e0aecdb92705918f15e3094022325bb14c9ea620d7eba6a4facf9ef8f27f3")
    version("8.2.3", sha256="884ef4f955eecaf18d52e818738089ab3924981fb510ef3671ad3f62ac7c6af1")
    version("8.2.2", sha256="3228496c9a10aa01da7694196ec5cd8cd463099be734207dac93e2097ea5279d")
    version("8.2.1", sha256="428fb2e708cce3a29f9bbc84ce63f112a2eb44fd1b0d2a88d83c86583ca83ed4")
    version("8.2.0", sha256="df9986c4ecad996f3be3d6855397141e63721207fe90e1500ae0df587d46481f")
    version("8.1.0", sha256="4f4b3bf102d7e22327b0e4b8a3cadd8c3e453c969547ec21cd2429ed7d4c5404")
    version("8.0.0", sha256="2c9c62117a2548e2cddf55acf7b726b529c044ed0f1eefe14dc69910a54a7bfd")
    version("7.1.0", sha256="e7aa1f6e09b25ebacb17188147380c3f8c0a254754cd24869c001745fcecc9e6")
    version("7.0.0", sha256="9b5b6235489b27d572bbc7620ed8e039fa9d4d14d41b1581b279be9db499f32c")
    version("6.11.0", sha256="0ce38236a0debcd775108684b835f9f92ca9d6594da714c0025014fe9f03eec3")

    depends_on("fortran", type="build")  # generated

    depends_on("cmake@2.8.8:", type="build")

    def cmake_args(self):
        return [
            "-DCMAKE_POSITION_INDEPENDENT_CODE=ON",
            "-DSKIP_DOC_GEN:BOOL=ON",
            "-DUSE_GNU_INSTALL_CONVENTION=ON",
        ]

    def check(self):
        # `make check` works but `make test` doesn't:
        # https://github.com/jacobwilliams/json-fortran/issues/154
        with working_dir(self.build_directory):
            make("check")
