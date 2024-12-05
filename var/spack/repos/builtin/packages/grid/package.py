# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Grid(AutotoolsPackage):
    """Data parallel C++ mathematical object library."""

    homepage = "https://github.com/paboyle/Grid"
    url = "https://github.com/paboyle/Grid/archive/refs/tags/0.8.2.tar.gz"
    git = "https://github.com/paboyle/Grid.git"

    maintainers("giordano")

    license("GPL-2.0-only")

    version("develop", branch="develop")

    depends_on("cxx", type="build")  # generated

    variant(
        "comms",
        default="mpi",
        values=("none", "mpi", "mpi3", conditional("shmem", when="^cray-mpich")),
        description="Choose communication interface",
    )
    variant("fftw", default=True, description="Activate FFTW support")
    variant("lapack", default=False, description="Activate LAPACK support")
    variant("hdf5", default=False, description="Activate HDF5 support")
    variant("lime", default=False, description="Activate LIME support")
    variant("doxygen-doc", default=False, description="Build the documentation with doxygen")
    variant(
        "gen-simd-width",
        default="64",
        description="Size (in bytes) of the generic SIMD vector type",
    )
    variant(
        "rng",
        default="sitmo",
        values=("sitmo", "ranlux48", "mt19937"),
        multi=False,
        description="RNG setting",
    )
    variant("timers", default=True, description="System dependent high-resolution timers")
    variant("chroma", default=False, description="Chroma regression tests")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("gmp")
    depends_on("mpfr")
    depends_on("openssl")

    depends_on("mpi", when="comms=mpi")
    depends_on("cray-mpich", when="comms=shmem")
    depends_on("mpi@3:", when="comms=mpi3")

    depends_on("fftw-api@3", when="+fftw")

    depends_on("lapack", when="+lapack")

    depends_on("hdf5", when="+hdf5")

    depends_on("c-lime", when="+lime")

    depends_on("doxygen", type="build", when="+doxygen-doc")

    def autoreconf(self, spec, prefix):
        Executable("./bootstrap.sh")()

    def configure_args(self):
        spec = self.spec
        args = ["--with-gmp", "--with-mpfr"]

        if spec.satisfies("^intel-mkl"):
            if spec.satisfies("+fftw") or spec.satisfies("+lapack"):
                args.append("--enable-mkl")
        else:
            if spec.satisfies("+fftw"):
                args.append("--with-fftw={0}".format(self.spec["fftw-api"].prefix))
            if spec.satisfies("+lapack"):
                args.append("--enable-lapack={0}".format(self.spec["lapack"].prefix))
                # lapack is searched only as `-llapack`, so anything else
                # wouldn't be found, causing an error.
                args.append("LIBS={0}".format(self.spec["lapack"].libs.ld_flags))

        if "comms=none" not in spec:
            # The build system can easily get very confused about MPI support
            # and what linker to use.  In many case it'd end up building the
            # code with support for MPI but without using `mpicxx` or linking to
            # `-lmpi`, wreaking havoc.  Forcing `CXX` to be mpicxx should help.
            args.extend(["CC={0}".format(spec["mpi"].mpicc), "CXX={0}".format(spec["mpi"].mpicxx)])

        args += self.enable_or_disable("timers")
        args += self.enable_or_disable("chroma")
        args += self.enable_or_disable("doxygen-doc")

        if "avx512" in spec.target:
            args.append("--enable-simd=AVX512")
        elif "avx2" in spec.target:
            args.append("--enable-simd=AVX2")
        elif "avx" in spec.target:
            if "fma4" in spec.target:
                args.append("--enable-simd=AVXFMA4")
            elif "fma" in spec.target:
                args.append("--enable-simd=AVXFMA")
            else:
                args.append("--enable-simd=AVX")
        elif "sse4_2" in spec.target:
            args.append("--enable-simd=SSE4")
        elif spec.target == "a64fx":
            args.append("--enable-simd=A64FX")
        elif "neon" in spec.target:
            args.append("--enable-simd=NEONv8")
        else:
            args.extend(
                [
                    "--enable-simd=GEN",
                    "--enable-gen-simd-width={0}".format(spec.variants["gen-simd-width"].value),
                ]
            )

        args.append("--enable-comms={0}".format(spec.variants["comms"].value))
        args.append("--enable-rng={0}".format(spec.variants["rng"].value))

        return args
