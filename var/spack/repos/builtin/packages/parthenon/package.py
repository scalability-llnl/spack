# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Parthenon(CMakePackage):
    """A performance portable block-structured adaptive mesh refinement framework."""

    homepage = "https://github.com/parthenon-hpc-lab/parthenon"
    git = "https://github.com/parthenon-hpc-lab/parthenon.git"
    url = "https://github.com/parthenon-hpc-lab/parthenon/archive/v0.8.0.tar.gz"
    maintainers("pbrady", "pgrete")

    version("develop", branch="develop")
    version("24.03", sha256="ec9109c6bf442237641e627f301567527eb5e756b6959b6747d35315d041727c")
    version("23.11", sha256="76f79fb7d6556d94052829a8ac71f53cbda76f37fabd9233c5c0cd47ef561aee")
    version("0.8.0", sha256="9ed7c9ebdc84927a43b86c1e061f925b57cef9b567c7275f22779ed4d98e858d")

    depends_on("cxx", type="build")  # generated

    # ------------------------------------------------------------#
    # Variants
    # ------------------------------------------------------------#

    variant("single", default=False, description="Run in single precision")
    variant("mpi", default=True, description="Enable mpi")
    variant(
        "host_comm_buffers", default=False, description="Allocate communication buffers on host"
    )
    variant("hdf5", default=True, description="Enable hdf5")
    with when("+hdf5"):
        variant(
            "compression",
            default=True,
            description="Enable compression in hdf5 output/restart files",
        )
    variant("sparse", default=True, description="Sparse capability")
    variant("ascent", default=False, description="Enable Ascent for in-situ vis and analysis")
    variant("examples", default=False, description="Build example drivers")
    variant("python", default=False, description="Enable python for testing")
    variant(
        "pressure", default=False, description="Registry pressure check for Kokkos CUDA kernels"
    )

    # ------------------------------------------------------------#
    # Dependencies
    # ------------------------------------------------------------#

    depends_on("cmake@3.16:", type="build")

    depends_on("mpi", when="+mpi")
    depends_on("hdf5", when="+hdf5")
    depends_on("hdf5 +mpi", when="+mpi +hdf5")
    depends_on("ascent", when="+ascent")
    depends_on("python@3.5:", when="+python")
    depends_on("kokkos@4:")

    def cmake_args(self):
        spec = self.spec
        return [
            self.define("PARTHENON_IMPORT_KOKKOS", True),
            self.define_from_variant("PARTHENON_SINGLE_PRECISION", "single"),
            self.define_from_variant("PARTHENON_ENABLE_HOST_COMM_BUFFERS", "host_comm_buffers"),
            self.define_from_variant("CHECK_REGISTRY_PRESSURE", "pressure"),
            self.define_from_variant("PARTHENON_ENABLE_ASCENT", "ascent"),
            self.define("PARTHENON_DISABLE_MPI", not spec.variants["mpi"].value),
            self.define("PARTHENON_DISABLE_HDF5", not spec.variants["hdf5"].value),
            self.define(
                "PARTHENON_DISABLE_HDF5_COMPRESSION", not spec.variants["compression"].value
            ),
            self.define("PARTHENON_DISABLE_SPARSE", not spec.variants["sparse"].value),
            self.define("PARTHENON_DISABLE_EXAMPLES", not spec.variants["examples"].value),
            self.define("BUILD_TESTING", self.run_tests),
        ]
