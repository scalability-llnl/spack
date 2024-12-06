# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AutodockGpu(MakefilePackage, CudaPackage):
    """AutoDock-GPU: AutoDock for GPUs and other accelerators.
    OpenCL and Cuda accelerated version of AutoDock 4.2.6. It
    leverages its embarrasingly parallelizable LGA by processing
    ligand-receptor poses in parallel over multiple compute units.
    """

    homepage = "https://ccsb.scripps.edu/autodock"
    git = "https://github.com/ccsb-scripps/AutoDock-GPU.git"

    maintainers("RemiLacroix-IDRIS")

    license("LGPL-2.1-or-later")

    version("develop", branch="develop")

    depends_on("cxx", type="build")  # generated

    variant(
        "device",
        default="cuda",
        description="Acceletor runtime",
        values=("cuda", "oclgpu"),
        multi=False,
    )
    variant("overlap", default=False, description="Overlap CPU and GPU operations")
    variant("cuda", default=True, description="Build with CUDA")

    depends_on("cuda")

    conflicts("~cuda")  # the cuda variant is mandatory
    conflicts("+cuda", when="cuda_arch=none")

    @property
    def build_targets(self):
        spec = self.spec
        return [
            "DEVICE={0}".format(spec.variants["device"].value.upper()),
            "TARGETS={0}".format(" ".join(spec.variants["cuda_arch"].value)),
            "GPU_INCLUDE_PATH={0}".format(spec["cuda"].prefix.include),
            "GPU_LIBRARY_PATH={0}".format(spec["cuda"].libs.directories[0]),
            "OVERLAP={0}".format("ON" if "+overlap" in spec else "OFF"),
        ]

    def install(self, spec, prefix):
        ignore_gitkeep = lambda p: p.endswith(".gitkeep")
        install_tree("bin", prefix.bin, ignore=ignore_gitkeep)
