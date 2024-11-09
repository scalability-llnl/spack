# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

from spack.error import NoHeadersError
from spack.package import *


class Elsi(CMakePackage, CudaPackage):
    """ELSI provides a unified interface for electronic structure
    codes to a variety of eigenvalue solvers."""

    homepage = "https://wordpress.elsi-interchange.org/"
    url = "https://gitlab.com/elsi_project/elsi_interface/-/archive/v2.10.1/elsi_interface-v2.10.1.tar.gz"
    git = "https://gitlab.com/elsi_project/elsi_interface.git"

    license("BSD-3-Clause")

    version("2.11.0", sha256="2e6929827ed9c99a32381ed9da40482e862c28608d59d4f27db7dcbcaed1520d")
    version("2.10.1", sha256="b3c7526d46a9139a26680787172a3df15bc648715a35bdf384053231e94ab829")
    version(
        "2.2.1",
        sha256="5b4b2e8fa4b3b68131fe02cc1803a884039b89a1b1138af474af66453bec0b4d",
        deprecated=True,
    )
    version("master", branch="master")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    generator("ninja")

    variant(
        "add_underscore",
        default=True,
        description="Suffix C functions with an underscore",
        when="@2.2.1",
    )
    variant(
        "elpa2_kernel",
        default="none",
        description="ELPA2 Kernel",
        values=("none", "AVX", "AVX2", "AVX512"),
        multi=False,
    )
    variant("enable_pexsi", default=False, description="Enable PEXSI support")
    variant("enable_sips", default=False, description="Enable SLEPc-SIPs support")
    variant("use_external_elpa", default=True, description="Build ELPA using SPACK")
    variant("use_external_ntpoly", default=True, description="Build NTPoly using SPACK")
    variant(
        "use_external_superlu", default=True, description="Use external SuperLU DIST", when="@:2.2"
    )
    variant(
        "use_external_pexsi",
        default=True,
        description="Use external PEXSI",
        when="@2.3: +enable_pexsi",
    )
    variant("use_external_omm", default=True, description="Use external libOMM")
    variant(
        "use_mpi_iallgather",
        default=True,
        description="Use non-blocking collective MPI functions",
        when="@:2.5",
    )
    variant(
        "internal_elpa_version",
        default="2020",
        values=("2020", "2021", conditional("2023", "2023_11", "2024", when="@:2.11")),
        description="Internal ELPA version",
        multi=False,
    )
    variant("dlaf", default=False, when="@2.11:", description="Enable DLA-Future support")

    # Basic dependencies
    depends_on("blas", type="link")
    depends_on("lapack", type="link")
    depends_on("scalapack", type="link")
    depends_on("mpi")

    # Library dependencies
    with when("+use_external_ntpoly"):
        depends_on("ntpoly")
        depends_on("ntpoly@3:", when="@2.11:")
        conflicts("^ntpoly@3:", when="@:2.10")
    with when("+use_external_elpa"):
        depends_on("elpa+cuda", when="+cuda")
        depends_on("elpa~cuda", when="~cuda")
    with when("+enable_sips"):
        depends_on("slepc+cuda", when="+cuda")
        depends_on("slepc~cuda", when="~cuda")
        depends_on("petsc+cuda", when="+cuda")
        depends_on("petsc~cuda", when="~cuda")
    with when("+use_external_superlu"):
        depends_on("superlu-dist+cuda", when="+cuda")
        depends_on("superlu-dist~cuda", when="~cuda")
    with when("+enable_pexsi +use_external_pexsi"):
        depends_on("pexsi+fortran")
        depends_on("superlu-dist+cuda", when="+cuda")
        depends_on("superlu-dist~cuda", when="~cuda")
        conflicts("^pexsi@2:", when="@:2.11")
    with when("+use_external_omm"):
        depends_on("omm")
        depends_on("matrix-switch")  # Direct dependency
    with when("+dlaf"):
        depends_on("dla-future-fortran")
        conflicts("dla-future~cuda", when="+cuda")
        conflicts("dla-future+cuda", when="~cuda")

    def cmake_args(self):
        libs_names = ["scalapack", "lapack", "blas"]

        # External libraries
        if self.spec.satisfies("+use_external_elpa"):
            libs_names.append("elpa")
        if self.spec.satisfies("+use_external_ntpoly"):
            libs_names.append("ntpoly")
        if self.spec.satisfies("+use_external_superlu"):
            libs_names.append("superlu-dist")
        if self.spec.satisfies("+use_external_pexsi"):
            libs_names.append("superlu-dist")
            libs_names.append("pexsi")
        if self.spec.satisfies("+use_external_omm"):
            libs_names.append("omm")
            libs_names.append("matrix-switch")
        if self.spec.satisfies("+dlaf"):
            libs_names.append("dla-future-fortran")

        lib_paths, inc_paths, libs = [], [], []
        for lib in libs_names:
            lib_paths.extend(self.spec[lib].libs.directories)
            libs.extend(self.spec[lib].libs.names)

            try:
                inc_paths.extend(self.spec[lib].headers.directories)

                # Deal with Fortran modules
                for path in self.spec[lib].headers:
                    # Add path to .mod files
                    # headers.directories only add path up to include/
                    if path.endswith(".mod"):
                        inc_paths.append(os.path.dirname(path))
            except NoHeadersError:
                pass

        args = [
            # Compiler Information (ELSI wants these explicitly set)
            self.define("CMAKE_Fortran_COMPILER", self.spec["mpi"].mpifc),
            self.define("CMAKE_C_COMPILER", self.spec["mpi"].mpicc),
            self.define("CMAKE_CXX_COMPILER", self.spec["mpi"].mpicxx),
            self.define_from_variant("ADD_UNDERSCORE", "add_underscore"),
            self.define_from_variant("ENABLE_PEXSI", "enable_pexsi"),
            self.define_from_variant("ENABLE_SIPS", "enable_sips"),
            self.define_from_variant("ENABLE_DLAF", "dlaf"),
            self.define_from_variant("USE_EXTERNAL_ELPA", "use_external_elpa"),
            self.define_from_variant("USE_EXTERNAL_NTPOLY", "use_external_ntpoly"),
            self.define_from_variant("USE_EXTERNAL_OMM", "use_external_omm"),
            self.define_from_variant("USE_EXTERNAL_SUPERLU", "use_external_superlu"),
            self.define_from_variant("USE_EXTERNAL_PEXSI", "use_external_pexsi"),
            self.define_from_variant("USE_MPI_IALLGATHER", "use_mpi_iallgather"),
            self.define("ENABLE_TESTS", self.run_tests),
            self.define("ENABLE_C_TESTS", self.run_tests),
            self.define_from_variant("USE_GPU_CUDA", "cuda"),
            self.define("LIB_PATHS", ";".join(set(lib_paths))),
            self.define("LIBS", ";".join(set(libs))),
        ]

        if not self.spec.satisfies("+use_external_elpa"):
            args.append(
                self.define(f"USE_ELPA_{self.spec.variants['internal_elpa_version'].value}", True)
            )

        if self.spec.variants["elpa2_kernel"].value != "none":
            args.append(self.define_from_variant("ELPA2_KERNEL", "elpa2_kernel"))

        if self.spec.satisfies("^elpa+cuda"):
            elpa_gpu_string = "nvidia-gpu" if self.spec.satisfies("^elpa@2021:") else "gpu"
            args.append(self.define(ELSI_ELPA_GPU_STRING, elpa_gpu_string))

        args.append(self.define("INC_PATHS", ";".join(set(inc_paths))))

        # Only when using fujitsu compiler
        if self.spec.satisfies("%fj"):
            args.append(self.define("CMAKE_Fortran_MODDIR_FLAG", "-M"))

        return args
