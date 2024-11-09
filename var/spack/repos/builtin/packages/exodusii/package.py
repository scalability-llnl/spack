# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.operating_systems.mac_os import macos_version
from spack.package import *

is_windows = sys.platform == "win32"


class Exodusii(CMakePackage):
    """Exodus II is a C++/Fortran library developed to store and retrieve
    data for finite element analyses. It's used for preprocessing
    (problem definition), postprocessing (results visualization), and
    data transfer between codes.  An Exodus II data file is a random
    access, machine independent, binary file that is written and read
    via C, C++, or Fortran API routines.  This package *only* installs
    the C and optionally Fortran library for exodus.  If you want the full
    suite of exodus-releated tools including the IOSS library, install
    the seacas package instead of this package.
    """

    homepage = "https://sandialabs.github.io/seacas/"
    git = "https://github.com/sandialabs/seacas.git"
    url = "https://github.com/sandialabs/seacas/archive/refs/tags/v2019-08-20.zip"
    maintainers("gsjaardema")

    license("BSD-3-Clause")

    version("master", branch="master")
    version(
        "2024-04-03", sha256="72b095bae64b2b6c232630f79de763c6ade00c9b1199fc6980800891b2ab3751"
    )
    version(
        "2024-03-11", sha256="5d417aa652e4ec8d66e27714c63b8cb5a7f878fb7b2ec55f629636fcff7c0f00"
    )
    version(
        "2023-11-27", sha256="00c444b2def2c9cf5694bee5bb0284ce289e83f7c84ac28c6701c746cfde9a4c"
    )
    version(
        "2023-05-30", sha256="d2cbd43596ed3ad77186f865fe8aa81a2efe389ff345b24622ac76c16614b532"
    )
    version(
        "2022-10-14", sha256="a96f29de3b69e7e3f5f344396c8cf791fe277dab0217fc0b90b02e38e75bbdc1"
    )
    version(
        "2022-08-01", sha256="c12a677ba2178cf5161d63fef3b1da4d3888622199cea3e611f59649085681dc"
    )
    version(
        "2022-05-16", sha256="80f6b0dee91766ab207a366b8eea546cc1afa33cea24deebaa6583f283d80fab"
    )
    version(
        "2022-03-04", sha256="b2e09f0f64d75634b7d3f9844c2cea7acbc877c4ceebb6b91e8e494bb3653166"
    )
    version(
        "2022-02-16", sha256="e1907f6831d9a0dd2c65879ca5746b9a0ef57d7ccce0036d55c0c6c5628ac981"
    )
    version(
        "2022-01-27", sha256="d21c14b9b30f773cef8e2029773f3cc35da021eebe9060298231f95021eb814f"
    )
    version(
        "2021-10-11",
        sha256="5c04d252e1c4a10b037aa352b89487e581ec6b52bdb46e9e85f101bbdcd9c388",
        deprecated=True,
    )
    version(
        "2021-04-05",
        sha256="f40d318674753287b8b28d2b4e5cca872cd772d4c7383af4a8f3eeb48fcc7ec0",
        deprecated=True,
    )
    version(
        "2021-04-02",
        sha256="811037a68eaff0daf9f34bd31b2ab1c9b8f028dfcb998ab01fbcb80d9458257c",
        deprecated=True,
    )
    version(
        "2021-01-20",
        sha256="6ff7c3f0651138f2e2305b5270108ca45f96346a739b35a126a0a260c91cbe64",
        deprecated=True,
    )
    version(
        "2021-01-06",
        sha256="69cafef17d8e624c2d9871f3a281ff3690116a6f82162fe5c1507bb4ecd6a32a",
        deprecated=True,
    )
    version(
        "2020-08-13",
        sha256="5b128a8ad9b0a69cff4fe937828d6d1702f1fe8aa80d4751e6522939afe62957",
        deprecated=True,
    )
    version(
        "2020-05-12",
        sha256="0402facf6cf23d903d878fb924b5d57e9f279dead5b92cf986953a6b91a6e81f",
        deprecated=True,
    )
    version(
        "2020-03-16",
        sha256="ed1d42c8c657931ecd45367a465cf9c00255772d9cd0811fc9baacdb67fc71fa",
        deprecated=True,
    )
    version(
        "2020-01-16",
        sha256="db69dca25595e88a40c00db0ccf2afed1ecd6008ba30bb478a4e1c5dd61998b8",
        deprecated=True,
    )
    version(
        "2019-12-18",
        sha256="88a71de836aa26fd63756cf3ffbf3978612edc5b6c61fa8de32fe9d638007774",
        deprecated=True,
    )
    version(
        "2019-10-14",
        sha256="f143d90e8a7516d25979d1416e580dea638332db723f26ae94a712dfe4052e8f",
        deprecated=True,
    )
    version("2016-08-09", commit="2ffeb1bd39454ad5aa230e12969ce976f3d1c92b", deprecated=True)

    patch("Fix-ioss-tpl.patch", when="@2021-10-11:")

    # Build options
    variant("fortran", default=False, description="Compile with Fortran support")
    variant("shared", default=True, description="Enables the build of shared libraries")
    variant("mpi", default=True, description="Enables MPI parallelism.")
    variant("thread_safe", default=False, description="Enable thread-safe exodus library")

    depends_on("cmake@3.22:", when="@2023-10-24:", type="build")
    depends_on("cmake@3.17:", when="@:2023-05-30", type="build")
    depends_on("mpi", when="+mpi")

    # Always depends on netcdf-c
    depends_on("netcdf-c@4.8.0:+mpi+parallel-netcdf", when="+mpi")
    depends_on("netcdf-c@4.8.0:~mpi", when="~mpi")
    depends_on("hdf5+hl~mpi", when="~mpi")
    depends_on("hdf5+hl+mpi", when="+mpi")

    depends_on("python@3.0:")
    conflicts("+shared", when="platform=windows")

    def setup_run_environment(self, env):
        env.prepend_path("PYTHONPATH", self.prefix.lib)

    def cmake_args(self):
        spec = self.spec
        from_variant = self.define_from_variant
        define = self.define

        if self.spec.satisfies("@2022-10-14:"):
            project_name_base = "Seacas"
        else:
            project_name_base = "SEACASProj"

        options = []

        # #################### Base Settings #######################
        # Only want to enable the Exodus library.  If want anything else, use the seacas package.
        options.extend(
            [
                define(project_name_base + "_ENABLE_ALL_PACKAGES", False),
                define(project_name_base + "_ENABLE_ALL_OPTIONAL_PACKAGES", False),
                define(project_name_base + "_ENABLE_SECONDARY_TESTED_CODE", False),
                define(project_name_base + "_ENABLE_SEACASExodus", True),
                from_variant(project_name_base + "_ENABLE_SEACASExodus_for", "fortran"),
                from_variant(project_name_base + "_ENABLE_SEACASExoIIv2for32", "fortran"),
                define(project_name_base + "_HIDE_DEPRECATED_CODE", False),
                from_variant("CMAKE_INSTALL_RPATH_USE_LINK_PATH", "shared"),
                from_variant("BUILD_SHARED_LIBS", "shared"),
                from_variant("SEACASExodus_ENABLE_THREADSAFE", "thread_safe"),
                from_variant("TPL_ENABLE_Pthread", "thread_safe"),
                from_variant(project_name_base + "_ENABLE_Fortran", "fortran"),
            ]
        )
        if "~shared" in self.spec and not is_windows:
            options.append(self.define(project_name_base + "_EXTRA_LINK_FLAGS", "z;dl"))
        options.append(from_variant("TPL_ENABLE_MPI", "mpi"))
        if "+mpi" in spec and not is_windows:
            options.extend(
                [
                    define("CMAKE_C_COMPILER", spec["mpi"].mpicc),
                    define("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx),
                    define("MPI_BASE_DIR", spec["mpi"].prefix),
                ]
            )
            if self.spec.satisfies("+fortran"):
                options.append(define("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc))

        # ##################### Dependencies ##########################
        # Always need NetCDF-C
        options.extend(
            [define("TPL_ENABLE_Netcdf", True), define("NetCDF_ROOT", spec["netcdf-c"].prefix)]
        )

        # ################# RPath Handling ######################
        if sys.platform == "darwin" and macos_version() >= Version("10.12"):
            # use @rpath on Sierra due to limit of dynamic loader
            options.append(define("CMAKE_MACOSX_RPATH", True))
        else:
            options.append(define("CMAKE_INSTALL_NAME_DIR", self.prefix.lib))

        return options
