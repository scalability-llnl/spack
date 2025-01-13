# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pathlib
import re
import sys

import spack.build_environment
from spack.build_systems.cmake import get_cmake_prefix_path
from spack.package import *


class Cmake(Package):
    """A cross-platform, open-source build system. CMake is a family of
    tools designed to build, test and package software.
    """

    homepage = "https://www.cmake.org"
    url = "https://github.com/Kitware/CMake/releases/download/v3.19.0/cmake-3.19.0.tar.gz"
    git = "https://gitlab.kitware.com/cmake/cmake.git"

    maintainers("alalazo", "johnwparent")

    tags = ["build-tools", "windows"]

    executables = ["^cmake[0-9]*$"]

    license("BSD-3-Clause")

    version("master", branch="master")
    version("3.31.4", sha256="a6130bfe75f5ba5c73e672e34359f7c0a1931521957e8393a5c2922c8b0f7f25")
    version("3.31.3", sha256="fac45bc6d410b49b3113ab866074888d6c9e9dc81a141874446eb239ac38cb87")
    version("3.31.2", sha256="42abb3f48f37dbd739cdfeb19d3712db0c5935ed5c2aef6c340f9ae9114238a2")
    version("3.31.1", sha256="c4fc2a9bd0cd5f899ccb2fb81ec422e175090bc0de5d90e906dd453b53065719")
    version("3.31.0", sha256="300b71db6d69dcc1ab7c5aae61cbc1aa2778a3e00cbd918bc720203e311468c3")
    version("3.30.6", sha256="a7aa25cdd8545156fe0fec95ebbd53cb2b5173a8717e227f6e8a755185c168cf")
    version("3.30.5", sha256="9f55e1a40508f2f29b7e065fa08c29f82c402fa0402da839fffe64a25755a86d")
    version("3.30.4", sha256="c759c97274f1e7aaaafcb1f0d261f9de9bf3a5d6ecb7e2df616324a46fe704b2")
    version("3.30.3", sha256="6d5de15b6715091df7f5441007425264bdd477809f80333fdf95f846aaff88e4")
    version("3.30.2", sha256="46074c781eccebc433e98f0bbfa265ca3fd4381f245ca3b140e7711531d60db2")
    version("3.30.1", sha256="df9b3c53e3ce84c3c1b7c253e5ceff7d8d1f084ff0673d048f260e04ccb346e1")
    version("3.30.0", sha256="157e5be6055c154c34f580795fe5832f260246506d32954a971300ed7899f579")
    version("3.29.6", sha256="1391313003b83d48e2ab115a8b525a557f78d8c1544618b48d1d90184a10f0af")
    version("3.29.5", sha256="dd63da7d763c0db455ca232f2c443f5234fe0b11f8bd6958a81d29cc987dfd6e")
    version("3.29.4", sha256="b1b48d7100bdff0b46e8c8f6a3c86476dbe872c8df39c42b8d104298b3d56a2c")
    version("3.28.6", sha256="c39c733900affc4eb0e9688b4d1a45435a732105d9bf9cc1e75dd2b9b81a36bb")
    version("3.27.9", sha256="609a9b98572a6a5ea477f912cffb973109ed4d0a6a6b3f9e2353d2cdc048708e")
    version("3.26.6", sha256="070b9a2422e666d2c1437e2dab239a236e8a63622d0a8d0ffe9e389613d2b76a")
    version("3.25.3", sha256="cc995701d590ca6debc4245e9989939099ca52827dd46b5d3592f093afe1901c")
    version("3.24.4", sha256="32c9e499510eff7070d3f0adfbabe0afea2058608c5fa93e231beb49fbfa2296")
    version("3.23.5", sha256="f2944cde7a140b992ba5ccea2009a987a92413762250de22ebbace2319a0f47d")
    version("3.22.6", sha256="73933163670ea4ea95c231549007b0c7243282293506a2cf4443714826ad5ec3")
    version("3.21.7", sha256="3523c4a5afc61ac3d7c92835301cdf092129c9b672a6ee17e68c92e928c1375a")
    version("3.20.6", sha256="a0bd485e1a38dd13c0baec89d5f4adbf61c7fd32fddb38eabc69a75bc0b65d72")
    version("3.19.8", sha256="09b4fa4837aae55c75fb170f6a6e2b44818deba48335d1969deddfbb34e30369")
    version("3.18.6", sha256="124f571ab70332da97a173cb794dfa09a5b20ccbb80a08e56570a500f47b6600")
    version("3.17.5", sha256="8c3083d98fd93c1228d5e4e40dbff2dd88f4f7b73b9fa24a2938627b8bc28f1a")
    version("3.16.9", sha256="1708361827a5a0de37d55f5c9698004c035abb1de6120a376d5d59a81630191f")
    version("3.15.7", sha256="71999d8a14c9b51708847371250a61533439a7331eb7702ac105cfb3cb1be54b")
    version("3.14.7", sha256="9221993e0af3e6d10124d840ff24f5b2f3b884416fca04d3312cb0388dec1385")
    version("3.13.5", sha256="526db6a4b47772d1943b2f86de693e712f9dacf3d7c13b19197c9bef133766a5")
    version("3.12.4", sha256="5255584bfd043eb717562cff8942d472f1c0e4679c4941d84baadaa9b28e3194")
    version("3.11.4", sha256="8f864e9f78917de3e1483e256270daabc4a321741592c5b36af028e72bff87f5")
    version("3.10.3", sha256="0c3a1dcf0be03e40cf4f341dda79c96ffb6c35ae35f2f911845b72dab3559cf8")
    version("3.9.6", sha256="7410851a783a41b521214ad987bb534a7e4a65e059651a2514e6ebfc8f46b218")
    version("3.8.2", sha256="da3072794eb4c09f2d782fcee043847b99bb4cf8d4573978d9b2024214d6e92d")
    version("3.7.2", sha256="dc1246c4e6d168ea4d6e042cfba577c1acd65feea27e56f5ff37df920c30cae0")
    version("3.6.1", sha256="28ee98ec40427d41a45673847db7a905b59ce9243bb866eaf59dce0f58aaef11")
    version("3.5.2", sha256="92d8410d3d981bb881dfff2aed466da55a58d34c7390d50449aa59b32bb5e62a")
    version("3.4.3", sha256="b73f8c1029611df7ed81796bf5ca8ba0ef41c6761132340c73ffe42704f980fa")
    version("3.3.1", sha256="cd65022c6a0707f1c7112f99e9c981677fdd5518f7ddfa0f778d4cee7113e3d6")
    version("3.1.0", sha256="8bdc3fa3f2da81bc10c772a6b64cc9052acc2901d42e1e1b2588b40df224aad9")
    version("3.0.2", sha256="6b4ea61eadbbd9bec0ccb383c29d1f4496eacc121ef7acf37c7a24777805693e")
    version("2.8.10.2", sha256="ce524fb39da06ee6d47534bbcec6e0b50422e18b62abc4781a4ba72ea2910eb1")

    with default_args(deprecated=True):
        version(
            "3.29.3", sha256="252aee1448d49caa04954fd5e27d189dd51570557313e7b281636716a238bccb"
        )
        version(
            "3.29.2", sha256="36db4b6926aab741ba6e4b2ea2d99c9193222132308b4dc824d4123cb730352e"
        )
        version(
            "3.29.1", sha256="7fb02e8f57b62b39aa6b4cf71e820148ba1a23724888494735021e32ab0eefcc"
        )
        version(
            "3.29.0", sha256="a0669630aae7baa4a8228048bf30b622f9e9fd8ee8cedb941754e9e38686c778"
        )
        version(
            "3.28.4", sha256="eb9c787e078848dc493f4f83f8a4bbec857cd1f38ab6425ce8d2776a9f6aa6fb"
        )
        version(
            "3.28.3", sha256="72b7570e5c8593de6ac4ab433b73eab18c5fb328880460c86ce32608141ad5c1"
        )
        version(
            "3.28.2", sha256="1466f872dc1c226f373cf8fba4230ed216a8f108bd54b477b5ccdfd9ea2d124a"
        )
        version(
            "3.28.1", sha256="15e94f83e647f7d620a140a7a5da76349fc47a1bfed66d0f5cdee8e7344079ad"
        )
        version(
            "3.28.0", sha256="e1dcf9c817ae306e73a45c2ba6d280c65cf4ec00dd958eb144adaf117fb58e71"
        )
        # used in py-cmake, to be removed in Spack 0.23
        version(
            "3.22.2", sha256="3c1c478b9650b107d452c5bd545c72e2fad4e37c09b89a1984b9a2f46df6aced"
        )
        version(
            "3.21.4", sha256="d9570a95c215f4c9886dd0f0564ca4ef8d18c30750f157238ea12669c2985978"
        )
        version(
            "3.18.0", sha256="83b4ffcb9482a73961521d2bafe4a16df0168f03f56e6624c419c461e5317e29"
        )

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant(
        "build_type",
        default="Release",
        description="CMake build type",
        values=("Debug", "Release", "RelWithDebInfo", "MinSizeRel"),
    )

    # We default ownlibs to true because it greatly speeds up the CMake
    # build, and CMake is built frequently. Also, CMake is almost always
    # a build dependency, and its libs will not interfere with others in
    # the build.
    variant("ownlibs", default=True, description="Use CMake-provided third-party libraries")
    variant(
        "doc",
        default=False,
        description="Enables the generation of html and man page documentation",
    )
    variant(
        "ncurses",
        default=sys.platform != "win32",
        description="Enables the build of the ncurses gui",
    )
    variant("qtgui", default=False, description="Enables the build of the Qt GUI")

    # Revert the change that introduced a regression when parsing mpi link
    # flags, see: https://gitlab.kitware.com/cmake/cmake/issues/19516
    patch("cmake-revert-findmpi-link-flag-list.patch", when="@3.15.0")

    # Fix linker error when using external libs on darwin.
    # See https://gitlab.kitware.com/cmake/cmake/merge_requests/2873
    patch("cmake-macos-add-coreservices.patch", when="@3.11.0:3.13.3")

    # Fix builds with XLF + Ninja generator
    # https://gitlab.kitware.com/cmake/cmake/merge_requests/4075
    patch(
        "fix-xlf-ninja-mr-4075.patch",
        sha256="42d8b2163a2f37a745800ec13a96c08a3a20d5e67af51031e51f63313d0dedd1",
        when="@3.15.5",
    )

    # Statically linked binaries error on install when CMAKE_INSTALL_RPATH is set
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/9623
    patch("mr-9623.patch", when="@3.22.0:3.30")

    depends_on("ninja", when="platform=windows")
    depends_on("gmake", when="platform=linux")
    depends_on("gmake", when="platform=darwin")
    depends_on("gmake", when="platform=freebsd")

    depends_on("qt", when="+qtgui")
    # Qt depends on libmng, which is a CMake package;
    # ensure we build using a non CMake build system
    # when libmng is build as a transitive dependency of CMake
    for plat in ["linux", "darwin", "freebsd"]:
        with when(f"platform={plat}"):
            depends_on("libmng build_system=autotools", when="+qtgui")

    # See https://gitlab.kitware.com/cmake/cmake/-/issues/21135
    conflicts(
        "%gcc platform=darwin",
        when="@:3.17",
        msg="CMake <3.18 does not compile with GCC on macOS, "
        "please use %apple-clang or a newer CMake release. "
        "See: https://gitlab.kitware.com/cmake/cmake/-/issues/21135",
    )

    # Vendored dependencies do not build with nvhpc; it's also more
    # transparent to patch Spack's versions of CMake's dependencies.
    conflicts("+ownlibs %nvhpc")

    # Use Spack's curl even if +ownlibs, since that allows us to make use of
    # the conflicts on the curl package for TLS libs like OpenSSL.
    # In the past we let CMake build a vendored copy of curl, but had to
    # provide Spack's TLS libs anyways, which is not flexible, and actually
    # leads to issues where we have to keep track of the vendored curl version
    # and its conflicts with OpenSSL.
    depends_on("curl")

    # When using curl, cmake defaults to using system zlib too, probably because
    # curl already depends on zlib. Therefore, also unconditionaly depend on zlib.
    depends_on("zlib-api")

    with when("~ownlibs"):
        depends_on("expat")
        # expat/zlib are used in CMake/CTest, so why not require them in libarchive.
        for plat in ["darwin", "linux", "freebsd"]:
            with when("platform=%s" % plat):
                depends_on("libarchive@3.1.0: xar=expat compression=bz2lib,lzma,zlib,zstd")
                depends_on("libarchive@3.3.3:", when="@3.15.0:")
                depends_on("libuv@1.0.0:1.10", when="@3.7.0:3.10.3")
                depends_on("libuv@1.10.0:1.10", when="@3.11.0:3.11")
                depends_on("libuv@1.10.0:", when="@3.12.0:")
                depends_on("rhash", when="@3.8.0:")
                depends_on("jsoncpp build_system=meson", when="@3.2:")

    depends_on("ncurses", when="+ncurses")

    with when("+doc"):
        depends_on("python@2.7.11:", type="build")
        depends_on("py-sphinx", type="build")

    # Cannot build with Intel, should be fixed in 3.6.2
    # https://gitlab.kitware.com/cmake/cmake/issues/16226
    patch("intel-c-gnu11.patch", when="@3.6.0:3.6.1")

    # Cannot build with Intel again, should be fixed in 3.17.4 and 3.18.1
    # https://gitlab.kitware.com/cmake/cmake/-/issues/21013
    patch("intel-cxx-bootstrap.patch", when="@3.17.0:3.17.3,3.18.0")

    # https://gitlab.kitware.com/cmake/cmake/issues/18232
    patch("nag-response-files.patch", when="@3.7:3.12")

    # Cray libhugetlbfs and icpc warnings failing CXX tests
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/4698
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/4681
    patch("ignore_crayxc_warnings.patch", when="@3.7:3.17.2")

    # The Fujitsu compiler requires the '--linkfortran' option
    # to combine C++ and Fortran programs.
    patch("fujitsu_add_linker_option.patch", when="%fj")

    # Remove -A from the C++ flags we use when CXX_EXTENSIONS is OFF
    # Should be fixed in 3.19. This patch is needed also for nvhpc.
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/5025
    patch("pgi-cxx-ansi.patch", when="@3.15:3.18")

    # Adds CCE v11+ fortran preprocessing definition.
    # requires Cmake 3.19+
    # https://gitlab.kitware.com/cmake/cmake/-/merge_requests/5882
    patch(
        "5882-enable-cce-fortran-preprocessing.patch",
        sha256="b48396c0e4f61756248156b6cebe9bc0d7a22228639b47b5aa77c9330588ce88",
        when="@3.19.0:3.19",
    )

    # https://gitlab.kitware.com/cmake/cmake/issues/18166
    conflicts("%intel", when="@3.11.0:3.11.4")
    conflicts("%intel@:14", when="@3.14:", msg="Intel 14 has immature C++11 support")

    resource(
        name="cmake-bootstrap",
        url="https://cmake.org/files/v3.21/cmake-3.21.2-windows-x86_64.zip",
        checksum="213a4e6485b711cb0a48cbd97b10dfe161a46bfe37b8f3205f47e99ffec434d2",
        placement="cmake-bootstrap",
        when="@3.0.2: platform=windows",
    )

    resource(
        name="cmake-bootstrap",
        url="https://cmake.org/files/v2.8/cmake-2.8.4-win32-x86.zip",
        checksum="8b9b520f3372ce67e33d086421c1cb29a5826d0b9b074f44a8a0304e44cf88f3",
        placement="cmake-bootstrap",
        when="@:2.8.10.2 platform=windows",
    )

    phases = ["bootstrap", "build", "install"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"cmake.*version\s+(\S+)", output)
        return match.group(1) if match else None

    def flag_handler(self, name, flags):
        if name == "cxxflags" and self.compiler.name == "fj":
            cxx11plus_flags = (self.compiler.cxx11_flag, self.compiler.cxx14_flag)
            cxxpre11_flags = self.compiler.cxx98_flag
            if any(f in flags for f in cxxpre11_flags):
                raise ValueError("cannot build cmake pre-c++11 standard")
            elif not any(f in flags for f in cxx11plus_flags):
                flags.append(self.compiler.cxx11_flag)
        return (flags, None, None)

    def bootstrap_args(self):
        spec = self.spec
        args = []
        self.generator = make

        # The Intel compiler isn't able to deal with noinline member functions of
        # template classes defined in headers.  As such it outputs
        #   warning #2196: routine is both "inline" and "noinline"
        # cmake bootstrap will fail due to the word 'warning'.
        if spec.satisfies("%intel@:2021.6.0"):
            args.append("CXXFLAGS=-diag-disable=2196")

        if self.spec.satisfies("platform=windows"):
            args.append("-GNinja")
            self.generator = ninja

        if not sys.platform == "win32":
            args.append("--prefix={0}".format(self.prefix))

            jobs = spack.build_environment.get_effective_jobs(
                make_jobs,
                parallel=self.parallel,
                supports_jobserver=self.generator.supports_jobserver,
            )
            if jobs is not None:
                args.append("--parallel={0}".format(jobs))

            if spec.satisfies("+ownlibs"):
                # Build and link to the CMake-provided third-party libraries
                args.append("--no-system-libs")
            else:
                # Build and link to the Spack-installed third-party libraries
                args.append("--system-libs")

                # cppdap is a CMake package, avoid circular dependency
                if spec.satisfies("@3.27:"):
                    args.append("--no-system-cppdap")

            # Whatever +/~ownlibs, use system curl.
            args.append("--system-curl")

            if spec.satisfies("+doc"):
                args.append("--sphinx-html")
                args.append("--sphinx-man")

            if spec.satisfies("+qtgui"):
                args.append("--qt-gui")
            else:
                args.append("--no-qt-gui")

            # Now for CMake arguments to pass after the initial bootstrap
            args.append("--")
        else:
            args.append("-DCMAKE_INSTALL_PREFIX=%s" % self.prefix)

        # Make CMake find its own dependencies.
        prefixes = get_cmake_prefix_path(self)
        rpaths = [
            pathlib.Path(self.prefix, "lib").as_posix(),
            pathlib.Path(self.prefix, "lib64").as_posix(),
        ]

        args.extend(
            [
                f"-DCMAKE_BUILD_TYPE={self.spec.variants['build_type'].value}",
                # Install CMake correctly, even if `spack install` runs
                # inside a ctest environment
                "-DCMake_TEST_INSTALL=OFF",
                f"-DBUILD_CursesDialog={'ON' if '+ncurses' in spec else 'OFF'}",
                f"-DBUILD_QtDialog={'ON' if spec.satisfies('+qtgui') else 'OFF'}",
                "-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON",
                f"-DCMAKE_INSTALL_RPATH={';'.join(rpaths)}",
                f"-DCMAKE_PREFIX_PATH={';'.join(str(v) for v in prefixes)}",
            ]
        )

        return args

    def cmake_bootstrap(self):
        exe_prefix = self.stage.source_path
        relative_cmake_exe = os.path.join("cmake-bootstrap", "bin", "cmake.exe")
        return Executable(os.path.join(exe_prefix, relative_cmake_exe))

    def bootstrap(self, spec, prefix):
        bootstrap_args = self.bootstrap_args()
        if sys.platform == "win32":
            bootstrap = self.cmake_bootstrap()
            bootstrap_args.extend(["."])
        else:
            bootstrap = Executable("./bootstrap")
        bootstrap(*bootstrap_args)

    def build(self, spec, prefix):
        self.generator()

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        # Some tests fail, takes forever
        self.generator("test")

    def install(self, spec, prefix):
        self.generator("install")

        if spec.satisfies("%fj"):
            for f in find(self.prefix, "FindMPI.cmake", recursive=True):
                filter_file("mpcc_r)", "mpcc_r mpifcc)", f, string=True)
                filter_file("mpc++_r)", "mpc++_r mpiFCC)", f, string=True)
                filter_file("mpifc)", "mpifc mpifrt)", f, string=True)

    def setup_dependent_package(self, module, dependent_spec):
        """Called before cmake packages's install() methods."""

        module.cmake = Executable(self.spec.prefix.bin.cmake)
        module.ctest = Executable(self.spec.prefix.bin.ctest)

    @property
    def libs(self):
        """CMake has no libraries, so if you ask for `spec['cmake'].libs`
        (which happens automatically for packages that depend on CMake as
        a link dependency) the default implementation of ``.libs` will
        search the entire root prefix recursively before failing.

        The longer term solution is for all dependents of CMake to change
        their deptype. For now, this returns an empty set of libraries.
        """
        return LibraryList([])

    @property
    def headers(self):
        return HeaderList([])

    def run_version_check(self, bin):
        """Runs and checks output of the installed binary."""
        exe_path = join_path(self.prefix.bin, bin)
        if not os.path.exists(exe_path):
            raise SkipTest(f"{exe} is not installed")

        exe = which(exe_path)
        out = exe("--version", output=str.split, error=str.split)
        assert f"version {self.spec.version}" in out

    def test_ccmake(self):
        """check version from ccmake"""
        self.run_version_check("ccmake")

    def test_cmake(self):
        """check version from cmake"""
        self.run_version_check("cmake")

    def test_cpack(self):
        """check version from cpack"""
        self.run_version_check("cpack")

    def test_ctest(self):
        """check version from ctest"""
        self.run_version_check("ctest")
