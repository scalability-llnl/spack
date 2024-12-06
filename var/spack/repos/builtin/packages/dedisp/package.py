# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dedisp(MakefilePackage, CudaPackage):
    """GPU-based dedispersion package."""

    homepage = "https://github.com/ajameson/dedisp"
    git = "https://github.com/ajameson/dedisp.git"

    maintainers("aweaver1fandm")

    version("master", branch="master", preferred=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    conflicts("~cuda", msg="You must specify +cuda")
    conflicts("cuda@11.8")
    conflicts("cuda_arch=none", msg="You must specify the CUDA architecture")

    depends_on("cuda", type="build")

    def edit(self, spec, prefix):
        # Build process required some edits to Makefile.inc instead of using command-line flags
        makefile = FileFilter("Makefile.inc")

        makefile.filter(r"^\s*CUDA_PATH\s*\?=.*", "CUDA_PATH ?= " + spec["cuda"].prefix)
        makefile.filter(
            r"^\s*GPU_ARCH\s*\?=.*", "GPU_ARCH ?= sm_" + spec.variants["cuda_arch"].value[0]
        )
        makefile.filter(r"^\s*INSTALL_DIR\s*\?=.*", "INSTALL_DIR ?= " + prefix)

    @run_before("install")
    def preinstall(self):
        # The $PREFIX/dedisp/include and $PREFIX/dedisp/lib directories don't seem
        # to be created automatically by the software's Makefile so manually create them
        libdir = join_path(self.prefix, "lib")
        incdir = join_path(self.prefix, "include")
        mkdirp(libdir)
        mkdirp(incdir)
