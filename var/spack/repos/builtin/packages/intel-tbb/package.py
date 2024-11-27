# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import platform
import sys

import spack.build_systems.cmake
import spack.build_systems.makefile
from spack.package import *


class IntelTbb(CMakePackage, MakefilePackage):
    """Widely used C++ template library for task parallelism.
    Intel Threading Building Blocks (Intel TBB) lets you easily write parallel
    C++ programs that take full advantage of multicore performance, that are
    portable and composable, and that have future-proof scalability.
    """

    homepage = "https://www.threadingbuildingblocks.org/"
    url_prefix = "https://github.com/oneapi-src/oneTBB/"
    url = url_prefix + "archive/v2020.1.tar.gz"
    git = "https://github.com/oneapi-src/oneTBB.git"

    maintainers("rscohn2")

    # Note: when adding new versions, please check and update the
    # patches, filters and url_for_version() below as needed.

    license("Apache-2.0")

    version("master", branch="master")
    version("2021.12.0", sha256="c7bb7aa69c254d91b8f0041a71c5bcc3936acb64408a1719aec0b2b7639dd84f")
    version("2021.11.0", sha256="782ce0cab62df9ea125cdea253a50534862b563f1d85d4cda7ad4e77550ac363")
    version("2021.10.0", sha256="487023a955e5a3cc6d3a0d5f89179f9b6c0ae7222613a7185b0227ba0c83700b")
    version("2021.9.0", sha256="1ce48f34dada7837f510735ff1172f6e2c261b09460e3bf773b49791d247d24e")
    version("2021.8.0", sha256="eee380323bb7ce864355ed9431f85c43955faaae9e9bce35c62b372d7ffd9f8b")
    version("2021.7.0", sha256="2cae2a80cda7d45dc7c072e4295c675fff5ad8316691f26f40539f7e7e54c0cc")
    version("2021.6.0", sha256="4897dd106d573e9dacda8509ca5af1a0e008755bf9c383ef6777ac490223031f")
    version("2021.5.0", sha256="e5b57537c741400cf6134b428fc1689a649d7d38d9bb9c1b6d64f092ea28178a")
    version("2021.4.0", sha256="021796c7845e155e616f5ecda16daa606ebb4c6f90b996e5c08aebab7a8d3de3")
    version("2021.3.0", sha256="8f616561603695bbb83871875d2c6051ea28f8187dbe59299961369904d1d49e")
    version("2021.2.0", sha256="cee20b0a71d977416f3e3b4ec643ee4f38cedeb2a9ff015303431dd9d8d79854")
    version("2021.1.1", sha256="b182c73caaaabc44ddc5ad13113aca7e453af73c1690e4061f71dfe4935d74e8")
    version("2020.3", sha256="ebc4f6aa47972daed1f7bf71d100ae5bf6931c2e3144cf299c8cc7d041dca2f3")
    version("2020.2", sha256="4804320e1e6cbe3a5421997b52199e3c1a3829b2ecb6489641da4b8e32faf500")
    version("2020.1", sha256="7c96a150ed22bc3c6628bc3fef9ed475c00887b26d37bca61518d76a56510971")
    version("2020.0", sha256="57714f2d2cf33935db33cee93af57eb3ecd5a7bef40c1fb7ca4a41d79684b118")
    version("2019.9", sha256="3f5ea81b9caa195f1967a599036b473b2e7c347117330cda99b79cfcf5b77c84")
    version("2019.8", sha256="6b540118cbc79f9cbc06a35033c18156c21b84ab7b6cf56d773b168ad2b68566")
    version("2019.7", sha256="94847fc627ed081c63ea253e31f23645ed3671548106b095ce303d1da5d76275")
    version("2019.6", sha256="21cd496ac768560e70d35e5423878aa3bcf0285f7194be77935d8febf0b18f47")
    version("2019.5", sha256="abf9236e6ec9a3675fa59ab56c2192c7ab4f7096a82af118e8efa514b2541578")
    version("2019.4", sha256="673e540aba6e526b220cbeacc3e4ff7b19a8689a00d7a09a9dc94396d73b24df")
    version("2019.3", sha256="4cb6bde796ae056e7c29f31bfdc6cfd0cfe848925219e9c82a20f09158e81542")
    version("2019.2", sha256="3bbe21054bd5b593ef99d4dfe451432cbf1f6f9429cd0dd543e879ef7e4e3327")
    version("2019.1", sha256="e6fb8dd1a1ae834b4e5f4ae6c4c87a3362f81a3aaeddfa6325168c6cfee59391")
    version("2019", sha256="91f00308a4e431bd9632b439d516134d7084f1eb35f52b7c9b111b46bdfcf093")
    version("2018.6", sha256="0ebb5fc877871ef15f7395d6e3c86de4ffedb820dc336383a3ab71fc39426aa7")
    version("2018.5", sha256="b8dbab5aea2b70cf07844f86fa413e549e099aa3205b6a04059ca92ead93a372")
    version("2018.4", sha256="c973b41b6da3db10efa7e14ce64a850e3fbfbcc16374494a005bf994d53a770a")
    version("2018.3", sha256="e5f19d747f6adabfc7daf2cc0a1ddcfab0f26bc083d70ea0a63def4a9f3919c5")
    version("2018.2", sha256="733c4dba646573b8285b1923dc106f0d771725bea620baa3659c86ab9312a1f4")
    version("2018.1", sha256="a9f51e0d081fbdda441d0150e759c7562318d6d7bc5a0c9a9d8064217d4d8d8d")
    version("2018", sha256="d427c58a59863c5f9510fffb3d05cd1bcc7abb94cdde1613407559e88b1263ab")
    version("2017.8", sha256="227cc1a8329da67f9957285f0020ad4d73d9ce26cbf88614349b8b74bb189ae1")
    version("2017.7", sha256="f487243e5931e967479189ef75946f02e3bb666ea73dcc19ac2828edd5550746")
    version("2017.6", sha256="b0f40edd010b90ce2519c1cebfa6f33216a1828d4fba19291b5cd23bd7fe809b")
    version("2017.5", sha256="b785e7181317350f0bb20f7bffda20bdecde7e82b824d2e5eb6d408a3b9cbeaf")
    version("2017.4", sha256="9a70ae3068767bf8c530bf98b9bbc655e36e82a301b347f7de76f99f401df1dd")
    version("2017.3", sha256="230ed3ff32bb3e91df1f59e4a3a567bde02639d9970b7e87cee0421b4c0b0f23")
    version("2017.2", sha256="dd37c896f95ca2357e828c24c9c4a169c6a6b5c905b3862a6cab09474d164497")
    version("2017.1", sha256="9b5b36b6d0ed97a3a1711b9095e78aed79bc998957a4a6b3d8a7af063523f037")
    version("2017", sha256="470544b0f374987273cc12e7706353edba8f9547578291d45b5b29358d4e5e81")
    version("4.4.6", sha256="65101b3a0eda38320ec3e3603daa79c54e6a60fb59ed2959738eaf4ce6d17f0a")
    version("4.4.5", sha256="2e372703fe444442c77760229897f00bb4babff62f7d0861b3f2783883cb257e")
    version("4.4.4", sha256="3ed03838c4e368b78305b0561cac48d369919bb4d9d68edd4d8a3becd6f62f5c")
    version("4.4.3", sha256="f0ff2e3735c8057b792f29c96f4f7623c1e4c76abfeda88be48645b8338c0f00")
    version("4.4.2", sha256="1ab10e70354685cee3ddf614f3e291434cea86c8eb62031e025f4052278152ad")
    version("4.4.1", sha256="05737bf6dd220b31aad63d77ca59c742271f81b4cc6643aa6f93d37450ae32b5")
    version("4.4", sha256="93c74b6054c69c86fa49d0fce7c50061fc907cb198a7237b8dd058298fd40c0e")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    build_system(
        conditional("makefile", when="@:2020.3"),
        conditional("cmake", when="@2021:"),
        default="cmake",
    )

    provides("tbb")

    # Clang builds incorrectly determine GCC version which in turn incorrectly
    # causes a mismatch in C++ features resulting in a link error. This also
    # means that clang builds require a gcc compiler to work correctly (this
    # has always been the case).
    #
    #    See https://github.com/intel/tbb/pull/147 for details.
    #
    conflicts("%apple-clang", when="@:2019.6", msg="2019.7 or later required for clang")
    conflicts("%clang", when="@:2019.6", msg="2019.7 or later required for clang")

    conflicts("%gcc@6.1:", when="@:4.4.3", msg="4.4.4 or later required for GCC >= 6.1.")

    variant("shared", default=True, description="Builds a shared version of TBB libraries")

    variant(
        "cxxstd",
        default="default",
        values=("default", "98", "11", "14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant("tm", default=True, description="Enable use of transactional memory on x86")

    # Testing version ranges inside when clauses was fixed in e9ee9eaf.
    # See: #8957 and #13989.

    # Build and install CMake config files if we're new enough.
    # CMake support started in 2017.7.
    depends_on("cmake@3.1.0:", type="build", when="@2017.7:")

    depends_on("hwloc", when="@2021.1.1:")

    # Patch for pedantic warnings (#10836).  This was fixed in the TBB
    # source tree in 2019.6.
    patch("gcc_generic-pedantic-2019.patch", level=1, when="@2019.1:2019.5")
    patch("gcc_generic-pedantic-4.4.patch", level=1, when="@:2019.0")

    # Patch and conflicts for GCC 13 support (#1031).
    patch("gcc_13-2021-v2.patch", when="@2021.1:2021.9")
    conflicts("%gcc@13", when="@:2021.3")

    # Patch cmakeConfig.cmake.in to find the libraries where we install them.
    patch("tbb_cmakeConfig-2019.5.patch", level=0, when="@2019.5:2021.0")
    patch("tbb_cmakeConfig.patch", level=0, when="@2017.7:2019.4")

    # Restore the debug targets.
    patch("makefile-debug.patch", when="@2020:2021.0")

    # Some very old systems don't support transactional memory.
    patch("disable-tm.patch", when="~tm")

    # Add support for building on arm64 macOS,
    # also included in hombrew and already available upstream:
    # https://github.com/oneapi-src/oneTBB/pull/258
    # https://github.com/oneapi-src/oneTBB/commit/86f6dcdc17a8f5ef2382faaef860cfa5243984fe.patch?full_index=1
    patch("macos-arm64.patch", when="@:2021.0")

    # build older tbb with %oneapi
    patch("intel-tbb.2020.3-icx.patch", when="@2020.3 %oneapi")

    # Support for building with %nvhpc
    # 1) remove flags nvhpc compilers do not recognize
    patch("intel-tbb.nvhpc-remove-flags.2017.patch", when="@2017:2018.9 %nvhpc")
    patch("intel-tbb.nvhpc-remove-flags.2019.patch", when="@2019:2019.0 %nvhpc")
    patch("intel-tbb.nvhpc-remove-flags.2019.1.patch", when="@2019.1:2019.6 %nvhpc")
    patch("intel-tbb.nvhpc-remove-flags.2019.7.patch", when="@2019.7:2019.8 %nvhpc")
    # The 2019.9 patch below was tested successfully
    # on @2019.9, @2020.0, and @2020.3
    patch("intel-tbb.nvhpc-remove-flags.2019.9.patch", when="@2019.9: %nvhpc")
    # 2) Fix generation of version script tbb.def for ld (nvc++ -E
    # appears to produce more output than g++ -E which was causing problems)
    # The 2017 patch below was tested on @2017, @2017.8, @2018,
    # @2018.3, @2018.6, 2019, @2019.[1-9], and @2020.[0-3]
    patch("intel-tbb.nvhpc-version-script-fix.2017.patch", when="@2017 %nvhpc")

    # Version and tar file names:
    #  2020.0 --> v2020.0.tar.gz  starting with 2020
    #  2017.1 --> 2017_U1.tar.gz  starting with 2017
    #  2017   --> 2017.tar.gz
    #  4.4.6  --> 4.4.6.tar.gz
    #
    def url_for_version(self, version):
        url = self.url_prefix + "archive/{0}.tar.gz"
        if version[0] >= 2020:
            name = "v{0}".format(version)
        elif version[0] >= 2017 and len(version) > 1:
            name = "{0}_U{1}".format(version[0], version[1])
        else:
            name = "{0}".format(version)
        return url.format(name)

    @property
    def libs(self):
        shared = True if self.spec.satisfies("+shared") else False
        return find_libraries("libtbb*", root=self.prefix, shared=shared, recursive=True)


class SetupEnvironment:
    # We set OS here in case the user has it set to something else
    # that TBB doesn't expect.
    def setup_build_environment(self, env):
        env.set("OS", platform.system())


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder, SetupEnvironment):
    def cmake_args(self):
        spec = self.spec
        options = [
            self.define("CMAKE_HWLOC_2_INCLUDE_PATH", spec["hwloc"].prefix.include),
            self.define("CMAKE_HWLOC_2_LIBRARY_PATH", spec["hwloc"].libs),
            self.define("TBB_CPF", True),
            self.define("TBB_STRICT", False),
            self.define("TBB_TEST", False),
        ]
        if spec.variants["cxxstd"].value != "default":
            options.append(self.define("CMAKE_CXX_STANDARD", spec.variants["cxxstd"].value))
        return options

    @run_after("install")
    def install_pkgconfig(self):
        # pkg-config generation is introduced in May 5, 2021.
        # It must not be overwritten by spack-generated tbb.pc.
        # https://github.com/oneapi-src/oneTBB/commit/478de5b1887c928e52f029d706af6ea640a877be
        if self.spec.satisfies("@:2021.2.0"):
            mkdirp(self.prefix.lib.pkgconfig)

            with open(join_path(self.prefix.lib.pkgconfig, "tbb.pc"), "w") as f:
                f.write("prefix={0}\n".format(self.prefix))
                f.write("exec_prefix=${prefix}\n")
                f.write("libdir={0}\n".format(self.prefix.lib))
                f.write("includedir={0}\n".format(self.prefix.include))
                f.write("\n")
                f.write("Name: Threading Building Blocks\n")
                f.write("Description: Intel's parallelism library for C++\n")
                f.write("Version: {0}\n".format(self.spec.version))
                f.write("Cflags: -I${includedir}\n")
                f.write("Libs: -L${libdir} -ltbb -latomic\n")


class MakefileBuilder(spack.build_systems.makefile.MakefileBuilder, SetupEnvironment):
    def coerce_to_spack(self, tbb_build_subdir):
        for compiler in ["icc", "gcc", "clang"]:
            fs = glob.glob(join_path(tbb_build_subdir, "*.%s.inc" % compiler))
            for f in fs:
                lines = open(f).readlines()
                of = open(f, "w")
                for lin in lines:
                    if lin.strip().startswith("CPLUS ="):
                        of.write("# coerced to spack\n")
                        of.write("CPLUS = $(CXX)\n")
                    elif lin.strip().startswith("CONLY ="):
                        of.write("# coerced to spack\n")
                        of.write("CONLY = $(CC)\n")
                    else:
                        of.write(lin)

    def build(self, pkg, spec, prefix):
        # Deactivate use of RTM with GCC when on an OS with a very old
        # assembler.
        if (
            spec.satisfies("%gcc@4.8.0: os=rhel6")
            or spec.satisfies("%gcc@4.8.0: os=centos6")
            or spec.satisfies("%gcc@4.8.0: os=scientific6")
        ):
            filter_file(r"RTM_KEY.*=.*rtm.*", "RTM_KEY =", join_path("build", "linux.gcc.inc"))

        # We need to follow TBB's compiler selection logic to get the proper
        # build + link flags but we still need to use spack's compiler wrappers
        # to accomplish this, we do two things:
        #
        # * Look at the spack spec to determine which compiler we should pass
        #   to tbb's Makefile;
        #
        # * patch tbb's build system to use the compiler wrappers (CC, CXX) for
        #   icc, gcc, clang (see coerce_to_spack());
        #
        self.coerce_to_spack("build")

        if spec.satisfies("%clang") or spec.satisfies("%apple-clang") or spec.satisfies("%rocmcc"):
            tbb_compiler = "clang"
        elif spec.satisfies("%intel"):
            tbb_compiler = "icc"
        else:
            tbb_compiler = "gcc"

        make_opts = []

        # Static builds of TBB are enabled by including 'big_iron.inc' file
        # See caveats in 'big_iron.inc' for limits on using TBB statically
        # Lore states this file must be handed to make before other options
        if "+shared" not in self.spec:
            make_opts.append("extra_inc=big_iron.inc")

        if spec.variants["cxxstd"].value != "default":
            make_opts.append("stdver=c++{0}".format(spec.variants["cxxstd"].value))

        #
        # tbb does not have a configure script or make install target
        # we simply call make, and try to put the pieces together
        #
        make_opts.append("compiler={0}".format(tbb_compiler))
        make(*make_opts)

    def install(self, pkg, spec, prefix):
        mkdirp(prefix)
        mkdirp(prefix.lib)

        # install headers to {prefix}/include
        install_tree("include", prefix.include)

        # install libs to {prefix}/lib
        tbb_lib_names = ["libtbb", "libtbbmalloc", "libtbbmalloc_proxy"]

        for lib_name in tbb_lib_names:
            # install release libs
            install(join_path("build", "*release", lib_name + ".*"), prefix.lib)
            # install debug libs if they exist
            install(join_path("build", "*debug", lib_name + "_debug.*"), prefix.lib)

        if spec.satisfies("@2017.8,2018.1:"):
            # Generate and install the CMake Config file.
            with working_dir(join_path(self.stage.source_path, "cmake")):
                cmake(
                    f"-DTBB_ROOT={prefix}",
                    f"-DTBB_OS={platform.system()}",
                    "-P",
                    "tbb_config_generator.cmake",
                )

    @run_after("install")
    def darwin_fix(self):
        # Replace @rpath in ids with full path
        if sys.platform == "darwin":
            fix_darwin_install_name(self.prefix.lib)
