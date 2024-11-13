# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *

is_windows = sys.platform == "win32"


class Cgns(CMakePackage):
    """The CFD General Notation System (CGNS) provides a general, portable,
    and extensible standard for the storage and retrieval of computational
    fluid dynamics (CFD) analysis data."""

    homepage = "https://cgns.github.io/"
    url = "https://github.com/CGNS/CGNS/archive/v4.3.0.tar.gz"
    git = "https://github.com/CGNS/CGNS"
    maintainers("gsjaardema")

    parallel = False

    license("Zlib")

    version("develop", branch="develop")
    version("master", branch="master")
    version("4.4.0", sha256="3b0615d1e6b566aa8772616ba5fd9ca4eca1a600720e36eadd914be348925fe2")
    version("4.3.0", sha256="7709eb7d99731dea0dd1eff183f109eaef8d9556624e3fbc34dc5177afc0a032")
    version("4.2.0", sha256="090ec6cb0916d90c16790183fc7c2bd2bd7e9a5e3764b36c8196ba37bf1dc817")
    version("4.1.2", sha256="951653956f509b8a64040f1440c77f5ee0e6e2bf0a9eef1248d370f60a400050")
    version("4.1.1", sha256="055d345c3569df3ae832fb2611cd7e0bc61d56da41b2be1533407e949581e226")
    version("4.1.0", sha256="4674de1fac3c47998248725fd670377be497f568312c5903d1bb8090a3cf4da0")
    version("4.0.0", sha256="748585a8e52dff4d250d6b603e6b847d05498e4566aba2dc3d7a7d85c4d55849")
    version("3.4.1", sha256="d32595e7737b9332243bd3de1eb8c018a272f620f09b289dea8292eba1365994")
    version("3.4.0", sha256="6372196caf25b27d38cf6f056258cb0bdd45757f49d9c59372b6dbbddb1e05da")
    version("3.3.1", sha256="81093693b2e21a99c5640b82b267a495625b663d7b8125d5f1e9e7aaa1f8d469")
    version("3.3.0", sha256="8422c67994f8dc6a2f201523a14f6c7d7e16313bdd404c460c16079dbeafc662")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("hdf5", default=True, description="Enable HDF5 interface")
    variant("fortran", default=False, description="Enable Fortran interface")
    variant("base_scope", default=False, description="Enable base scope")
    variant("scoping", default=True, description="Enable scoping")
    variant("mpi", default=True, description="Enable parallel cgns")
    variant("int64", default=False, description="Build with 64-bit integers")
    variant("shared", default=True, description="Enable shared library")
    variant("static", default=False, description="Build static libraries")
    variant("testing", default=False, description="Build CGNS testing")
    variant("legacy", default=False, description="Enable legacy options")
    variant("mem_debug", default=False, description="Enable memory debugging option")
    variant("tools", default=False, description="Enable CGNS tools")
    variant("pic", default=False, description="Produce position-independent code")

    depends_on("cmake@3.12:", when="@4.3:", type="build")
    depends_on("cmake@3.8:", when="@4.2:", type="build")
    depends_on("cmake@2.8:", when="@:4.1", type="build")
    depends_on("hdf5~mpi", when="+hdf5~mpi")
    depends_on("hdf5+mpi", when="+hdf5+mpi")
    depends_on("mpi", when="+mpi")

    # cgnsview requires tk to run
    depends_on("tk", when="+tools", type=("build", "link", "run"))
    depends_on("tcl", when="+tools")
    depends_on("gl", when="+tools")
    depends_on("glu", when="+tools")
    depends_on("libxmu", when="+tools")
    depends_on("libsm", when="+tools")

    conflicts("~pic", when="+fortran", msg="+pic required when +fortran")

    # patch for error undefined reference to `matherr, see
    # https://bugs.gentoo.org/662210
    patch("no-matherr.patch", when="@:3.3.1 +tools")

    # patch for gcc14 due to using internal tk type/function,
    # copied from https://github.com/CGNS/CGNS/pull/757
    # (adjusted an include from tk-private/generic/tkInt.h to tkInt.h)
    patch("gcc14.patch", when="@:4.4.0 %gcc@14:")

    def cmake_args(self):
        spec = self.spec
        options = []

        options.extend(
            [
                self.define_from_variant("CGNS_ENABLE_FORTRAN", "fortran"),
                self.define_from_variant("CGNS_ENABLE_SCOPING", "scoping"),
                self.define_from_variant("CGNS_ENABLE_PARALLEL", "mpi"),
                "-DCGNS_ENABLE_TESTS:BOOL=OFF",
                self.define_from_variant("CGNS_BUILD_TESTING", "testing"),
                self.define_from_variant("CGNS_BUILD_CGNSTOOLS", "tools"),
                self.define_from_variant("CGNS_BUILD_SHARED", "shared"),
                self.define_from_variant("CGNS_BUILD_STATIC", "static"),
                self.define_from_variant("CGNS_ENABLE_BASE_SCOPE", "base_scope"),
                self.define_from_variant("CGNS_ENABLE_LEGACY", "legacy"),
                self.define_from_variant("CGNS_ENABLE_MEM_DEBUG", "mem_debug"),
                self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
                self.define_from_variant("CGNS_ENABLE_64BIT", "int64"),
            ]
        )

        if "+mpi" in spec and not is_windows:
            options.extend(
                [
                    "-DCMAKE_C_COMPILER=%s" % spec["mpi"].mpicc,
                    "-DCMAKE_CXX_COMPILER=%s" % spec["mpi"].mpicxx,
                ]
            )
            if spec.satisfies("+fortran"):
                options.append(self.define("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc))

        if spec.satisfies("+hdf5"):
            options.extend(
                [
                    "-DCGNS_ENABLE_HDF5:BOOL=ON",
                    "-DHDF5_NEED_ZLIB:BOOL=ON",
                    "-DHDF5_INCLUDE_DIR:PATH=%s" % spec["hdf5"].prefix.include,
                    "-DHDF5_LIBRARY_DIR:PATH=%s" % spec["hdf5"].prefix.lib,
                ]
            )
            if spec.satisfies("+mpi"):
                options.extend(["-DHDF5_NEED_MPI:BOOL=ON", "-DHDF5_ENABLE_PARALLEL:BOOL=ON"])
        else:
            options.extend(["-DCGNS_ENABLE_HDF5=OFF"])

        if self.version <= Version("3.3.1"):
            if sys.platform == "darwin":
                options.extend(["-DCMAKE_MACOSX_RPATH:BOOL=ON"])

        return options
