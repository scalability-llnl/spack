# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Parallelio(CMakePackage):
    """The Parallel IO libraries (PIO) are high-level parallel I/O C and
    Fortran libraries for applications that need to do netCDF I/O from
    large numbers of processors on a HPC system."""

    homepage = "https://ncar.github.io/ParallelIO/"
    url = "https://github.com/NCAR/ParallelIO/archive/pio2_5_8.tar.gz"
    git = "https://github.com/NCAR/ParallelIO.git"

    maintainers("jedwards4b")

    license("Apache-2.0")

    version("2.6.2", sha256="c318894f0230197458917e932ec66301b4407a744df481e9c6a6d9d85f7e5ab1")
    version("2.6.1", sha256="83d3108d2b9db8219aa6b6ee333cfc12b2a588bcfc781587df5f8b24a716a6eb")
    version("2.6.0", sha256="e56a980c71c7f57f396a88beae08f1670d4adf59be6411cd573fe85868ef98c0")
    version("2.5.10", sha256="fac694827c81434a7766976711ba7179940e361e8ed0c189c7b397fd44d401de")
    version("2.5.9", sha256="e5dbc153d8637111de3a51a9655660bf15367d55842de78240dcfc024380553d")
    version("2.5.8", sha256="f2584fb4310ff7da39d51efbe3f334efd0ac53ae2995e5fc157decccc0570a89")
    version("2.5.7", sha256="af8af04e41af17f98f2c90b996ef0d8bcd980377e0b35e57b38938c7fdc87cbd")
    version("2.5.4", sha256="e51dc71683da808a714deddc1a80c2650ce847110383e42f1710f3ba567e7a65")
    version("2.5.3", sha256="205a0a128fd5262700efc230b3380dc5ab10e74bc5d273ae05db76c9d95487ca")
    version("2.5.2", sha256="935bc120ef3bf4fe09fb8bfdf788d05fb201a125d7346bf6b09e27ac3b5f345c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("pnetcdf", default=False, description="enable pnetcdf")
    variant("timing", default=False, description="enable GPTL timing")
    variant("ncint", default=False, description="enable netcdf integration", when="@2.6.0:")
    variant("shared", default=True, description="build shared libraries")
    variant("logging", default=False, description="enable verbose logging")
    variant(
        "fortran", default=True, description="enable fortran interface (requires netcdf fortran)"
    )
    variant("mpi", default=True, description="Use mpi to build, otherwise use mpi-serial")

    # This patch addresses building pio2.6.1 with serial netcdf, the issue is netcdf filters
    patch("serial261.patch", when="@2.6.1")
    patch("remove_redefinition_of_mpi_offset.patch", when="@:2.5.6")

    # This patch addresses an issue when compiling pio2.6.0 with a serial netcdf library.
    # netcdf4 filters are only available with the parallel build of netcdf.
    patch("pio_260.patch", when="@2.6.0")

    depends_on("cmake@3.7:", type="build")
    depends_on("mpi", when="+mpi")
    depends_on("mpi-serial", when="~mpi")
    depends_on("netcdf-c +mpi", type="link", when="+mpi")
    depends_on("netcdf-c ~mpi", type="link", when="~mpi")
    depends_on("netcdf-fortran", type="link", when="+fortran")
    depends_on("parallel-netcdf", type="link", when="+pnetcdf")

    resource(name="genf90", git="https://github.com/PARALLELIO/genf90.git", tag="genf90_200608")
    resource(
        name="CMake_Fortran_utils",
        git="https://github.com/CESM-Development/CMake_Fortran_utils.git",
        tag="CMake_Fortran_utils_150308",
    )

    # Allow argument mismatch in gfortran versions > 10 for mpi library compatibility
    patch("gfortran.patch", when="@:2.5.8 +fortran %gcc@10:")

    @run_after("install", when="platform=darwin")
    def darwin_install_name(self):
        # The shared library is not installed correctly on Darwin; fix this
        fix_darwin_install_name(self.prefix.lib)

    def cmake_args(self):
        define = self.define
        define_from_variant = self.define_from_variant
        spec = self.spec
        src = self.stage.source_path

        args = [
            define("NetCDF_C_PATH", spec["netcdf-c"].prefix),
            define("NetCDF_Fortran_PATH", spec["netcdf-fortran"].prefix),
            define("USER_CMAKE_MODULE_PATH", join_path(src, "CMake_Fortran_utils")),
            define("GENF90_PATH", join_path(src, "genf90")),
            define_from_variant("BUILD_SHARED_LIBS", "shared"),
            define("PIO_ENABLE_EXAMPLES", False),
        ]
        if spec.satisfies("+ncint"):
            args.extend([define("PIO_ENABLE_NETCDF_INTEGRATION", True)])
        if spec.satisfies("+pnetcdf"):
            args.extend([define("PnetCDF_C_PATH", spec["parallel-netcdf"].prefix)])
        if spec.satisfies("+fortran"):
            args.extend([define("NetCDF_Fortran_PATH", spec["netcdf-fortran"].prefix)])
        if spec.satisfies("+mpi"):
            env["CC"] = spec["mpi"].mpicc
            env["FC"] = spec["mpi"].mpifc
        else:
            env["FFLAGS"] = "-DNO_MPIMOD"
            args.extend(
                [
                    define("PIO_USE_MPISERIAL", True),
                    define("PIO_ENABLE_TESTS", False),
                    define("MPISERIAL_PATH", spec["mpi-serial"].prefix),
                ]
            )
        args.extend(
            [
                define_from_variant("PIO_ENABLE_TIMING", "timing"),
                define_from_variant("PIO_ENABLE_LOGGING", "logging"),
                define_from_variant("PIO_ENABLE_FORTRAN", "fortran"),
            ]
        )
        return args

    def url_for_version(self, version):
        return "https://github.com/NCAR/ParallelIO/archive/pio{0}.tar.gz".format(
            version.underscored
        )

    def setup_run_environment(self, env):
        env.set("PIO_VERSION_MAJOR", "2")
        valid_values = "netcdf"
        if self.spec.satisfies("+mpi"):
            valid_values += ",netcdf4p,netcdf4c"
            if self.spec.satisfies("+pnetcdf"):
                valid_values += ",pnetcdf"
        env.set("PIO_TYPENAME_VALID_VALUES", valid_values)
