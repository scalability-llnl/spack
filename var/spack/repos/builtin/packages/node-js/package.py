# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import subprocess
import sys

from spack.package import *


class NodeJs(Package):
    """Node.js is an open-source, cross-platform JavaScript runtime environment."""

    homepage = "https://nodejs.org/"
    url = "https://nodejs.org/dist/v13.5.0/node-v13.5.0.tar.gz"
    list_url = "https://nodejs.org/dist/"
    list_depth = 1

    maintainers("cosmicexplorer")

    license("Unicode-TOU")

    # Current (latest features) - odd major number
    version("21.7.3", sha256="ce1f61347671ef219d9c2925313d629d3fef98fc8d7f5ef38dd4656f7d0f58e7")
    version("19.2.0", sha256="aac9d1a366fb57d68f4639f9204d1de5d6387656959a97ed929a5ba9e62c033a")
    version("17.9.1", sha256="1102f5e0aafaab8014d19c6c57142caf2ba3ef69d88d7a7f0f82798051796027")
    version("15.3.0", sha256="cadfa384a5f14591b84ce07a1afe529f28deb0d43366fb0ae4e78afba96bfaf2")
    with default_args(deprecated=True):
        # requires deprecated python versions
        version(
            "13.8.0", sha256="815b5e1b18114f35da89e4d98febeaba97555d51ef593bd5175db2b05f2e8be6"
        )
        version(
            "13.5.0", sha256="4b8078d896a7550d7ed399c1b4ac9043e9f883be404d9b337185c8d8479f2db8"
        )

    # LTS (recommended for most users) - even major number
    version(
        "22.11.0",
        sha256="24e5130fa7bc1eaab218a0c9cb05e03168fa381bb9e3babddc6a11f655799222",
        preferred=True,
    )
    version("22.4.0", sha256="b62cd83c9a57a11349883f89b1727a16e66c02eb6255a4bf32714ff5d93165f5")
    version("22.3.0", sha256="6326484853093ab6b8f361a267445f4a5bff469042cda11a3585497b13136b55")
    version("20.15.0", sha256="01e2c034467a324a33e778c81f2808dff13d289eaa9307d3e9b06c171e4d932d")
    version("18.12.1", sha256="ba8174dda00d5b90943f37c6a180a1d37c861d91e04a4cb38dc1c0c74981c186")
    version("16.18.1", sha256="3d24c9c3a953afee43edc44569045eda56cd45cd58b0539922d17da62736189c")
    version("14.21.1", sha256="76ba961536dc11e4dfd9b198c61ff3399e655eca959ae4b66d926f29bfcce9d3")
    version("14.16.1", sha256="5f5080427abddde7f22fd2ba77cd2b8a1f86253277a1eec54bc98a202728ce80")
    version("14.15.1", sha256="a1120472bf55aea745287693a6651e16973e1008c9d6107df350126adf9716fe")
    with default_args(deprecated=True):
        # requires deprecated python versions
        version(
            "14.13.0", sha256="8538b2e76aa06ee0e6eb1c118426c3c5ca53b2e49d66591738eacf76e89edd61"
        )
        version(
            "14.10.0", sha256="7e0d7a1aa23697415e3588a1ca4f1c47496e6c88b9cf37c66be90353d3e4ac3e"
        )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("debug", default=False, description="Include debugger support")
    variant("doc", default=False, description="Compile with documentation")
    variant(
        "icu4c",
        default=False,
        description="Build with support for all locales instead of just English",
    )
    variant(
        "openssl",
        default=True,
        description="Build with Spacks OpenSSL instead of the bundled version",
    )
    variant(
        "zlib", default=True, description="Build with Spacks zlib instead of the bundled version"
    )

    # https://github.com/nodejs/node/blob/master/BUILDING.md#unix-and-macos
    depends_on("gmake@3.81:", type="build")

    # python requirements are based according to
    # https://github.com/spack/spack/pull/47942#discussion_r1875624177
    depends_on("python@:3.7", when="@13.0.0:13.0.1", type="build")
    depends_on("python@:3.8", when="@13.1.0:14.13.1", type="build")
    depends_on("python@:3.9", when="@14.14.0:14.18.1", type="build")
    depends_on("python@:3.10", when="@14.18.2:14.21.3", type="build")
    depends_on("python@:3.9", when="@15.0.0:15.14.0", type="build")
    depends_on("python@:3.9", when="@16.0.0:16.10.0", type="build")
    depends_on("python@:3.10", when="@16.11.0:16.18.1", type="build")
    depends_on("python@:3.11", when="@16.19.0:16.20.2", type="build")
    depends_on("python@:3.10", when="@17.0.0:18.12.1", type="build")
    depends_on("python@:3.11", when="@18.13.0:18.19.1", type="build")
    depends_on("python@:3.12", when="@18.20.0:18.20.5", type="build")
    depends_on("python@:3.10", when="@19.0.0:19.0.1", type="build")
    depends_on("python@:3.11", when="@19.1.0:20.10.0", type="build")
    depends_on("python@:3.12", when="@20.11.0:20.15.1", type="build")
    depends_on("python@:3.13", when="@20.16.0:20.18.1", type="build")
    depends_on("python@:3.11", when="@21.0.0:21.1.0", type="build")
    depends_on("python@:3.12", when="@21.2.0:22.2.0", type="build")
    depends_on("python@:3.13", when="@22.3.0:22.7.0", type="build")

    depends_on("libtool", type="build", when=sys.platform != "darwin")
    depends_on("pkgconfig", type="build")
    # depends_on('bash-completion', when="+bash-completion")
    depends_on("icu4c", when="+icu4c")
    depends_on("openssl@1.1:", when="+openssl")
    depends_on("zlib-api", when="+zlib")

    # https://github.com/nodejs/node/blob/main/BUILDING.md#supported-toolchains
    conflicts("%gcc@:12.1", when="@23:")
    conflicts("%gcc@:10.0", when="@20:")
    conflicts("%gcc@:8.2", when="@16:")
    conflicts("%gcc@:6.2", when="@12:")
    conflicts("%apple-clang@:11", when="@21:")
    conflicts("%apple-clang@:10", when="@16:")
    conflicts("%apple-clang@:9", when="@13:")

    phases = ["configure", "build", "install"]

    # https://github.com/spack/spack/issues/19310
    conflicts(
        "%gcc@:4.8",
        msg="fails to build with gcc 4.8 (see https://github.com/spack/spack/issues/19310)",
    )

    conflicts(
        "%gcc@14:", when="@:19", msg="fails to build with gcc 14+ due to implicit conversions"
    )

    # See https://github.com/nodejs/node/issues/52223
    patch("fix-old-glibc-random-headers.patch", when="^glibc@:2.24")

    # Work around gcc-12.[1-2] compiler bug
    # See https://github.com/nodejs/node/pull/53728
    # and https://github.com/nodejs/node/issues/53633
    patch("fix-broken-gcc12-pr53728.patch", when="@22.2:22.5")

    def setup_build_environment(self, env):
        # Force use of experimental Python 3 support
        env.set("PYTHON", self.spec["python"].command.path)
        env.set("NODE_GYP_FORCE_PYTHON", self.spec["python"].command.path)

    def configure_args(self):
        # On macOS, the system libtool must be used
        # So, we ensure that this is the case by...
        if sys.platform == "darwin":
            # Possible output formats:
            #
            # /usr/bin/libtool
            process_pipe = subprocess.Popen(["which", "libtool"], stdout=subprocess.PIPE)
            result_which = process_pipe.communicate()[0].strip()

            # Possible output formats:
            #
            # /usr/bin/libtool
            # libtool: /usr/bin/libtool
            #
            # We specify -M -f (an empty list of man-path entries) to prevent man-page
            # searching to avoid an Illegal seek error processing manpath results in CI,
            # which prevents the last form:
            # libtool: /usr/bin/libtool /Applications/Xcode.app/.../share/man/man1/libtool.1
            process_pipe = subprocess.Popen(
                ["whereis", "-M", "-f", "libtool"], stdout=subprocess.PIPE
            )
            result_whereis_list = process_pipe.communicate()[0].strip().split()
            if len(result_whereis_list) == 1:
                result_whereis = result_whereis_list[0]
            else:
                result_whereis = result_whereis_list[1]

            assert result_which == result_whereis, (
                "On macOS the system libtool must be used. Please (temporarily) remove "
                "\n or its link to libtool from PATH"
            )

        args = [
            "--prefix={0}".format(self.prefix),
            # Note: npm is updated more regularly than node.js, so we build
            # the package instead of using the bundled version
            "--without-npm",
        ]

        if "+debug" in self.spec:
            args.append("--debug")

        if "+openssl" in self.spec:
            args.extend(
                [
                    "--shared-openssl",
                    "--shared-openssl-includes={0}".format(self.spec["openssl"].prefix.include),
                    "--shared-openssl-libpath={0}".format(self.spec["openssl"].prefix.lib),
                ]
            )

        if "+zlib" in self.spec:
            args.extend(
                [
                    "--shared-zlib",
                    "--shared-zlib-includes={0}".format(self.spec["zlib-api"].prefix.include),
                    "--shared-zlib-libpath={0}".format(self.spec["zlib-api"].prefix.lib),
                ]
            )

        if "+icu4c" in self.spec:
            args.append("--with-intl=full-icu")

        return args

    def configure(self, spec, prefix):
        python("configure.py", *self.configure_args())

    def build(self, spec, prefix):
        make()
        if "+doc" in spec:
            make("doc")

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def build_test(self):
        make("test")
        make("test-addons")

    def install(self, spec, prefix):
        make("install")
