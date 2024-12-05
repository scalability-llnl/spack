# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Xrootd(CMakePackage):
    """The XROOTD project aims at giving high performance, scalable fault
    tolerant access to data repositories of many kinds."""

    homepage = "https://xrootd.web.cern.ch"
    urls = [
        "https://xrootd.web.cern.ch/download/v5.7.0/xrootd-5.7.0.tar.gz",
        "https://github.com/xrootd/xrootd/releases/download/v5.7.0/xrootd-5.7.0.tar.gz",
    ]
    list_url = "https://xrootd.web.cern.ch/dload.html"
    git = "https://github.com/xrootd/xrootd.git"

    maintainers("gartung", "greenc-FNAL", "marcmengel", "vitodb", "wdconinc")

    license("LGPL-3.0-only")

    version("5.7.1", sha256="c28c9dc0a2f5d0134e803981be8b1e8b1c9a6ec13b49f5fa3040889b439f4041")
    version("5.7.0", sha256="214599bba98bc69875b82ac74f2d4b9ac8a554a1024119d8a9802b3d8b9986f8")
    version("5.6.9", sha256="44196167fbcf030d113e3749dfdecab934c43ec15e38e77481e29aac191ca3a8")
    version("5.6.8", sha256="19268fd9f0307d936da3598a5eb8471328e059c58f60d91d1ce7305ca0d57528")
    version("5.6.7", sha256="4089ce3a69fcf6566d320ef1f4a73a1d6332e6835b7566e17548569bdea78a8d")
    version("5.6.6", sha256="b265a75be750472561df9ff321dd0b2102bd64ca19451d312799f501edc597ba")
    version("5.6.5", sha256="600874e7c5cdb11d20d6bd6c549b04a3c5beb230d755829726cd15fab99073b1")
    version("5.6.4", sha256="52f041ab2eaa4bf7c6087a7246c3d5f90fbab0b0622b57c018b65f60bf677fad")
    version("5.6.3", sha256="72000835497f6337c3c6a13c6d39a51fa6a5f3a1ccd34214f2d92f7d47cc6b6c")
    version("5.6.2", sha256="7d7c262714268b92dbe370a9ae72275cc07f0cdbed400afd9989c366fed04c00")
    version("5.6.1", sha256="9afc48ab0fb3ba69611b1edc1b682a185d49b45caf197323eecd1146d705370c")
    version("5.6.0", sha256="cda0d32d29f94220be9b6627a80386eb33fac2dcc25c8104569eaa4ea3563009")
    version("5.5.5", sha256="0710caae527082e73d3bf8f9d1dffe95808afd3fcaaaa15ab0b937b8b226bc1f")
    version("5.5.4", sha256="41a8557ea2d118b1950282b17abea9230b252aa5ee1a5959173e2534b7d611d3")
    version("5.5.3", sha256="703829c2460204bd3c7ba8eaa23911c3c9a310f6d436211ba0af487ef7f6a980")
    version("5.5.2", sha256="ec4e0490b8ee6a3254a4ea4449342aa364bc95b78dc9a8669151be30353863c6")
    version("5.5.1", sha256="3556d5afcae20ed9a12c89229d515492f6c6f94f829a3d537f5880fcd2fa77e4")
    version("5.3.2", sha256="e8371fb9e86769bece74b9b9d67cb695023cd6a20a1199386fddd9ed840b0875")
    version("5.3.1", sha256="7ea3a112ae9d8915eb3a06616141e5a0ee366ce9a5e4d92407b846b37704ee98")
    version("5.1.0", sha256="c639536f1bdc5b6b365e807f3337ed2d41012cd3df608d40e91ed05f1c568b6d")
    version("5.0.3", sha256="be40a1897d6c1f153d3e23c39fe96e45063bfafc3cc073db88a1a9531db79ac5")
    version("5.0.1", sha256="ff4462b0b61db4cc01dda0e26abdd78e43649ee7ac5e90f7a05b74328ff5ac83")
    version("4.12.6", sha256="1a9056ab7aeeaafa586ea77e442960c71d233c9ba60c7f9db9262c1410954ac4")
    version("4.12.3", sha256="6f2ca1accc8d49d605706bb556777c753860bf46d845b1ee11393a5cb5987f15")
    version("4.12.2", sha256="29f7bc3ea51b9d5d310eabd177152245d4160223325933c67f938ed5120f67bb")
    version("4.12.1", sha256="7350d9196a26d17719b839fd242849e3995692fda25f242e67ac6ec907218d13")
    version("4.12.0", sha256="69ef4732256d9a88127de4bfdf96bbf73348e0c70ce1d756264871a0ffadd2fc")
    version("4.11.3", sha256="8e7a64fd55dfb452b6d5f76a9a97c493593943227b377623a3032da9197c7f65")
    version("4.11.2", sha256="4620824db97fcc37dc3dd26110da8e5c3aab1d8302e4921d4f32e83207060603")
    version("4.10.0", sha256="f07f85e27d72e9e8ff124173c7b53619aed8fcd36f9d6234c33f8f7fd511995b")
    version("4.8.5", sha256="42e4d2cc6f8b442135f09bcc12c7be38b1a0c623a005cb5e69ff3d27997bdf73")
    version("4.8.4", sha256="f148d55b16525567c0f893edf9bb2975f7c09f87f0599463e19e1b456a9d95ba")
    version("4.8.3", sha256="9cd30a343758b8f50aea4916fa7bd37de3c37c5b670fe059ae77a8b2bbabf299")
    version("4.8.2", sha256="8f28ec53e799d4aa55bd0cc4ab278d9762e0e57ac40a4b02af7fc53dcd1bef39")
    version("4.8.1", sha256="edee2673d941daf7a6e5c963d339d4a69b4db5c4b6f77b4548b3129b42198029")
    version("4.8.0", sha256="0b59ada295341902ca01e9d23e29780fb8df99a6d2bd1c2d654e9bb70c877ad8")
    version("4.7.1", sha256="90ddc7042f05667045b06e02c8d9c2064c55d9a26c02c50886254b8df85fc577")
    version("4.7.0", sha256="6cc69d9a3694e8dcf2392e9c3b518bd2497a89b3a9f25ffaec62efa52170349b")
    version("4.6.1", sha256="0261ce760e8788f85d68918d7702ae30ec677a8f331dae14adc979b4cc7badf5")
    version("4.6.0", sha256="b50f7c64ed2a4aead987de3fdf6fce7ee082407ba9297b6851cd917db72edd1d")
    version("4.5.0", sha256="27a8e4ef1e6bb6bfe076fef50afe474870edd198699d43359ef01de2f446c670")
    version("4.4.1", sha256="3c295dbf750de086c04befc0d3c7045fd3976611c2e75987c1477baca37eb549")
    version("4.4.0", sha256="f066e7488390c0bc50938d23f6582fb154466204209ca92681f0aa06340e77c8")
    version("4.3.0", sha256="d34865772d975b5d58ad80bb05312bf49aaf124d5431e54dc8618c05a0870e3c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("davix", default=True, description="Build with Davix")
    variant(
        "ec",
        default=True,
        description="Build with erasure coding component support",
        when="@5.7.0:",
    )
    variant("http", default=True, description="Build with HTTP support")
    variant("krb5", default=False, description="Build with KRB5 support")
    variant("python", default=False, description="Build pyxroot Python extension")
    variant("readline", default=True, description="Use readline")

    variant(
        "cxxstd",
        default="98",
        values=("98", "11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building",
        when="@:4.5.99",
    )

    variant(
        "cxxstd",
        default="11",
        values=("98", "11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building",
        when="@4.6.0:5.1.99",
    )

    variant(
        "cxxstd",
        default="14",
        values=("98", "11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building",
        when="@5.2.0:5.6.99",
    )

    variant(
        "cxxstd",
        default="17",
        values=("98", "11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building",
        when="@5.7.0:",
    )

    variant(
        "scitokens-cpp", default=False, when="@5.1.0:", description="Enable support for SciTokens"
    )

    variant(
        "client_only", default=False, description="Build and install client only", when="@4.10.0:"
    )

    conflicts("cxxstd=98", when="@4.7.0:")
    # C++ standard is not honored without
    # https://github.com/xrootd/xrootd/pull/1929
    # Related: C++>14 causes compilation errors with ~client_only. See
    # also https://github.com/xrootd/xrootd/pull/1933.
    conflicts("cxxstd=17", when="@5.0:5.5.2")
    conflicts("cxxstd=20", when="@5.0:5.5.2")
    conflicts("cxxstd=17", when="@5 ~client_only")
    conflicts("cxxstd=20", when="@5 ~client_only")
    conflicts("^scitokens-cpp", when="@:5.5.2 +client_only")

    depends_on("bzip2")
    depends_on("cmake@2.6:", type="build", when="@3.1.0:")
    depends_on("cmake@3.16:", type="build", when="@5.6:")
    conflicts("^cmake@:3.0", when="@5.0.0")
    conflicts("^cmake@:3.15.99", when="@5.5.4:5.5")
    depends_on("davix", when="+davix")
    depends_on("isa-l", when="+ec")
    depends_on("pkgconfig", type="build", when="+davix")
    depends_on("libxml2", when="+http")
    depends_on("uuid", when="@4.11.0:")
    depends_on("openssl@:1", when="@:5.4")
    depends_on("openssl")
    depends_on("python", when="+python")
    depends_on("py-setuptools", type="build", when="@:5.5 +python")
    depends_on("py-pip", type="build", when="@5.6: +python")
    depends_on("readline", when="+readline")
    depends_on("xz")
    depends_on("zlib-api")
    depends_on("curl")
    depends_on("krb5", when="+krb5")
    depends_on("json-c")
    depends_on("scitokens-cpp", when="+scitokens-cpp")
    conflicts("^openssl@3:", when="@:5.3.99")

    extends("python", when="+python")

    # Issue with _STAT_VER not being defined, fixed in 5.0.3
    patch(
        "https://github.com/xrootd/xrootd/commit/1f2d48fa23ba220ce92bf8ec6c15305ebbf19564.diff?full_index=1",
        sha256="cfb5c2a13257012c6f117e8a1d0a3831b02586e910d845b5ff5e80d1ab2119bc",
        when="@4:5.0.2",
    )
    patch("python-support.patch", level=1, when="@:4.8+python")
    # https://github.com/xrootd/xrootd/pull/1805
    patch(
        "https://patch-diff.githubusercontent.com/raw/xrootd/xrootd/pull/1805.patch?full_index=1",
        sha256="2655e2d609d80bf9c9ab58557f4f6940408a1af9c686e7aa214ac0348c89c8fa",
        when="@5.5.1",
    )
    # https://github.com/xrootd/xrootd/pull/1930
    patch(
        "https://patch-diff.githubusercontent.com/raw/xrootd/xrootd/pull/1930.patch?full_index=1",
        sha256="969f8b07edff42449ad76b02f3e57d93b8d6c829be1ba14bccf831c27bc971e1",
        when="@5.5.3",
    )
    # https://github.com/xrootd/xrootd/pull/2013
    patch(
        "https://patch-diff.githubusercontent.com/raw/xrootd/xrootd/pull/2013.patch?full_index=1",
        sha256="3596f45234c421abb00d0d0539033207596587f00b2d35897da8ba3302811bba",
        when="@5.5.0:5.5.5",
    )

    # do not use systemd
    patch("no-systemd-pre-5.5.2.patch", when="@:5.5.1")
    patch("no-systemd-5.5.2.patch", when="@5.5.2:")

    @when("@4.7.0:5.1.99")
    def patch(self):
        """Remove hardcoded -std=c++0x flag"""
        filter_file(r"\-std=c\+\+0x", r"", "cmake/XRootDOSDefs.cmake")

    @when("@5.2.0:5 +client_only")
    def patch(self):
        """Allow CMAKE_CXX_STANDARD to be set in cache"""
        # See https://github.com/xrootd/xrootd/pull/1929
        filter_file(
            r"^(\s+(?i:set)\s*\(\s*CMAKE_CXX_STANDARD\s+\d+)(\s*\).*)$",
            r'\1 CACHE STRING "C++ Standard"\2',
            "cmake/XRootDOSDefs.cmake",
        )

    def cmake_args(self):
        spec = self.spec
        define = self.define
        define_from_variant = self.define_from_variant
        options = []
        if spec.satisfies("@5.2.0: +client_only") or spec.satisfies("@6:"):
            options += [
                define_from_variant("CMAKE_CXX_STANDARD", "cxxstd"),
                define("CMAKE_CXX_STANDARD_REQUIRED", True),
            ]

        options += [
            define_from_variant("ENABLE_HTTP", "http"),
            define_from_variant("ENABLE_XRDCLHTTP", "davix"),
            define_from_variant("ENABLE_PYTHON", "python"),
            define_from_variant("ENABLE_READLINE", "readline"),
            define_from_variant("ENABLE_KRB5", "krb5"),
            define_from_variant("ENABLE_SCITOKENS", "scitokens-cpp"),
            define_from_variant("ENABLE_XRDEC", "ec"),
            define_from_variant("XRDCL_ONLY", "client_only"),
            define("ENABLE_CEPH", False),
            define("ENABLE_CRYPTO", True),
            define("ENABLE_FUSE", False),
            define("ENABLE_MACAROONS", False),
            define("ENABLE_VOMS", False),
            define("FORCE_ENABLED", True),
            define("USE_SYSTEM_ISAL", True),
        ]
        # see https://github.com/spack/spack/pull/11581
        if "+python" in self.spec:
            options.append(define("XRD_PYTHON_REQ_VERSION", spec["python"].version.up_to(2)))

        if "+scitokens-cpp" in self.spec:
            options.append("-DSCITOKENS_CPP_DIR=%s" % spec["scitokens-cpp"].prefix)

        return options

    @when("@:5.1.99")
    def setup_build_environment(self, env):
        cxxstdflag = ""
        if self.spec.variants["cxxstd"].value == "98":
            cxxstdflag = self.compiler.cxx98_flag
        elif self.spec.variants["cxxstd"].value == "11":
            cxxstdflag = self.compiler.cxx11_flag
        elif self.spec.variants["cxxstd"].value == "14":
            cxxstdflag = self.compiler.cxx14_flag
        elif self.spec.variants["cxxstd"].value == "17":
            cxxstdflag = self.compiler.cxx17_flag
        else:
            # The user has selected a (new?) legal value that we've
            # forgotten to deal with here.
            tty.die(
                "INTERNAL ERROR: cannot accommodate unexpected variant ",
                "cxxstd={0}".format(self.spec.variants["cxxstd"].value),
            )

        if cxxstdflag:
            env.append_flags("CXXFLAGS", cxxstdflag)
