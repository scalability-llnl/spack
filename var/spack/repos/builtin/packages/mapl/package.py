# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import subprocess

from spack.package import *


class Mapl(CMakePackage):
    """
    MAPL is a foundation layer of the GEOS architecture, whose
    original purpose is to supplement the Earth System Modeling
    Framework (ESMF).  MAPL fills in missing capabilities of ESMF,
    provides higher-level interfaces for common boiler-plate logic,
    and enforces various componentization conventions across ESMF
    gridded components within GEOS.

    """

    homepage = "https://github.com/GEOS-ESM/MAPL"
    url = "https://github.com/GEOS-ESM/MAPL/archive/refs/tags/v2.33.0.tar.gz"
    list_url = "https://github.com/GEOS-ESM/MAPL/tags"
    git = "https://github.com/GEOS-ESM/MAPL.git"

    maintainers(
        "mathomp4",
        "tclune",
        "climbfuji",
        "edwardhartnett",
        "Hang-Lei-NOAA",
        "AlexanderRichert-NOAA",
    )

    license("Apache-2.0")

    version("develop", branch="develop")
    version("main", branch="main")

    version("2.50.0", sha256="12282e547936f667f85c95d466273dcbaccbd600add72fa5981c0c734ccb1f7d")
    version("2.49.1", sha256="975e349c7ff8be65d4e63f2a6adf74ca96127628505dbce16c7ba7a3901edc70")
    version("2.49.0", sha256="fdf4d48bd38abd1059180b123c5d9fdc2781992c783244ddc51ab0f2ef63dd67")
    version("2.48.0", sha256="60a0fc4fd82b1a05050666ae478da7d79d86305aff1643a57bc09cb5347323b7")
    version("2.47.2", sha256="d4ca384bf249b755454cd486a26bae76944a7cae3a706b9a7c9298825077cac0")
    version("2.47.1", sha256="ca3e94c0caa78a91591fe63603d1836196f5294d4baad7cf1d83b229b3a85916")
    version("2.47.0", sha256="66c862d2ab8bcd6969e9728091dbca54f1f420e97e41424c4ba93ef606088459")
    version("2.46.4", sha256="f0c169254727d61bfc83beb3abd14f2562480c4cdbd2ad5bc1fe0419828a0ac2")
    version("2.46.3", sha256="333e1382ab744302d28b6f39e7f5504c7919d77d2443d70af952f60cbd8f27e7")
    version("2.46.2", sha256="6d397ad73042355967de8ef5b521d6135c004f96e93ae7b215f9ee325e75c6f0")
    version("2.46.1", sha256="f3090281de6293b484259d58f852c45b98759de8291d36a4950e6d348ece6573")
    version("2.46.0", sha256="726d9588b724bd43e5085d1a2f8d806d548f185ed6b22a1b13c0ed06212d7be2")
    # NOTE: Due to issues with CMake and ESMF, versions 2.44 and 2.45 of MAPL were not
    #       correctly installable with spack. The versions are still available in the
    #       repository, but we are skipping them in spack. There are references to these
    #       versions below in case a 2.44 or 2.45 spack-compatible version is needed
    #       and changes backported.
    version("2.43.2", sha256="966130931153a9a3974ad6ae011d1df194e057cb82301c8703ef69669b9f27ba")
    version("2.43.1", sha256="62b7a8c438c960e47b83d9835cb37c7ce25f617d648f2affe9961b4a6e638abc")
    version("2.43.0", sha256="1be99d64ca46001ac94f7db3607c345e144976dc34fe184e734e212bf3955d01")
    version("2.42.4", sha256="f6b643cc45f2dc55df96a316c84d84ace341bb6e06f81f83b5de258d9978b3d4")
    version("2.42.3", sha256="4ccac684dcbbca36cd7b30cb1515b52f05d7c06ca93399e60ccf42726d147018")
    version("2.42.2", sha256="cc70be57942a3d7f7a53d4762cb972cebcb9ae1737be7e03f195e4d4eefbc68a")
    version("2.42.1", sha256="78fdcc17f99f525feded05fc360f5b76e6f2c07057e0b16ce3177da2a534dc33")
    version("2.42.0", sha256="9b6c3434919c14ef79004db5f76cb3dd8ef375584227101c230a372bb0470fdd")
    version("2.41.2", sha256="73e1f0961f1b70e8159c0a2ce3499eb5158f3ca6d081f4c7826af7854ebfb44d")
    version("2.41.1", sha256="2b384bd4fbaac1bff4ef009922c436c4ab54832172a5cd4d312ea44e32c1ae7c")
    version("2.41.0", sha256="1142f9395e161174e3ec1654fba8bda1d0bd93edc7438b1927d8f5d7b42a0a86")
    version("2.40.5", sha256="85b4a4ac0d843398452808b88d7a5c29435aa37b69b91a1f4bee664e9f367b7d")
    version("2.40.4", sha256="fb843b118d6e56cd4fc4b114c4d6f91956d5c8b3d9389ada56da1dfdbc58904f")
    version("2.40.3", sha256="4b82a314c88a035fc2b91395750aa7950d6bee838786178ed16a3f39a1e45519")
    version("2.40.2", sha256="7327f6f5bce6e09e7f7b930013fba86ee7cbfe8ed4c7c087fc9ab5acbf6640fd")
    version("2.40.1", sha256="6f40f946fabea6ba73b0764092e495505d220455b191b4e454736a0a25ee058c")
    version("2.40.0", sha256="406bc63407ced3cd0cb147f203994fd4d14149fa3b909280ee1e0b2b549e732e")
    version("2.39.7", sha256="f0b02bf3dc1c77dba636f95020e4b858da03214711d3a50bc233df277698755a")
    version("2.39.6", sha256="3c1a838b445c5ae5c80d6912033495a9e696257c6113aead4a13755b6a242883")
    version("2.39.5", sha256="42afac883793cb0f2f40ed2c51bfc9f116803299168cbf055a83b33934d3f6c2")
    version("2.39.4", sha256="681842fda70f21e2b2743b3bf861ea2674862c322b885e69c6c2c926e0f5d09e")
    version("2.39.3", sha256="693310aea86bc3e00aaf3d7230eddee2ab0a994e6a55f857f780230e6b47c7d4")
    version("2.39.2", sha256="7a73a73b51852c988e89950a629201221261466d0b810c686423b7ced6ae491e")
    version("2.39.1", sha256="eef783622c8d69bcdcede427760d994906343c5b15a9f020ed45231e9a312192")
    version("2.39.0", sha256="c6ae4558597fe31c1efe18d9a8fc862a89656c88c02098a01fb40d38782e6fa3")
    version("2.38.1", sha256="4bff1077a12da2c63d7ee7b4dc829984dfbd4e84d357595933100a9fd8dd4028")
    version("2.38.0", sha256="bdfd46a348e776356c2cd0e776861dfa7a484a0075a7ee4066364452e4947e8b")
    version("2.37.3", sha256="48f8972605d7a6f4c75b4fe2b0d597c2269210ee6ca65513629891bea5f8e9a4")
    version("2.37.2", sha256="c156383a75b3b8cb57309e03683ae5ad8da7cd2701ee2a1d63226903d75b81bb")
    version("2.37.1", sha256="d68374d1cb8a8a0cc9c1fb018e8d1d81c9efa29c6ccaccc438023ec3461f83f2")
    version("2.37.0", sha256="ae53d58436d74fa40e3a5a743af9bcd6588a4590c0ef0a57c8317f4c7366b62b")
    version("2.36.0", sha256="0dc6c0e4240ae0db31cc0d58ed0f08f568b073710e5722b292bbe0e8ce9b6786")
    version("2.35.3", sha256="079b97a58f3728e5c9fa2a5dffb872496551a79c1cc544f215f2b0a63c708606")
    version("2.35.2", sha256="12d2c3fa264b702253e4792d858f67002fa04ce1c60db341803bc000abb3b7a2")
    version("2.34.3", sha256="8b750754cf5823771f2149d50f9aef585bcf194ca4635e1807c302d4020077e9")
    version("2.34.2", sha256="e46a763084027fe0f326d515e0648b814a82720948062405e03046531f7bb948")
    version("2.34.1", sha256="d2a504f08a4b416c3993d59630f226925bdaeb71488a1706decc49893dc8bcd0")
    version("2.34.0", sha256="4188df84654beed5c7fc3a96a3fb19289ebfc4020c4e14d52088d2ead2745f73")
    version("2.33.0", sha256="a36680d3186cd0399240e9739f5497310bac3f9563f55f77775acf53fa5491bb")
    version("2.32.0", sha256="f0eaec4b6d2514516a77cf426b656655d66f2e0801e639175dddfbd0648997f3")
    version("2.31.0", sha256="dcee4f0d02cc56c29437ab0dfc2f1ae78acce3af84630a55136f8e3626ce36c9")
    version("2.30.3", sha256="52bf65fcd5530079dab32ad1127fbaed940e218a99a89ac5bc8f8330b2094962")
    version("2.30.2", sha256="508b6d0e42593dbedbbb2524bafe7340be7306f80479fde2e4d55868a29753e7")
    version("2.30.1", sha256="df691ac12422184f05f37cb926541d18577ce129e0d6f10e91c90c3922bff572")
    version("2.30.0", sha256="71c469d4618ae97813f784208a102a38c4a30d5ff6301c08cb4fdbd1b1931202")
    version("2.29.0", sha256="aeca5258bc88526895715e3fd3604d43916b5143e948866fea4c1a608120598d")
    version("2.28.0", sha256="3a1f0c9b8b5a1932b2f036deb5463ddbef58a472ee4759c6cc3a4a871b8fe613")
    version("2.27.1", sha256="1aeca20b49729d0212bca764510cb069839d1f2b702c46c8b29a6b2535b2052c")
    version("2.27.0", sha256="a322257522f7fb2768668c02272ae8246ba4be81aa41d8015ce947ba871ce3fb")
    version("2.26.0", sha256="4ef9a1eeffc0521bd6fb4ea5ab261e07d3b5a46f0a6c43673ee169bf0d624bb8")
    version("2.25.0", sha256="f3ce71004f4274cedee28852cc105e0bf51a86cafc4d5f5af9de6492c4be9402")
    version("2.24.0", sha256="cd15ffd6897c18e64267e5fa86523402eb48cbf638ad5f3b4b5b0ff8939d1936")
    version("2.23.1", sha256="563f3e9f33adae298835e7de7a4a29452a2a584d191248c59494c49d3ee80d24")
    version("2.23.0", sha256="ae25ec63d0f288599c668f35fdbccc76abadbfc6d48f95b6eb4e7a2c0c69f241")
    version("2.22.0", sha256="3356b8d29813431d272c5464e265f3fe3ce1ac7f49ae6d41da34fe4b82aa691a")
    version(
        "2.12.3",
        sha256="e849eff291939509e74830f393cb2670c2cc96f6160d8060dbeb1742639c7d41",
        deprecated=True,
    )
    version(
        "2.11.0",
        sha256="76351e026c17e2044b89085db639e05ba0e7439a174d14181e01874f0f93db44",
        deprecated=True,
    )
    version(
        "2.8.1",
        sha256="a7657d4c52a66c3a6663e436d2c2dd4dbb81addd747e1ace68f59843665eb739",
        deprecated=True,
    )
    version(
        "2.8.0",
        sha256="6da60a21ab77ecebc80575f25b756c398ef48f635ab0b9c96932a1d4ebd8b4a0",
        deprecated=True,
    )
    version(
        "2.7.3",
        sha256="e8cdc0816471bb4c42673c2fa66d9d749f5a18944cd31580a2d6fd6d961ba163",
        deprecated=True,
    )
    version(
        "2.7.2",
        sha256="8f123352c665c434a18ff87304a71a61fb3342919adcccfea2a40729992d9f93",
        deprecated=True,
    )
    version(
        "2.7.1",
        sha256="8239fdbebd2caa47a232c24927f7a91196704e35c8b7909e1bbbefccf0647ea6",
        deprecated=True,
    )

    depends_on("c", type="build")
    depends_on("fortran", type="build")

    # Versions later than 3.14 remove FindESMF.cmake
    # from ESMA_CMake.
    resource(
        name="esma_cmake",
        git="https://github.com/GEOS-ESM/ESMA_cmake.git",
        tag="v3.51.0",
        when="@2.48:",
    )
    resource(
        name="esma_cmake",
        git="https://github.com/GEOS-ESM/ESMA_cmake.git",
        tag="v3.46.0",
        when="@2.47",
    )
    resource(
        name="esma_cmake",
        git="https://github.com/GEOS-ESM/ESMA_cmake.git",
        tag="v3.45.2",
        when="@2.45:2.46",
    )
    resource(
        name="esma_cmake",
        git="https://github.com/GEOS-ESM/ESMA_cmake.git",
        tag="v3.40.0",
        when="@2.44",
    )
    resource(
        name="esma_cmake",
        git="https://github.com/GEOS-ESM/ESMA_cmake.git",
        tag="v3.36.0",
        when="@2.42.0:2.43",
    )
    resource(
        name="esma_cmake",
        git="https://github.com/GEOS-ESM/ESMA_cmake.git",
        tag="v3.31.0",
        when="@2.40.0:2.41",
    )
    resource(
        name="esma_cmake",
        git="https://github.com/GEOS-ESM/ESMA_cmake.git",
        tag="v3.28.0",
        when="@2.36.0:2.39",
    )
    resource(
        name="esma_cmake",
        git="https://github.com/GEOS-ESM/ESMA_cmake.git",
        tag="v3.24.0",
        when="@2.34.0:2.35",
    )
    resource(
        name="esma_cmake",
        git="https://github.com/GEOS-ESM/ESMA_cmake.git",
        tag="v3.21.0",
        when="@2.22.0:2.33",
    )
    # NOTE: Remove this resource(), the patch() commands below
    # and the actual patches when MAPL 2.12 and older are deleted
    resource(
        name="esma_cmake",
        git="https://github.com/GEOS-ESM/ESMA_cmake.git",
        tag="v3.13.0",
        when="@:2.12.3",
    )

    # Patch to configure Apple M1 chip in x86_64 Rosetta 2 emulator mode
    # Needed for versions earlier than 3.14 of ESMA_cmake only.
    patch("esma_cmake_apple_m1_rosetta.patch", when="@:2.12.3")

    # Patch to add missing NetCDF C target in various CMakeLists.txt
    patch("mapl-2.12.3-netcdf-c.patch", when="@:2.12.3")

    # Patch to add missing MPI Fortran target to top-level CMakeLists.txt
    patch("mapl-2.12.3-mpi-fortran.patch", when="@:2.12.3")

    # MAPL only compiles with MPICH from version 2.42.0 and higher so we conflict
    # with older versions. Also, it's only been tested with MPICH 4, so we don't
    # allow older MPICH
    conflicts("mpich@:3")
    conflicts("mpich@4", when="@:2.41")

    # MAPL only supports gcc 13 from MAPL 2.45 onwards, so we only allow
    # builds with gcc 13 from that version onwards
    conflicts("%gcc@13:", when="@:2.44")

    variant("flap", default=False, description="Build with FLAP support", when="@:2.39")
    variant("pflogger", default=True, description="Build with pFlogger support")
    variant("fargparse", default=True, description="Build with fArgParse support")
    variant("shared", default=True, description="Build as shared library")
    variant("debug", default=False, description="Make a debuggable version of the library")
    variant("extdata2g", default=True, description="Use ExtData2G")
    variant("pfunit", default=False, description="Build with pFUnit support")
    variant("f2py", default=False, description="Build with f2py support")
    variant("zstd", default=True, description="Build with ZSTD support", when="@2.49:")

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release", "Aggressive"),
    )

    # https://github.com/JCSDA/spack-stack/issues/769
    conflicts("+pflogger", when="@:2.40.3 %intel@2021.7:")
    conflicts("+extdata2g", when="@:2.40.3 %intel@2021.7:")

    depends_on("cmake@3.23:", type="build", when="@2.50:")
    depends_on("cmake@3.17:", type="build", when="@:2.49")
    depends_on("mpi")
    depends_on("hdf5")
    depends_on("netcdf-c")
    depends_on("netcdf-c +zstd", when="+zstd")
    depends_on("netcdf-fortran")

    # ESMF dependency
    depends_on("esmf@8.6.1:", when="@2.45:")
    depends_on("esmf@8.6.0", when="@2.44")
    depends_on("esmf@8.5:", when="@2.40:2.43")
    depends_on("esmf@8.4", when="@2.34:2.39")
    depends_on("esmf@8.3", when="@2.22:2.33")
    depends_on("esmf", when="@:2.12.99")
    depends_on("esmf~debug", when="~debug")
    depends_on("esmf+debug", when="+debug")

    # udunits dependency from MAPL 2.48 onwards
    depends_on("udunits", when="@2.48:")

    # gFTL dependency
    depends_on("gftl@1.14.0:", when="@2.48:")
    depends_on("gftl@1.13.0:", when="@2.45:2.47")
    depends_on("gftl@1.11.0:", when="@2.44")
    depends_on("gftl@1.10.0:", when="@2.40:2.43")
    depends_on("gftl@1.5.5:1.9", when="@:2.39")

    # gFTL-Shared dependency
    depends_on("gftl-shared@1.9.0:", when="@2.48:")
    depends_on("gftl-shared@1.8.0:", when="@2.45:2.47")
    depends_on("gftl-shared@1.7.0:", when="@2.44")
    depends_on("gftl-shared@1.6.1:", when="@2.40:2.43")
    depends_on("gftl-shared@1.3.1:1.6.0", when="@:2.39")

    # yafyaml dependency
    # Note that MAPL 2.40+ no longer directly requires yafyaml as
    # extdata2g gets yaml support via esmf 8.5.0, but pflogger will
    # bring in yafyaml as a dependency.
    depends_on("yafyaml@1.0.4:", when="@2.23:2.39+extdata2g")
    depends_on("yafyaml@1.0-beta5", when="@:2.22+extdata2g")

    # pflogger dependency
    depends_on("pflogger@1.15.0: +mpi", when="@2.48:+pflogger")
    depends_on("pflogger@1.14.0: +mpi", when="@2.45:2.47+pflogger")
    depends_on("pflogger@1.11.0: +mpi", when="@2.44+pflogger")
    depends_on("pflogger@1.9.5: +mpi", when="@2.40:2.43+pflogger")
    depends_on("pflogger@1.9.1: +mpi", when="@2.23:2.39+pflogger")
    depends_on("pflogger@:1.6 +mpi", when="@:2.22+pflogger")

    # fargparse dependency
    depends_on("fargparse@1.8.0:", when="@2.48:+fargparse")
    depends_on("fargparse@1.7.0:", when="@2.45:2.47+fargparse")
    depends_on("fargparse@1.6.0:", when="@2.44+fargparse")
    depends_on("fargparse@1.5.0:", when="@2.40:43+fargparse")
    depends_on("fargparse@1.4.1:1.4", when="@:2.39+fargparse")

    # pfunit dependency
    depends_on("pfunit@4.10: +mpi +fhamcrest", when="@2.48:+pfunit")
    depends_on("pfunit@4.9: +mpi +fhamcrest", when="@2.45:2.47+pfunit")
    depends_on("pfunit@4.8: +mpi +fhamcrest", when="@2.44+pfunit")
    depends_on("pfunit@4.7.3: +mpi +fhamcrest", when="@2.40:+pfunit")
    depends_on("pfunit@4.6.1: +mpi +fhamcrest", when="@2.32:+pfunit")
    depends_on("pfunit@4.4.1: +mpi +fhamcrest", when="@2.26:+pfunit")
    depends_on("pfunit@4.2: +mpi +fhamcrest", when="@:2.25+pfunit")

    depends_on("flap", when="+flap")

    depends_on("ecbuild", type="build")

    depends_on("python@3:")
    depends_on("py-numpy", when="+f2py")
    depends_on("perl")

    # when using apple-clang version 15.x or newer, need to use the llvm-openmp library
    depends_on("llvm-openmp", when="%apple-clang@15:", type=("build", "run"))

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_WITH_PFLOGGER", "pflogger"),
            self.define_from_variant("BUILD_WITH_FARGPARSE", "fargparse"),
            self.define_from_variant("BUILD_SHARED_MAPL", "shared"),
            self.define_from_variant("USE_EXTDATA2G", "extdata2g"),
            self.define_from_variant("USE_F2PY", "f2py"),
        ]

        # We only want to add BUILD_WITH_FLAP if we are @:2.39 otherwise
        # there is a weird empty string that gets added to the CMake command
        if self.spec.satisfies("@:2.39"):
            args.append(self.define("BUILD_WITH_FLAP", self.spec.satisfies("+flap")))

        if self.spec.satisfies("@2.22.0:"):
            args.append(self.define("CMAKE_MODULE_PATH", self.spec["esmf"].prefix.cmake))

        # Compatibility flags for gfortran
        fflags = []
        if self.compiler.name in ["gcc", "clang", "apple-clang"]:
            fflags.append("-ffree-line-length-none")
            gfortran_major_ver = int(
                spack.compiler.get_compiler_version_output(self.compiler.fc, "-dumpversion").split(
                    "."
                )[0]
            )
            if gfortran_major_ver >= 10:
                fflags.append("-fallow-invalid-boz")
                fflags.append("-fallow-argument-mismatch")
        if fflags:
            args.append(self.define("CMAKE_Fortran_FLAGS", " ".join(fflags)))

        # Scripts often need to know the MPI stack used to setup the environment.
        # Normally, we can autodetect this, but building with Spack does not
        # seem to work. We need to pass in the MPI stack used to CMake
        # via -DMPI_STACK on the CMake command line. We use the following
        # names for the MPI stacks:
        #
        # - MPICH --> mpich
        # - Open MPI --> openmpi
        # - Intel MPI --> intelmpi
        # - MVAPICH --> mvapich
        # - HPE MPT --> mpt
        # - Cray MPICH --> mpich

        if self.spec.satisfies("^mpich"):
            args.append(self.define("MPI_STACK", "mpich"))
        elif self.spec.satisfies("^mvapich2"):
            args.append(self.define("MPI_STACK", "mvapich"))
        elif self.spec.satisfies("^openmpi"):
            args.append(self.define("MPI_STACK", "openmpi"))
        elif self.spec.satisfies("^intel-oneapi-mpi"):
            args.append(self.define("MPI_STACK", "intelmpi"))
        elif self.spec.satisfies("^mvapich"):
            args.append(self.define("MPI_STACK", "mvapich"))
        elif self.spec.satisfies("^mpt"):
            args.append(self.define("MPI_STACK", "mpt"))
        elif self.spec.satisfies("^cray-mpich"):
            args.append(self.define("MPI_STACK", "mpich"))
        else:
            raise InstallError("Unsupported MPI stack")

        return args

    def patch(self):
        if "~shared" in self.spec["netcdf-c"]:
            nc_pc_cmd = ["nc-config", "--static", "--libs"]
            nc_flags = subprocess.check_output(nc_pc_cmd, encoding="utf8").strip()
            filter_file(
                "(target_link_libraries[^)]+PUBLIC )", r"\1 %s " % nc_flags, "pfio/CMakeLists.txt"
            )

    def setup_build_environment(self, env):
        # esma_cmake, an internal dependency of mapl, is
        # looking for the cmake argument -DBASEDIR, and
        # if it doesn't find it, it's looking for an
        # environment variable with the same name. This
        # name is common and used all over the place,
        # and if it is set it breaks the mapl build.
        env.unset("BASEDIR")

    # We can run some tests to make sure the build is working
    # but we can only do it if the pfunit variant is enabled
    @when("+pfunit")
    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check(self):
        with working_dir(self.builder.build_directory):
            # The test suite contains a lot of tests. We select only those
            # that are cheap. Note this requires MPI and 6 processes
            ctest("--output-on-failure", "-L", "ESSENTIAL")
