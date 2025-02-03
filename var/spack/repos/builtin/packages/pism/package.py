# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pism(CMakePackage):
    """Parallel Ice Sheet Model"""

    homepage = "https://www.pism.io"
    url = "https://github.com/pism/pism/archive/v2.1.1.tar.gz"
    git = "https://github.com/pism/pism.git"

    maintainers("citibeth")

    license("GPL-3.0-only")

    version("develop", branch="dev")
    version("2.1.1", sha256="be4ac3ac42abbcb4d23af5c35284e06333dff0797eb11fa9745a214033857ab0")
    version("2.0.7", sha256="cd1523fdccd5c261c68cfb1e84a044d014f2e892796b31c490109a5e56cc9edf")
    version("1.1.4", sha256="8ccb867af3b37e8d103351dadc1d7e77512e64379519fe8a2592668deb27bc44")
    version("0.7.x", branch="stable0.7")
    version("icebin", branch="efischer/dev")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("extra", default=False, description="Build extra executables (testing/verification)")
    variant("shared", default=True, description="Build shared Pism libraries")
    variant("python", default=False, description="Build python bindings", when="@1.1:")
    variant("icebin", default=False, description="Build classes needed by IceBin")
    variant(
        "proj",
        default=True,
        description="Use Proj to compute cell areas, " "longitudes, and latitudes.",
    )
    variant("parallel-netcdf4", default=False, description="Enables parallel NetCDF-4 I/O.")
    variant(
        "parallel-netcdf3",
        default=False,
        description="Enables parallel NetCDF-3 I/O using PnetCDF.",
    )
    variant("parallel-hdf5", default=False, description="Enables parallel HDF5 I/O.")
    # variant('tao', default=False,
    #         description='Use TAO in inverse solvers.')

    description = "Build PISM documentation (requires LaTeX and Doxygen)"
    variant("doc", default=False, description=description)

    variant("examples", default=False, description="Install examples directory")

    description = "Report errors through Everytrace (requires Everytrace)"
    variant("everytrace", default=False, description=description)

    patch("pism-petsc-3.18.diff", when="@1.1.4 ^petsc@3.18:")

    # CMake build options not transferred to Spack variants
    # (except from CMakeLists.txt)
    #
    # option (Pism_TEST_USING_VALGRIND "Add extra regression tests
    #         using valgrind" OFF)
    # mark_as_advanced (Pism_TEST_USING_VALGRIND)
    #
    # option (Pism_ADD_FPIC "Add -fPIC to C++ compiler flags
    #         (CMAKE_CXX_FLAGS). Try turning it off if it does not work." ON)
    # option (Pism_LINK_STATICALLY
    #         "Set CMake flags to try to ensure that everything is
    #         linked statically")
    # option (Pism_LOOK_FOR_LIBRARIES
    #         "Specifies whether PISM should look for libraries. (Disable
    #         this on Crays.)" ON)
    # option (Pism_USE_TR1
    #        "Use the std::tr1 namespace to access shared pointer
    #        definitions. Disable to get shared pointers from the std
    #        namespace (might be needed with some compilers)." ON)
    # option (Pism_USE_TAO "Use TAO in inverse solvers." OFF)

    depends_on("fftw")
    depends_on("gsl")
    depends_on("mpi")
    depends_on("netcdf-c")  # Only the C interface is used, no netcdf-cxx4
    depends_on("petsc@3.21:", when="@2.1.1:")
    depends_on("petsc@:3.20", when="@:2.0.7")
    depends_on("udunits")
    depends_on("proj")
    depends_on("everytrace", when="+everytrace")

    extends("python", when="+python")
    depends_on("python@2.7:2.8,3.3:", when="+python")
    depends_on("py-matplotlib", when="+python")
    depends_on("py-numpy", when="+python")

    def cmake_args(self):
        spec = self.spec

        return [
            "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
            "-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx,
            # Fortran not needed for PISM...
            # '-DCMAKE_Fortran_COMPILER=%s' % spec['mpi'].mpifc,
            self.define_from_variant("Pism_BUILD_EXTRA_EXECS", "extra"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("Pism_BUILD_PYTHON_BINDINGS", "python"),
            self.define_from_variant("Pism_BUILD_ICEBIN", "icebin"),
            self.define_from_variant("Pism_USE_PROJ", "proj"),
            self.define_from_variant("Pism_USE_PARALLEL_NETCDF4", "parallel-netcdf4"),
            self.define_from_variant("Pism_USE_PNETCDF", "parallel-netcdf3"),
            self.define_from_variant("Pism_USE_PARALLEL_HDF5", "parallel-hdf5"),
            self.define_from_variant("Pism_BUILD_PDFS", "doc"),
            self.define_from_variant("Pism_INSTALL_EXAMPLES", "examples"),
            self.define_from_variant("Pism_USE_EVERYTRACE", "everytrace"),
        ]
