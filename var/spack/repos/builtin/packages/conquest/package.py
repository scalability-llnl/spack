# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Conquest(MakefilePackage):
    """CONQUEST is a DFT code designed for large-scale calculations,
    with excellent parallelisation."""

    homepage = "http://www.order-n.org/"
    url = "https://github.com/OrderN/CONQUEST-release/releases/download/v1.2/CONQUEST-release-1.2.tar.gz"
    git = "https://github.com/OrderN/CONQUEST-release/"

    # notify when the package is updated.
    maintainers("davidbowler", "tkoskela", "ilectra")

    license("MIT")

    version("1.2", sha256="74d974f20ec15ff31d97cd42aae6dbe95288eedfa785896d5872b9ff44ee7ae2")
    version("1.1", sha256="772e058f073cccfee45521aa62bb13192ab07cb2979b6076ddbf21ba22f9ba5d")
    version("master", branch="master")
    version("develop", branch="develop")

    depends_on("fortran", type="build")  # generated

    depends_on("blas")
    depends_on("lapack")
    depends_on("scalapack")
    depends_on("fftw-api")
    depends_on("libxc@:5")
    depends_on("mpi")

    variant("openmp", default=False, description="Build with OpenMP support")
    variant(
        "mult_kern",
        default="default",
        values=[
            "default",
            "gemm",
            "ompDoii",
            "ompDoik",
            "ompDoji",
            "ompDojk",
            "ompGemm",
            "ompGemm_m",
            "ompTsk",
        ],
        description="Matrix multiplication kernel type",
    )

    build_directory = "src"

    # The SYSTEM variable is required above version 1.2.
    # Versions 1.2 and older should ignore it.
    @property
    def build_targets(self):
        if self.version > Version("1.2"):
            return ["SYSTEM = example", "Conquest"]
        else:
            return ["Conquest"]

    def edit(self, spec, prefix):
        fflags = "-O3 -fallow-argument-mismatch"
        ldflags = ""

        if self.spec.satisfies("+openmp"):
            fflags += " " + self.compiler.openmp_flag
            ldflags += " " + self.compiler.openmp_flag

        libxc = self.spec["libxc:fortran"]
        fflags += " " + libxc.headers.include_flags
        ldflags += " " + self.spec["scalapack"].libs.ld_flags

        lapack_ld = self.spec["lapack"].libs.ld_flags
        blas_ld = self.spec["blas"].libs.ld_flags
        fftw_ld = self.spec["fftw"].libs.ld_flags
        libxc_ld = self.spec["libxc"].libs.ld_flags

        # Starting from 1.3 there's automated logic in the Makefile that picks
        # from a list of possible files for system/compiler-specific definitions.
        # This is useful for manual builds, but since the spack will do its own
        # automation of compiler-specific flags, we will override it.
        if self.version > Version("1.2"):
            defs_file = FileFilter("./src/system/system.example.make")
        else:
            defs_file = FileFilter("./src/system.make")

        defs_file.filter(".*COMPFLAGS=.*", f"COMPFLAGS= {fflags}")
        defs_file.filter(".*LINKFLAGS=.*", f"LINKFLAGS= {ldflags}")
        defs_file.filter(".*BLAS=.*", f"BLAS= {lapack_ld} {blas_ld}")
        defs_file.filter(".*FFT_LIB=.*", f"FFT_LIB={fftw_ld}")
        defs_file.filter(".*XC_LIB=.*", f"XC_LIB={libxc_ld} -lxcf90 -lxc")

        if self.spec.satisfies("+openmp"):
            defs_file.filter("OMP_DUMMY = DUMMY", "OMP_DUMMY = ")

        if self.spec.variants["mult_kern"].value != "default":
            defs_file.filter(
                "MULT_KERN =.*", f"MULT_KERN = {self.spec.variants['mult_kern'].value}"
            )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("./bin/Conquest", prefix.bin)
        if self.version > Version("1.2"):
            install_tree("./benchmarks/", join_path(prefix, "benchmarks"))
