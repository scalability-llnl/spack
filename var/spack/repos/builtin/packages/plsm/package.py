# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Plsm(CMakePackage, CudaPackage):
    """plsm is a generic library for spatial subdivision within an N-dimensional lattice."""

    homepage = "https://github.com/ORNL-Fusion/plsm"
    url = "https://github.com/ORNL-Fusion/plsm/archive/refs/tags/v2.1.2.tar.gz"
    git = "https://github.com/ORNL-Fusion/plsm.git"

    maintainers("PhilipFackler", "sblondel")
    license("BSD-3-Clause", checked_by="PhilipFackler")

    version("2.1.2", sha256="0816fc604b35aac9d848063c2cb2e20abef5e39e146d745873a061a9445ec277")
    version("2.0.4", sha256="a92080c7015d33a11ffd0d790a75341d1b1e3b7d19331fbd48c5e6a15a09693d")
    version("2.0.3", sha256="d7ca114dd566ee8f1485bcb5e4d9307a43c33f107d295cec31a568b3ad7064bc")
    version("2.0.1", sha256="b5b60172ee398a08df9d11b04719d85c7c99c6a5b10b3709f72fcd40a920c0c3")
    version("2.0.0", sha256="833e63134101e1574de383e3d6d50fcee60ef7f9e69394d5b4c722e2a6317017")
    version("1.1.1", sha256="e40e2d5d3339b303a0056bcec0882b3040e69b38ddef4c3154a6e8ce3d83ebb8")

    depends_on("cxx", type="build")

    variant("int64", default=True, description="Use 64-bit indices")
    variant("openmp", default=False, description="Activates OpenMP backend")

    conflicts("+cuda", when="cuda_arch=none")
    conflicts("+openmp", when="+cuda", msg="Can't use both OpenMP and CUDA")

    depends_on("kokkos")
    depends_on("kokkos +openmp", when="+openmp")
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on(
            f"kokkos+cmake_lang+cuda+cuda_lambda cuda_arch={cuda_arch}",
            when=f"+cuda cuda_arch={cuda_arch}",
        )

    def cmake_args(self):
        args = [
            self.define("BUILD_TESTING", self.run_tests),
            self.define_from_variant("PLSM_USE_64BIT_INDEX_TYPE", "int64"),
        ]
        return args
