# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class NetcdfCxx4(CMakePackage):
    """NetCDF (network Common Data Form) is a set of software libraries and
    machine-independent data formats that support the creation, access, and
    sharing of array-oriented scientific data. This is the C++ distribution."""

    homepage = "https://www.unidata.ucar.edu/software/netcdf"
    url = "ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-cxx4-4.3.1.tar.gz"

    maintainers("WardF")

    license("Apache-2.0")

    version("4.3.1", sha256="6a1189a181eed043b5859e15d5c080c30d0e107406fbb212c8fb9814e90f3445")
    version("4.3.0", sha256="e34fbc6aba243ec82c23e9ee99db2430555ada849c54c1f3ab081b0ddd0f5f30")

    variant("shared", default=True, description="Enable shared library")
    variant("pic", default=True, description="Produce position-independent code (for shared libs)")
    variant("doc", default=False, description="Enable doxygen docs")
    variant("tests", default=False, description="Enable CTest-based tests, dashboards.")  # This looks to have unidata specific config

    depends_on("netcdf-c")
    depends_on('hdf5') # the cmake code path of netcdf-cxx4 has an explicit check on hdf5 so this needs to be a depend now
    depends_on('mpi',when='^hdf5+mpi')  # if we link against an mpi-aware hdf5 then this needs to also be mpi aware 
    depends_on("doxygen", when="+doc", type="build")

    filter_compiler_wrappers("ncxx4-config", relative_root="bin")

    def flag_handler(self, name, flags):
        if name == "cflags" and "+pic" in self.spec:
            flags.append(self.compiler.cc_pic_flag)
        if name == "cxxflags" and "+pic" in self.spec:
            flags.append(self.compiler.cxx_pic_flag)
        elif name == "ldlibs":
            # Address the underlinking problem reported in
            # https://github.com/Unidata/netcdf-cxx4/issues/86, which also
            # results into a linking error on macOS:
            flags.append(self.spec["netcdf-c"].libs.link_flags)

        # Note that cflags and cxxflags should be added by the compiler wrapper
        # and not on the command line to avoid overriding the default
        # compilation flags set by the configure script:
        return flags, None, None

    @property
    def libs(self):
        libraries = ["libnetcdf_c++4"]

        libs = find_libraries(libraries, root=self.prefix, shared=True if "+debug" in spec else False, recursive=True)

        if libs:
            return libs

        msg = "Unable to recursively locate {0} {1} libraries in {2}"
        raise spack.error.NoLibrariesError(
            msg.format("+shared" if self.spec else "static", self.spec.name, self.spec.prefix)
        )


    def patch(self):
        # An incorrect value is queried post find_package(HDF5)
        # This looks to be resolved in master, but not any of the tag releases
        # https://github.com/Unidata/netcdf-cxx4/issues/88
        filter_file(
               r"HDF5_C_LIBRARY_hdf5",
               "HDF5_C_LIBRARIES",
               join_path(self.stage.source_path,"CMakeLists.txt"))


    def cmake_args(self):

        args = [ 
                    self.define_from_variant('BUILD_SHARED_LIBS', "shared"),
                    self.define_from_variant('ENABLE_DOXYGEN', "doc"), 
                    self.define_from_variant('NCXX_ENABLE_TESTS', "tests"),
            ]

        return args


    def check(self):
        with working_dir(self.build_directory):
            make("check", parallel=False)
