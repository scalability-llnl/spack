# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class UfsWeatherModel(CMakePackage):
    """The Unified Forecast System (UFS) Weather Model (WM) is a prognostic
    model that can be used for short- and medium-range research and
    operational forecasts, as exemplified by its use in the operational Global
    Forecast System (GFS) of the National Oceanic and Atmospheric
    Administration (NOAA)."""

    homepage = "https://ufs-weather-model.readthedocs.io/en/latest/"
    url = "https://github.com/ufs-community/ufs-weather-model/archive/refs/tags/ufs-v1.1.0.tar.gz"
    git = "https://github.com/ufs-community/ufs-weather-model.git"

    maintainers("AlexanderRichert-NOAA")

    version("develop", branch="develop", submodules=True)
    version(
        "2.0.0",
        tag="ufs-v2.0.0",
        commit="e3cb92f1cd8941c019ee5ef7da5c9aef67d55cf8",
        submodules=True,
    )
    version(
        "1.1.0",
        tag="ufs-v1.1.0",
        commit="5bea16b6d41d810dc2e45cba0fa3841f45ea7c7a",
        submodules=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Enable MPI")
    variant(
        "32bit", default=True, description="Enable 32-bit single precision arithmetic in dycore"
    )
    variant(
        "ccpp_32bit",
        default=False,
        description="Enable CCPP_32BIT (single precision arithmetic in slow physics)",
    )
    variant("debug", default=False, description="Enable DEBUG mode", when="@develop")
    variant(
        "debug_linkmpi",
        default=True,
        description="Enable linkmpi option when DEBUG mode is on",
        when="@develop",
    )
    variant("inline_post", default=False, description="Enable inline post")
    variant("multi_gases", default=False, description="Enable multi gases in physics routines")
    variant("moving_nest", default=False, description="Enable moving nest code", when="@develop")
    variant("openmp", default=True, description="Enable OpenMP")
    variant("pdlib", default=False, description="Enable PDLIB (WW3)", when="@develop")
    variant("parallel_netcdf", default=True, description="Enable parallel NetCDF")
    variant(
        "jedi_driver",
        default=False,
        description="Enable JEDI as top level driver",
        when="@develop",
    )
    variant(
        "cmeps_aoflux",
        default=False,
        description="Enable atmosphere-ocean flux calculation in mediator",
        when="@develop",
    )
    variant(
        "ccpp",
        default=True,
        description="Enable the Common Community Physics Package (CCPP)",
        when="@:2.0.0",
    )
    variant(
        "ccpp_suites",
        default="FV3_GFS_v15p2,FV3_RRFS_v1alpha",
        description="CCPP suites to compile",
        values=("FV3_GFS_v15p2", "FV3_RRFS_v1alpha", "FV3_GFS_v15p2,FV3_RRFS_v1alpha"),
        multi=True,
        when="@:2.0.0",
    )
    dev_ccpp_default = [
        "FV3_GFS_v16",
        "FV3_GFS_v16_flake",
        "FV3_GFS_v17_p8",
        "FV3_GFS_v17_p8_rrtmgp",
        "FV3_GFS_v15_thompson_mynn_lam3km",
        "FV3_WoFS_v0",
        "FV3_GFS_v17_p8_mynn",
        "FV3_GFS_v17_p8_ugwpv1",
    ]
    variant(
        "ccpp_suites",
        default=",".join(dev_ccpp_default),
        description="CCPP suites to compile",
        multi=True,
        when="@develop",
    )
    variant(
        "quad_precision",
        default=False,
        description="Enable quad precision for certain grid metric terms in dycore",
        when="@:2.0.0",
    )
    variant("mom6solo", default=False, description="Build MOM6 solo executable", when="@develop")

    variant("app", default="ATM", description="UFS application", when="@develop")

    depends_on("bacio")
    depends_on("mpi", when="+mpi")
    depends_on("netcdf-c")
    depends_on("netcdf-fortran")
    depends_on("sp")
    depends_on("w3emc")
    depends_on("esmf@:8.0.0", when="@:2.0.0")
    depends_on("nemsio", when="@:2.0.0")
    depends_on("w3nco", when="@:2.0.0")
    depends_on("bacio@2.4.0:", when="@develop")
    depends_on("crtm", when="@develop")
    depends_on("esmf@8.3.0:", when="@develop")
    depends_on("fms@2022.04: +deprecated_io precision=32,64 constants=GFS", when="@develop")
    depends_on("g2", when="@develop")
    depends_on("g2tmpl", when="@develop")
    depends_on("hdf5+hl+mpi", when="@develop")
    depends_on("ip@:4", when="@develop")
    depends_on("netcdf-c~parallel-netcdf+mpi", when="@develop")
    for app in [
        "ATMW",
        "ATML",
        "NG-GODAS",
        "S2S",
        "S2SA",
        "S2SW",
        "S2SWA",
        "S2SWAL",
        "HAFS",
        "HAFSW",
        "HAFS-ALL",
        "LND",
    ]:
        depends_on("parallelio@2.5.3: +fortran~pnetcdf~shared", when="@develop app=%s" % app)
    depends_on("python@3.6:", type="build", when="@develop")
    depends_on("sp@2.3.3:", when="@develop")
    depends_on("w3emc@2.9.2:", when="@develop")

    with when("@develop app=S2SA"):
        depends_on("mapl")
        depends_on("gftl-shared")
    with when("@develop app=S2SWA"):
        depends_on("mapl")
        depends_on("gftl-shared")
    with when("@develop app=ATMAERO"):
        depends_on("mapl")
        depends_on("gftl-shared")
    depends_on("scotch", when="+pdlib")

    depends_on("w3nco", when="@:2.0.0")
    depends_on("python", type="build", when="@:2.0.0")

    conflicts("%gcc@:8", when="@develop")

    def setup_build_environment(self, env):
        spec = self.spec
        env.set("CC", spec["mpi"].mpicc)
        env.set("CXX", spec["mpi"].mpicxx)
        env.set("FC", spec["mpi"].mpifc)
        env.set("CMAKE_C_COMPILER", spec["mpi"].mpicc)
        env.set("CMAKE_CXX_COMPILER", spec["mpi"].mpicxx)
        env.set("CMAKE_Fortran_COMPILER", spec["mpi"].mpifc)

        env.set("CCPP_SUITES", ",".join([x for x in spec.variants["ccpp_suites"].value if x]))

        if spec.platform == "linux" and spec.satisfies("%intel"):
            env.set("CMAKE_Platform", "linux.intel")
        elif spec.platform == "linux" and spec.satisfies("%gcc"):
            env.set("CMAKE_Platform", "linux.gnu")
        elif spec.platform == "darwin" and spec.satisfies("%gcc"):
            env.set("CMAKE_Platform", "macosx.gnu")
        else:
            msg = "The host system {0} and compiler {0} "
            msg += "are not supported by UFS."
            raise InstallError(msg.format(spec.platform, self.compiler.name))

    def cmake_args(self):
        args = [
            self.define("AVX2", False),  # use target settings from Spack
            self.define("SIMDMULTIARCH", False),  # use target settings from Spack
            self.define_from_variant("CCPP_SUITES", "ccpp_suites").replace(";", ","),
        ]
        variants = [
            "32bit",
            "app",
            "ccpp_32bit",
            "cmeps_aoflux",
            "debug",
            "debug_linkmpi",
            "inline_post",
            "jedi_driver",
            "moving_nest",
            "mpi",
            "multi_gases",
            "openmp",
            "parallel_netcdf",
            "pdlib",
        ]
        for variant in variants:
            args.append(self.define_from_variant(variant.upper(), variant))

        if self.spec.satisfies("@:2.0.0"):
            args.append(self.define_from_variant("CCPP", "ccpp"))
            args.append(self.define_from_variant("QUAD_PRECISION", "quad_precision"))

        return args

    # This patch can be removed once https://github.com/NOAA-EMC/WW3/issues/1021
    # is resolved.
    @when("+pdlib ^scotch+shared")
    def patch(self):
        filter_file(r"(lib[^ ]+)\.a", r"\1.so", "WW3/cmake/FindSCOTCH.cmake")
        filter_file("STATIC", "SHARED", "WW3/cmake/FindSCOTCH.cmake")

    @run_after("install")
    def install_additional_files(self):
        mkdirp(prefix.bin)
        if self.spec.satisfies("@develop"):
            ufs_src = join_path(self.build_directory, "ufs_model")
        else:
            ufs_src = join_path(self.build_directory, "NEMS.exe")
        ufs_dst = join_path(prefix.bin, "ufs_weather_model")
        install(ufs_src, ufs_dst)
        set_executable(ufs_dst)
