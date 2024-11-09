# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Asio(AutotoolsPackage):
    """C++ library for network and low-level I/O programming."""

    homepage = "https://think-async.com/Asio/"
    url = "https://github.com/chriskohlhoff/asio/archive/asio-1-18-2.tar.gz"
    git = "https://github.com/chriskohlhoff/asio.git"
    maintainers("msimberg", "pauleonix")

    license("BSL-1.0")

    # As uneven minor versions of asio are not considered stable, they wont be added anymore
    version("1.30.2", sha256="755bd7f85a4b269c67ae0ea254907c078d408cce8e1a352ad2ed664d233780e8")
    version("1.30.1", sha256="94b121cc2016680f2314ef58eadf169c2d34fff97fba01df325a192d502d3a58")
    version("1.30.0", sha256="df6674bd790842b3a7422e9cc4c5d3212ac268cebdb5d38f3e783e4918313c7b")
    version("1.28.2", sha256="5705a0e403017eba276625107160498518838064a6dd7fd8b00b2e30c0ffbdee")
    version("1.28.1", sha256="5ff6111ec8cbe73a168d997c547f562713aa7bd004c5c02326f0e9d579a5f2ce")
    version("1.28.0", sha256="226438b0798099ad2a202563a83571ce06dd13b570d8fded4840dbc1f97fa328")
    version("1.26.0", sha256="935583f86825b7b212479277d03543e0f419a55677fa8cb73a79a927b858a72d")
    version("1.24.0", sha256="cbcaaba0f66722787b1a7c33afe1befb3a012b5af3ad7da7ff0f6b8c9b7a8a5b")
    version("1.22.2", sha256="985fc2d522f32d232d8386d2fa4ac6f2b25a0cad30495bf2e2e7997bce743f0b")
    version("1.22.1", sha256="30cb54a5de5e465d10ec0c2026d6b5917f5e89fffabdbabeb1475846fc9a2cf0")
    version("1.22.0", sha256="17bfd506f6d55c85a33603277a256b42ca5883bf290930040489ffeeed23724a")
    version(
        "1.21.0",
        sha256="5d2d2dcb7bfb39bff941cabbfc8c27ee322a495470bf0f3a7c5238648cf5e6a9",
        deprecated=True,  # non-stable
    )
    version("1.20.0", sha256="34a8f07be6f54e3753874d46ecfa9b7ab7051c4e3f67103c52a33dfddaea48e6")
    version(
        "1.19.2",
        sha256="5ee191aee825dfb1325cbacf643d599b186de057c88464ea98f1bae5ba4ff47a",
        deprecated=True,  # non-stable
    )
    version(
        "1.19.1",
        sha256="2555e0a29256de5c77d6a34b14faefd28c76555e094ba0371acb0b91d483520e",
        deprecated=True,  # non-stable
    )
    version(
        "1.19.0",
        sha256="11bc0e22fcdfb3f0b77574ac33760a3592c0dac7e7eece7668b823c158243629",
        deprecated=True,  # non-stable
    )
    version("1.18.2", sha256="8d67133b89e0f8b212e9f82fdcf1c7b21a978d453811e2cd941c680e72c2ca32")
    version("1.18.1", sha256="39c721b987b7a0d2fe2aee64310bd128cd8cc10f43481604d18cb2d8b342fd40")
    version("1.18.0", sha256="820688d1e0387ff55194ae20036cbae0fb3c7d11b7c3f46492369723c01df96f")
    version(
        "1.17.0",
        sha256="46406a830f8334b3789e7352ed7309a39c7c30b685b0499d289eda4fd4ae2067",
        deprecated=True,  # non-stable
    )
    version("1.16.1", sha256="e40bbd531530f08318b7c7d7e84e457176d8eae6f5ad2e3714dc27b9131ecd35")
    version("1.16.0", sha256="c87410ea62de6245aa239b9ed2057edf01d7f66acc3f5e50add9a29343c87512")

    depends_on("cxx", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("m4", type="build")
    depends_on("libtool", type="build")
    depends_on("pkgconfig", type="build", when="@1.23:")

    # See https://github.com/chriskohlhoff/asio/issues/944 and
    # https://github.com/chriskohlhoff/asio/pull/995
    conflicts(
        "%gcc@12:",
        when="@:1.22.0",
        msg="asio v1.22.1 fixed missing includes necessary for gcc v12 and above",
    )

    stds = ("11", "14", "17", "2a")
    variant(
        "cxxstd",
        default="11",
        values=stds,
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    variant("separate_compilation", default=False, description="Compile Asio sources separately")

    variant("boost_coroutine", default=False, description="Enable support for Boost.Coroutine.")
    variant("boost_regex", default=False, description="Enable support for Boost.Regex.")

    for std in stds:
        depends_on(f"boost +regex cxxstd={std}", when=f"cxxstd={std} +boost_regex")
        depends_on(f"boost +context+coroutine cxxstd={std}", when=f"cxxstd={std} +boost_coroutine")

    def configure_args(self):
        variants = self.spec.variants

        args = ["CXXFLAGS=-std=c++{0}".format(variants["cxxstd"].value)]

        if variants["separate_compilation"].value:
            args.append("--enable-separate-compilation")

        if variants["boost_coroutine"].value:
            args.append("--enable-boost-coroutine")

        if variants["boost_coroutine"].value or variants["boost_regex"].value:
            args.append("--with-boost={self.spec['boost'].prefix}")

        return args

    def url_for_version(self, version):
        return "https://github.com/chriskohlhoff/asio/archive/asio-{0}.tar.gz".format(
            version.dashed
        )

    @property
    def configure_directory(self):
        return os.path.join(self.stage.source_path, "asio")
