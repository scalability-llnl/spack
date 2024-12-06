# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Sw4lite(MakefilePackage, CudaPackage):
    """Sw4lite is a bare bone version of SW4 intended for testing
    performance optimizations in a few important numerical kernels of SW4."""

    tags = ["proxy-app", "ecp-proxy-app"]

    homepage = "https://geodynamics.org/cig/software/sw4"
    url = "https://github.com/geodynamics/sw4lite/archive/v1.0.zip"
    git = "https://github.com/geodynamics/sw4lite.git"

    version("develop", branch="master")
    version("1.1", sha256="34b5f7b56f9e40474c14abebcaa024192de018de6beb6dafee53d3db5b07c6d3")
    version("1.0", sha256="2ed7784fe0564b33879c280d3a8d54d963f2f45cd7f61215b8077fcc4ce8a608")

    variant("openmp", default=True, description="Build with OpenMP support")
    variant(
        "precision",
        default="double",
        values=("float", "double"),
        multi=False,
        description="Floating point precision",
    )
    variant("ckernel", default=False, description="C or Fortran kernel")

    depends_on("blas")
    depends_on("lapack")
    depends_on("mpi")

    parallel = False

    @property
    def build_targets(self):
        targets = []
        spec = self.spec

        if spec.variants["precision"].value == "double":
            cxxflags = ["-I../src", "-I../src/double"]
        else:
            cxxflags = ["-I../src", "-I../src/float"]
        cflags = []
        fflags = []

        if "+openmp" in self.spec:
            cflags.append("-DSW4_OPENMP")
            cflags.append(self.compiler.openmp_flag)
            cxxflags.append("-DSW4_OPENMP")
            cxxflags.append(self.compiler.openmp_flag)
            fflags.append(self.compiler.openmp_flag)

        if spec.variants["ckernel"].value is True:
            cxxflags.append("-DSW4_CROUTINES")
            targets.append("ckernel=yes")

        if "+cuda" in self.spec:
            targets.append("NVCC = {0}".format(self.spec["cuda"].prefix.bin.nvcc))
            targets.append("HOSTCOMP = {0}".format(spack_cxx))
            targets.append("MPIPATH= {0} ".format(self.spec["mpi"].prefix))
            targets.append("gpuarch= {0}".format(self.cuda_flags(cuda_arch)))
            targets.append("MPIINC = {0}".format(self.spec["mpi"].headers.directories[0]))

        targets.append("FC=" + spec["mpi"].mpifc)
        targets.append("CXX=" + spec["mpi"].mpicxx)

        targets.append("CFLAGS={0}".format(" ".join(cflags)))
        targets.append("CXXFLAGS={0}".format(" ".join(cxxflags)))
        targets.append("FFLAGS={0}".format(" ".join(fflags)))

        targets.append("EXTRA_CXX_FLAGS=")
        targets.append("EXTRA_FORT_FLAGS=")
        lapack_blas = spec["lapack"].libs + spec["blas"].libs
        if spec.satisfies("%gcc"):
            targets.append("EXTRA_LINK_FLAGS={0} -lgfortran".format(lapack_blas.ld_flags))
        elif spec.satisfies("%arm"):
            targets.append("EXTRA_LINK_FLAGS={0} -larmflang".format(lapack_blas.ld_flags))
        else:
            targets.append("EXTRA_LINK_FLAGS={0}".format(lapack_blas.ld_flags))

        return targets

    def build(self, spec, prefix):
        if "+cuda" in spec:
            make("-f", "Makefile.cuda", *self.build_targets)
        else:
            make("-f", "Makefile", *self.build_targets)

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("*/sw4lite", prefix.bin)
        install_tree("tests", prefix.tests)
