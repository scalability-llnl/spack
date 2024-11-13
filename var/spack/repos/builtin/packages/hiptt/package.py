# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hiptt(MakefilePackage, ROCmPackage):
    """hipTT - Fast GPU Tensor Transpose for NVIDIA and AMD GPU."""

    homepage = "https://github.com/DmitryLyakh/hipTT"
    url = "https://github.com/DmitryLyakh/hipTT"
    git = "https://github.com/DmitryLyakh/hipTT.git"
    tags = ["ecp", "radiuss"]

    maintainers("bvanessen")

    license("Unlicense")

    version("master", branch="master")

    depends_on("cxx", type="build")  # generated

    patch("bugfix_make.patch")

    # To enable this package add it to the LD_LIBRARY_PATH
    def setup_dependent_build_environment(self, env, dependent_spec):
        hiptt_home = self.spec["hiptt"].prefix
        env.prepend_path("cuTT_ROOT", hiptt_home)
        env.prepend_path("cuTT_LIBRARY", hiptt_home.lib)
        env.prepend_path("cuTT_INCLUDE_PATH", hiptt_home.include)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("bin/cutt_test", prefix.bin)
        install("bin/cutt_bench", prefix.bin)
        install_tree("lib", prefix.lib)
        install_tree("include", prefix.include)
