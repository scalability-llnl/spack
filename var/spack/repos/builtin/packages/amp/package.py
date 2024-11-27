# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *
from spack.pkg.builtin.boost import Boost


class Amp(CMakePackage):
    """The Advanced Multi-Physics (AMP) package.

    The Advanced Multi-Physics (AMP) package is an open source parallel
    object-oriented computational framework that is designed with single
    and multi-domain multi-physics applications in mind.
    """

    homepage = "https://bitbucket.org/AdvancedMultiPhysics/amp"
    hg = homepage

    version("develop")

    variant("boost", default=True, description="Build with support for Boost")
    variant("hdf5", default=True, description="Build with support for HDF5")
    variant("hypre", default=True, description="Build with support for hypre")
    variant("libmesh", default=True, description="Build with libmesh support")
    variant("mpi", default=True, description="Build with MPI support")
    variant("netcdf", default=True, description="Build with NetCDF support")
    variant("petsc", default=True, description="Build with Petsc support")
    variant("shared", default=True, description="Build shared libraries")
    variant("silo", default=True, description="Build with support for Silo")
    variant("sundials", default=True, description="Build with support for Sundials")
    variant("trilinos", default=True, description="Build with support for Trilinos")
    variant("zlib", default=True, description="Build with support for zlib")

    # Everything should be compiled position independent (-fpic)
    depends_on("blas")
    depends_on("lapack")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="+boost")
    depends_on("hdf5", when="+hdf5")
    depends_on("hypre", when="+hypre")
    depends_on("libmesh", when="+libmesh")
    depends_on("netcdf-c", when="+netcdf")
    depends_on("petsc", when="+petsc")
    depends_on("silo", when="+silo")
    depends_on("sundials", when="+sundials")
    depends_on("trilinos", when="+trilinos")
    depends_on("zlib-api", when="+zlib")

    # MPI related dependencies
    depends_on("mpi", when="+mpi")

    def cmake_args(self):
        spec = self.spec

        options = [
            self.define("TPL_URL", "https://bitbucket.org/AdvancedMultiPhysics/tpl-builder"),
            self.define(
                "AMP_DATA_URL",
                "https://bitbucket.org/AdvancedMultiPhysics/amp/downloads/AMP-Data.tar.gz",
            ),
            self.define("AMP_ENABLE_TESTS", "OFF"),
            self.define("AMP_ENABLE_EXAMPLES", "OFF"),
            self.define("AMP_ENABLE_CXX11", "ON"),
            self.define("CXX_STD", "11"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("USE_MPI", "0"),
        ]

        if spec.satisfies("+mpi"):
            options.extend(
                [
                    self.define("CMAKE_C_COMPILER", spec["mpi"].mpicc),
                    self.define("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx),
                    self.define("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc),
                    self.define("MPI_COMPILER", "1"),
                    self.define("MPIEXEC", spec["mpi"].prefix.bin),
                ]
            )
        else:
            options.extend(
                [
                    self.define("CMAKE_C_COMPILER", self.compiler.cc),
                    self.define("CMAKE_CXX_COMPILER", self.compiler.cxx),
                    self.define("CMAKE_Fortran_COMPILER", self.compiler.fc),
                ]
            )

        tpl_list = ["LAPACK"]
        blas, lapack = spec["blas"].libs, spec["lapack"].libs
        options.extend(
            [
                self.define("TPL_LAPACK_INSTALL_DIR", spec["lapack"].prefix),
                self.define("TPL_BLAS_LIBRARY_NAMES", ";".join(blas.names)),
                self.define("TPL_BLAS_LIBRARY_DIRS", ";".join(blas.directories)),
                self.define("TPL_LAPACK_LIBRARY_NAMES", ";".join(lapack.names)),
                self.define("TPL_LAPACK_LIBRARY_DIRS", ";".join(lapack.directories)),
            ]
        )

        if spec.satisfies("+zlib"):
            tpl_list.append("ZLIB")
            options.append(self.define("TPL_ZLIB_INSTALL_DIR", spec["zlib-api"].prefix))

        for vname in (
            "boost",
            "hdf5",
            "hypre",
            "libmesh",
            "petsc",
            "silo",
            "sundials",
            "trilinos",
        ):
            if "+" + vname in spec:
                tpl_list.append(vname.upper())
                options.append(self.define(f"TPL_{vname.upper()}_INSTALL_DIR", spec[vname].prefix))

        if spec.satisfies("+netcdf"):
            tpl_list.append("NETCDF")
            options.append(self.define("TPL_NETCDF_INSTALL_DIR", spec["netcdf-c"].prefix))

        options.append(self.define("TPL_LIST", ";".join(tpl_list)))
        return options
