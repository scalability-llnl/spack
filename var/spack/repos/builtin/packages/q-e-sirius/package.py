# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# adapted from official quantum espresso package


from spack.package import *


class QESirius(CMakePackage):
    """SIRIUS enabled fork of QuantumESPRESSO."""

    homepage = "https://github.com/electronic-structure/q-e-sirius/"
    url = "https://github.com/electronic-structure/q-e-sirius/archive/v6.5-rc4-sirius.tar.gz"
    git = "https://github.com/electronic-structure/q-e-sirius.git"

    maintainers("simonpintarelli")

    license("GPL-2.0-or-later")

    version("develop-ristretto", branch="ristretto", preferred=True, submodules=True)
    version(
        "6.7-rc1-sirius",
        tag="v6.7-rc1-sirius",
        commit="b1c79e30a2f9351316a90ca296f98cffef1f35c3",
        submodules=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("openmp", default=True, description="Enables OpenMP support")
    variant("libxc", default=False, description="Support functionals through libxc")
    variant("sirius_apps", default=False, description="Build SIRIUS standalone binaries")
    # Support for HDF5 has been added starting in QE 6.1.0 and is
    # still experimental
    variant(
        "hdf5",
        default="none",
        description="Orbital and density data I/O with HDF5",
        values=("parallel", "serial", "none"),
        multi=False,
    )

    depends_on("sirius +fortran")
    depends_on("sirius +apps", when="+sirius_apps")
    depends_on("sirius ~apps", when="~sirius_apps")
    depends_on("sirius +openmp", when="+openmp")
    depends_on("sirius@develop", when="@develop-ristretto")

    depends_on("mpi")
    depends_on("elpa", when="+elpa")
    depends_on("libxc", when="+libxc")
    depends_on("fftw-api@3")
    depends_on("blas")
    depends_on("lapack")
    depends_on("git", type="build")
    depends_on("pkgconfig", type="build")

    variant("scalapack", default=True, description="Enables scalapack support")

    with when("+scalapack"):
        depends_on("scalapack")
        variant("elpa", default=False, description="Uses elpa as an eigenvalue solver")

    # Versions of HDF5 prior to 1.8.16 lead to QE runtime errors
    depends_on("hdf5@1.8.16:+fortran+hl+mpi", when="hdf5=parallel")
    depends_on("hdf5@1.8.16:+fortran+hl~mpi", when="hdf5=serial")

    with when("+openmp"):
        depends_on("fftw+openmp", when="^[virtuals=fftw-api] fftw")
        depends_on("openblas threads=openmp", when="^[virtuals=blas] openblas")
        depends_on("intel-mkl threads=openmp", when="^[virtuals=blas] intel-mkl")

    def cmake_args(self):
        args = [
            "-DQE_ENABLE_SIRIUS=ON",
            "-DQE_ENABLE_CUDA=OFF",
            "-DQE_LAPACK_INTERNAL=OFF",
            "-DQE_ENABLE_DOC=OFF",
            "-DQE_ENABLE_MPI=ON",
            self.define_from_variant("QE_ENABLE_OPENMP", "openmp"),
            self.define_from_variant("QE_ENABLE_ELPA", "elpa"),
            self.define_from_variant("QE_ENABLE_LIBXC", "libxc"),
            self.define_from_variant("QE_ENABLE_SCALAPACK", "scalapack"),
        ]

        if not self.spec.satisfies("hdf5=none"):
            args.append(self.define("QE_ENABLE_HDF5", True))

        # Work around spack issue #19970 where spack sets
        # rpaths for MKL just during make, but cmake removes
        # them during make install.
        if self.spec["lapack"].name in INTEL_MATH_LIBRARIES:
            args.append("-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON")
        spec = self.spec
        args.append(self.define("BLAS_LIBRARIES", spec["blas"].libs.joined(";")))
        args.append(self.define("LAPACK_LIBRARIES", spec["lapack"].libs.joined(";")))

        return args
