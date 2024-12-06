# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dorado(CMakePackage, CudaPackage):
    """Dorado is a high-performance, easy-to-use, open source basecaller
    for Oxford Nanopore reads."""

    homepage = "https://github.com/nanoporetech/dorado"
    git = "https://github.com/nanoporetech/dorado.git"
    url = "https://github.com/nanoporetech/dorado/archive/refs/tags/v0.5.1.tar.gz"

    maintainers("snehring")

    version("0.5.3", commit="d9af343c0097e0e60503231e036d69e6eda2f19a", submodules=True)
    version("0.5.1", commit="a7fb3e3d4afa7a11cb52422e7eecb1a2cdb7860f", submodules=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("git", type="build")
    depends_on("curl", type="build")
    depends_on("cuda")
    depends_on("hdf5@1.17:+hl+cxx+szip")
    depends_on("htslib@1.15.1")
    depends_on("openssl")
    depends_on("zstd")
    depends_on("libdeflate")
    depends_on("zlib-api")

    conflicts("%gcc@:8", msg="Dorado requires at least gcc@9 to compile.")
    conflicts("%gcc@13:", msg="Dorado will not build with gcc@13 and newer.")

    patch("cmake-htslib.patch")

    def setup_build_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.spec["libdeflate"].prefix.lib64)
        env.prepend_path("LIBRARY_PATH", self.spec["libdeflate"].prefix.lib64)

    def cmake_args(self):
        htslib_prefix = self.spec["htslib"].prefix
        args = [f"-DHTSLIB_PREFIX={htslib_prefix}", f"-DDORADO_INSTALL_PATH={self.prefix}"]
        return args
