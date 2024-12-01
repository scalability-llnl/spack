# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Casacore(CMakePackage):
    """A suite of c++ libraries for radio astronomy data processing."""

    homepage = "https://github.com/casacore/casacore"
    url = "https://github.com/casacore/casacore/archive/refs/tags/v3.5.0.tar.gz"

    maintainers("mpokorny")

    license("LGPL-2.0-only")

    version("3.6.1", sha256="480d3340fa17e9ba67f18efbaff4bbb272a01d1f400d2295c0b6c86eb7abcf82")
    version("3.6.0", sha256="c88075aa73c2139b323b71a7f5d56cec5a6a0de649efd11e2d00ca033be5a0d7")
    version("3.5.0", sha256="63f1c8eff932b0fcbd38c598a5811e6e5397b72835b637d6f426105a183b3f91")
    version("3.4.0", sha256="31f02ad2e26f29bab4a47a2a69e049d7bc511084a0b8263360e6157356f92ae1")
    version("3.3.0", sha256="3a714644b908ef6e81489b792cc9b80f6d8267a275e15d38a42a6a5137d39d3d")
    version("3.2.1", sha256="f87ce81d2b42ec5401cff8317baeeb9a3b408b716bb791ef252ad97af6e235ad")
    version("3.2.0", sha256="ae5d3786cb6dfdd7ebc5eecc0c724ff02bbf6929720bc23be43a027978e79a5f")
    version("3.1.2", sha256="ac94f4246412eb45d503f1019cabe2bb04e3861e1f3254b832d9b1164ea5f281")
    version("3.1.1", sha256="85d2b17d856592fb206b17e0a344a29330650a4269c80b87f8abb3eaf3dadad4")
    version("3.1.0", sha256="a6adf2d77ad0d6f32995b1e297fd88d31ded9c3e0bb8f28966d7b35a969f7897")
    version("3.0.0", sha256="6f0e68fd77b5c96299f7583a03a53a90980ec347bff9dfb4c0abb0e2933e6bcb")
    version("2.4.1", sha256="58eccc875053b2c6fe44fe53b6463030ef169597ec29926936f18d27b5087d63")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    depends_on("cmake@3.7.1:", type="build")

    variant("adios2", default=False, description="Build ADIOS2 support")
    variant("dysco", default=True, when="@3.5.0:", description="Build Dysco storage manager")
    variant("fftpack", default=False, description="Build FFTPack")
    variant("hdf5", default=False, description="Build HDF5 support")
    variant("mpi", default=False, description="Use MPI for parallel I/O")
    variant("openmp", default=False, description="Build OpenMP support")
    variant("python", default=False, description="Build python support")
    variant("readline", default=True, description="Build readline support")
    variant("shared", default=True, description="Build shared libraries")
    variant("tablelocking", default=True, description="Enable table locking")
    variant("threads", default=True, description="Use mutex thread synchronization")

    # Force dependency on readline in v3.2 and earlier. Although the
    # presence of readline is tested in CMakeLists.txt, and casacore
    # can be built without it, there's no way to control that
    # dependency at build time; since many systems come with readline,
    # it's better to explicitly depend on it here always.
    depends_on("readline", when="@:3.2.0")
    depends_on("readline", when="+readline")
    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("blas")
    depends_on("lapack")
    depends_on("cfitsio")
    depends_on("wcslib@4.20:+cfitsio")
    depends_on("fftw@3.0.0: precision=float,double", when="@3.4.0:")
    depends_on("fftw@3.0.0: precision=float,double", when="~fftpack")
    depends_on("sofa-c", type="test")
    depends_on("hdf5", when="+hdf5")
    depends_on("adios2@2.6.0:", when="+adios2")
    depends_on("adios2+mpi", when="+adios2+mpi")
    depends_on("adios2~mpi", when="+adios2~mpi")
    depends_on("mpi", when="+mpi")
    depends_on("python@2.6:", when="@:3.5.0 +python")
    depends_on("python@3:", when="@3.6.0: +python")
    depends_on("boost +python", when="+python")
    depends_on("boost +system +filesystem", when="+dysco")
    depends_on("py-numpy@:1", when="@:3.6.0 +python")
    depends_on("py-numpy", when="@3.6.1: +python")
    depends_on("gsl", when="+dysco")

    conflicts("+tablelocking", when="+mpi")
    conflicts("~threads", when="+openmp")

    def cmake_args(self):
        args = []
        spec = self.spec

        args.append(self.define_from_variant("BUILD_DYSCO", "dysco"))
        args.append(self.define_from_variant("ENABLE_TABLELOCKING", "tablelocking"))
        args.append(self.define_from_variant("ENABLE_SHARED", "shared"))
        args.append(self.define_from_variant("USE_THREADS", "threads"))
        args.append(self.define_from_variant("USE_OPENMP", "openmp"))
        args.append(self.define_from_variant("USE_READLINE", "readline"))
        args.append(self.define_from_variant("USE_HDF5", "hdf5"))
        args.append(self.define_from_variant("USE_ADIOS2", "adios2"))
        args.append(self.define_from_variant("USE_MPI", "mpi"))
        args.append("-DPORTABLE=ON")  # let Spack determine arch build flags

        # fftw3 is required by casacore starting with v3.4.0, but the
        # old fftpack is still available. For v3.4.0 and later, we
        # always require FFTW3 dependency with the optional addition
        # of FFTPack. In older casacore versions, only one of FFTW3 or
        # FFTPack can be selected.
        if spec.satisfies("@3.4.0:"):
            if spec.satisfies("+fftpack"):
                args.append(self.define("BUILD_FFTPACK_DEPRECATED", True))
        else:
            args.append(self.define("USE_FFTW3", spec.satisfies("~fftpack")))

        # Python2 and Python3 binding
        if spec.satisfies("~python"):
            args.extend([self.define("BUILD_PYTHON", False), self.define("BUILD_PYTHON3", False)])
        elif spec.satisfies("^python@3.0.0:"):
            args.extend([self.define("BUILD_PYTHON", False), self.define("BUILD_PYTHON3", True)])
        else:
            args.extend([self.define("BUILD_PYTHON", True), self.define("BUILD_PYTHON3", False)])
        if spec.satisfies("@3.6.0:"):
            args.append(self.define("USE_PCH", True))

        # tests won't pass unless measures data are installed, which
        # we don't do in this package, and for which we don't yet
        # provide any way of specifying at build time
        #
        # args.append(self.define('BUILD_TESTING', self.run_tests))
        args.append(self.define("BUILD_TESTING", False))

        return args

    def patch(self):
        # Rely on CMake ability to find hdf5, available since CMake 3.7.X
        os.remove("cmake/FindHDF5.cmake")
