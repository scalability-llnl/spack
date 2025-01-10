# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Sw4(MakefilePackage):
    """This package builds SW4 with MPI, OpenMP, HDF5, FFTW, PROJ, and ZFP."""

    homepage = "https://github.com/geodynamics/sw4"
    git = "https://github.com/geodynamics/sw4.git"

    maintainers("houjun", "andersp")

    version("master", branch="master")
    version("developer", branch="developer")
    version("3.0", tag="v3.0", commit="13e6d431976f7fc49124c997bf87353aa7afd35e")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("openmp", default=True, description="build with OpenMP")
    variant("hdf5", default=True, description="build with HDF5")
    variant("proj", default=True, description="build with proj")
    variant("zfp", default=False, description="build with ZFP")
    variant("fftw", default=True, description="build with FFTW")

    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("proj", when="+proj")
    depends_on("hdf5+mpi", when="+hdf5")
    depends_on("fftw@3.0: +mpi", when="+fftw")
    depends_on("zfp", when="+zfp")
    depends_on("h5z-zfp@develop", when="+zfp")
    depends_on("python")
    depends_on("py-h5py")
    depends_on("llvm-openmp", when="%apple-clang +openmp")

    def edit(self, spec, prefix):
        os.environ["CXX"] = spec["mpi"].mpicxx
        os.environ["FC"] = spec["mpi"].mpifc
        os.environ["proj"] = "yes"
        os.environ["openmp"] = "yes"
        os.environ["hdf5"] = "yes"
        os.environ["zfp"] = "yes"
        os.environ["fftw"] = "yes"
        os.environ["SW4ROOT"] = spec["proj"].prefix
        os.environ["HDF5ROOT"] = spec["hdf5"].prefix
        os.environ["H5ZROOT"] = spec["h5z-zfp"].prefix
        os.environ["ZFPROOT"] = spec["zfp"].prefix
        os.environ["FFTWHOME"] = spec["fftw"].prefix
        os.environ["EXTRA_LINK_FLAGS"] = "-lstdc++ -lm -ldl "
        os.environ["EXTRA_LINK_FLAGS"] += spec["blas"].libs.ld_flags + " "
        os.environ["EXTRA_LINK_FLAGS"] += spec["blas"].libs.ld_flags + " "

        if "+openmp" in spec:
            if spec.satisfies("%apple-clang"):
                os.environ["EXTRA_LINK_FLAGS"] += spec["llvm-openmp"].libs.ld_flags + " "

        # From spack/trilinos
        if spec.satisfies("%gcc") or spec.satisfies("%clang") or spec.satisfies("%apple-clang"):
            fc = Executable(self.compiler.fc)
            libgfortran = fc("--print-file-name", "libgfortran." + dso_suffix, output=str).strip()
            if libgfortran == "libgfortran." + dso_suffix:
                libgfortran = fc("--print-file-name", "libgfortran.a", output=str).strip()
            os.environ["EXTRA_LINK_FLAGS"] += " -L{0} -lgfortran ".format(
                os.path.dirname(libgfortran)
            )

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("optimize_mp/sw4", prefix.bin)
        install_tree("pytest", prefix.test)
