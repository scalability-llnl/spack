# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Heimdall(AutotoolsPackage, CudaPackage):
    """GPU accelerated transient detection pipeline"""

    homepage = "https://sourceforge.net/projects/heimdall-astro/"
    git = "https://git.code.sf.net/p/heimdall-astro/code"

    maintainers("aweaver1fandm")

    version("master", branch="master", preferred=True)

    depends_on("cxx", type="build")  # generated

    conflicts("~cuda", msg="You must specify +cuda")
    conflicts("cuda@11.8")
    conflicts("cuda_arch=none", msg="You must specify the CUDA architecture")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("cuda")

    # Pass the cuda architecture to DEDISP and PSRDADA for building
    for arch in CudaPackage.cuda_arch_values:
        depends_on(f"dedisp cuda_arch={arch}", when=f"cuda_arch={arch}")

        depends_on(f"psrdada cuda_arch={arch}", when=f"cuda_arch={arch}")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.spec["psrdada"].prefix.bin)
        env.prepend_path("PATH", self.prefix.bin)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["dedisp"].prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["cuda"].prefix.lib)

    def configure_args(self):
        # Required flags for configure
        args = [
            f"--with-psrdada-dir={self.spec['psrdada'].prefix}",
            f"--with-dedisp-dir={self.spec['dedisp'].prefix}",
            f"--with-cuda-dir={self.spec['cuda'].prefix}",
        ]
        return args
