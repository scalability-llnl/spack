# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Sw4(MakefilePackage):
    """SW4 implements substantial capabilities for 3-D seismic modeling."""

    homepage = "https://github.com/geodynamics/sw4"
    git = "https://github.com/geodynamics/sw4.git"

    maintainers("houjun", "andersp")

    license("GPL-2.0-or-later")

    version("master", branch="master")
    version("developer", branch="developer")
    version("3.0", tag="v3.0", commit="13e6d431976f7fc49124c997bf87353aa7afd35e")

    variant("openmp", default=True, description="Build with OpenMP")
    variant("proj", default=True, description="Build with PROJ")
    variant("hdf5", default=True, description="Build with HDF5")
    variant("zfp", default=False, when="+hdf5", description="Build with ZFP")
    variant("fftw", default=True, description="Build with FFTW")
    variant("debug", default=False, description="Build with debugging symbols")

    depends_on("cxx", type="build")
    depends_on("fortran", type="build")
    depends_on("mpi")
    depends_on("blas")
    depends_on("lapack")
    depends_on("python")
    depends_on("proj@9:", when="+proj")
    depends_on("hdf5@1.12: +mpi", when="+hdf5")
    depends_on("py-h5py", when="+hdf5")
    depends_on("zfp", when="+zfp")
    depends_on("h5z-zfp@develop", when="+zfp")
    depends_on("fftw@3: +mpi", when="+fftw")
    depends_on("llvm-openmp", when="%apple-clang +openmp")

    def edit(self, spec, prefix):
        os.environ["CXX"] = spec["mpi"].mpicxx
        os.environ["FC"] = spec["mpi"].mpifc
        # openmp is enabled by default
        if spec.satisfies("~openmp"):
            os.environ["openmp"] = "no"
        if spec.satisfies("+proj"):
            os.environ["proj"] = "yes"
            os.environ["SW4ROOT"] = spec["proj"].prefix
        if spec.satisfies("+hdf5"):
            os.environ["hdf5"] = "yes"
            os.environ["HDF5ROOT"] = spec["hdf5"].prefix
        if spec.satisfies("+zfp"):
            os.environ["zfp"] = "yes"
            os.environ["ZFPROOT"] = spec["zfp"].prefix
            os.environ["H5ZROOT"] = spec["h5z-zfp"].prefix
        if spec.satisfies("+fftw"):
            os.environ["fftw"] = "yes"
            os.environ["FFTWHOME"] = spec["fftw"].prefix
        if spec.satisfies("+debug"):
            os.environ["debug"] = "yes"
        os.environ["EXTRA_LINK_FLAGS"] = "-lstdc++ -lm -ldl "
        os.environ["EXTRA_LINK_FLAGS"] += spec["blas"].libs.ld_flags + " "
        os.environ["EXTRA_LINK_FLAGS"] += spec["lapack"].libs.ld_flags + " "
        if spec.satisfies("%apple-clang +openmp"):
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
        if spec.satisfies("+openmp~debug"):
            install("optimize_mp/sw4", prefix.bin)
        elif spec.satisfies("+openmp+debug"):
            install("debug_mp/sw4", prefix.bin)
        elif spec.satisfies("~openmp~debug"):
            install("optimize/sw4", prefix.bin)
        elif spec.satisfies("~openmp+debug"):
            install("debug/sw4", prefix.bin)
        install_tree("pytest", prefix.test)
