# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Med(CMakePackage):
    """The MED file format is a specialization of the HDF5 standard."""

    homepage = "https://docs.salome-platform.org/latest/dev/MEDCoupling/med-file.html"
    url = "https://files.salome-platform.org/Salome/other/med-3.2.0.tar.gz"

    maintainers("likask")

    license("LGPL-3.0-only")

    version(
        "5.0.0",
        sha256="267e76d0c67ec51c10e3199484ec1508baa8d5ed845c628adf660529dce7a3d4",
        url="https://files.salome-platform.org/Salome/medfile/med-5.0.0.tar.bz2",
    )
    version(
        "4.1.1",
        sha256="a082b705d1aafe95d3a231d12c57f0b71df554c253e190acca8d26fc775fb1e6",
        url="https://files.salome-platform.org/Salome/medfile/med-4.1.1.tar.gz",
    )
    # Older versions are no more available from the official provider
    version(
        "4.1.0",
        sha256="847db5d6fbc9ce6924cb4aea86362812c9a5ef6b9684377e4dd6879627651fce",
        deprecated=True,
    )
    version(
        "4.0.0",
        sha256="a474e90b5882ce69c5e9f66f6359c53b8b73eb448c5f631fa96e8cd2c14df004",
        deprecated=True,
    )
    version(
        "3.2.0",
        sha256="d52e9a1bdd10f31aa154c34a5799b48d4266dc6b4a5ee05a9ceda525f2c6c138",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("api23", default=True, description="Enable API2.3")
    variant("mpi", default=True, description="Enable MPI")
    variant("shared", default=False, description="Builds a shared version of the library")
    variant("fortran", default=False, description="Enable Fortran support")
    variant("doc", default=False, description="Install documentation")
    variant("python", default=False, description="Build Python bindings")

    depends_on("hdf5@:1.8.22", when="@3.2.0")
    depends_on("hdf5@1.10.2:1.10.7", when="@4")
    depends_on("hdf5@1.12.1:1.12", when="@5:")

    depends_on("hdf5~mpi", when="~mpi")
    depends_on("hdf5+mpi", when="+mpi")
    depends_on("mpi", when="+mpi")

    depends_on("doxygen", type="build", when="+doc")

    depends_on("swig", type="build", when="+python")
    depends_on("python", when="+python")
    conflicts("~shared", when="+python", msg="Python bindings require shared libraries")

    conflicts("@4.1.0", when="~shared", msg="Link error when static")

    # C++11 requires a space between literal and identifier
    patch("add_space.patch", when="@3.2.0")

    # Fix problem where CMake "could not find TARGET hdf5"
    # The patch only works with HDF5 shared library builds
    patch("med-4.1.0-hdf5-target.patch", when="@4.0.0:4.1.0")
    depends_on("hdf5+shared", when="@4.0.0:4.1.0")

    def patch(self):
        # resembles FindSalomeHDF5.patch as in salome-configuration
        # see https://cmake.org/cmake/help/latest/prop_tgt/IMPORTED_LINK_INTERFACE_LIBRARIES.html
        filter_file(
            "GET_PROPERTY(_lib_lst TARGET hdf5-shared PROPERTY IMPORTED_LINK_INTERFACE_LIBRARIES_NOCONFIG)",  # noqa: E501
            "#GET_PROPERTY(_lib_lst TARGET hdf5-shared PROPERTY IMPORTED_LINK_INTERFACE_LIBRARIES_NOCONFIG)",  # noqa: E501
            "config/cmake_files/FindMedfileHDF5.cmake",
            string=True,
        )

    def cmake_args(self):
        spec = self.spec

        options = [
            self.define("HDF5_ROOT_DIR", spec["hdf5"].prefix),
            self.define("MEDFILE_BUILD_TESTS", self.run_tests),
            self.define_from_variant("MEDFILE_BUILD_PYTHON", "python"),
            self.define_from_variant("MEDFILE_INSTALL_DOC", "doc"),
        ]
        if "~fortran" in spec:
            options.append("-DCMAKE_Fortran_COMPILER=")

        if "+api23" in spec:
            options.extend(
                [
                    "-DCMAKE_CXX_FLAGS:STRING=-DMED_API_23=1",
                    "-DCMAKE_C_FLAGS:STRING=-DMED_API_23=1",
                    "-DMED_API_23=1",
                ]
            )

        if "+shared" in spec:
            options.extend(["-DMEDFILE_BUILD_SHARED_LIBS=ON", "-DMEDFILE_BUILD_STATIC_LIBS=OFF"])
        else:
            options.extend(["-DMEDFILE_BUILD_SHARED_LIBS=OFF", "-DMEDFILE_BUILD_STATIC_LIBS=ON"])

        if "+mpi" in spec:
            options.extend(["-DMEDFILE_USE_MPI=YES", "-DMPI_ROOT_DIR=%s" % spec["mpi"].prefix])

        return options
