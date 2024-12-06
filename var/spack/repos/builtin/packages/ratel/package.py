# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ratel(MakefilePackage, CudaPackage, ROCmPackage):
    """Extensible, performance-portable solid mechanics with libCEED and PETSc"""

    homepage = "https://ratel.micromorph.org"
    git = "https://gitlab.com/micromorph/ratel.git"

    maintainers("jedbrown", "jeremylt")

    license("BSD-2-Clause")

    version("develop", branch="main")
    version("0.3.0", tag="v0.3.0", commit="ca2f3357e10b89fb274626fba104aad30c72774b")
    version("0.2.1", tag="v0.2.1", commit="043b61696a2407205fdfd898681467d1a7ff59e0")
    version("0.1.2", tag="v0.1.2", commit="94ad630bf897d231af7a94bf08257f6067258aae")

    depends_on("c", type="build")  # generated

    # development version
    depends_on("libceed@develop", when="@develop")
    depends_on("petsc@main", when="@develop")
    # released versions
    depends_on("libceed@0.12.0:0.12", when="@0.3.0")
    depends_on("petsc@3.20.0:3.20", when="@0.3.0")
    depends_on("libceed@0.11.0:0.11", when="@0.2.1")
    depends_on("petsc@3.18.3:3.18", when="@0.2.1")
    depends_on("libceed@0.10.1:0.10", when="@0.1.2")
    depends_on("petsc@3.17:3.17", when="@0.1.2")

    # Note: '+cuda' and 'cuda_arch' variants are added by the CudaPackage
    #       '+rocm' and 'amdgpu_target' variants are added by the ROCmPackage
    # But we need to sync cuda/rocm with libCEED and PETSc
    for sm_ in CudaPackage.cuda_arch_values:
        depends_on(
            "libceed+cuda cuda_arch={0}".format(sm_), when="+cuda cuda_arch={0}".format(sm_)
        )
        depends_on("petsc+cuda cuda_arch={0}".format(sm_), when="+cuda cuda_arch={0}".format(sm_))
    for gfx in ROCmPackage.amdgpu_targets:
        depends_on(
            "libceed+rocm amdgpu_target={0}".format(gfx),
            when="+rocm amdgpu_target={0}".format(gfx),
        )
        depends_on(
            "petsc+rocm amdgpu_target={0}".format(gfx), when="+rocm amdgpu_target={0}".format(gfx)
        )
    # Kokkos required for AMD GPUs
    depends_on("petsc+kokkos", when="+rocm")

    @property
    def common_make_opts(self):
        spec = self.spec

        # verbose build and test
        make_options = ["V=1", "PROVE_OPTS=-v"]

        # libCEED and PETSc dirs
        make_options += [
            "CEED_DIR=%s" % spec["libceed"].prefix,
            "PETSC_DIR=%s" % spec["petsc"].prefix,
        ]
        return make_options

    def edit(self, spec, prefix):
        make("info", *self.common_make_opts)

    @property
    def build_targets(self):
        return self.common_make_opts

    @property
    def install_targets(self):
        return ["install", "prefix={0}".format(self.prefix)] + self.common_make_opts

    def check(self):
        make("prove", *self.common_make_opts, parallel=False)
