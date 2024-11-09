# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys

import spack.build_systems
from spack.package import *


class Libuv(CMakePackage, AutotoolsPackage):
    """Multi-platform library with a focus on asynchronous IO"""

    homepage = "https://libuv.org"
    url = "https://dist.libuv.org/dist/v1.44.1/libuv-v1.44.1.tar.gz"
    list_url = "https://dist.libuv.org/dist"
    list_depth = 1

    license("MIT")

    if sys.platform == "win32":
        version(
            "1.48.0", sha256="7f1db8ac368d89d1baf163bac1ea5fe5120697a73910c8ae6b2fffb3551d59fb"
        )
        version(
            "1.47.0", sha256="20c37a4ca77a2107879473c6c8fa0dc1350e80045df98bfbe78f7cd6d7dd2965"
        )
        version(
            "1.46.0", sha256="111f83958b9fdc65f1489195d25f342b9f7a3e683140c60e62c00fbaccddddce"
        )
        version(
            "1.45.0", sha256="f5b07f65a1e8166e47983a7ed1f42fae0bee08f7458142170c37332fc676a748"
        )
        version(
            "1.44.2", sha256="ccfcdc968c55673c6526d8270a9c8655a806ea92468afcbcabc2b16040f03cb4"
        )
        version(
            "1.44.1", sha256="9d37b63430fe3b92a9386b949bebd8f0b4784a39a16964c82c9566247a76f64a"
        )
        version(
            "1.44.0", sha256="d969fc47b8e39ec909d3f8cfa6a6e616e7c370637068ce2d95fdfcbb7f8467f5"
        )
    else:
        version(
            "1.48.0", sha256="c593139feb9061699fdd2f7fde47bb6c1ca77761ae9ec04f052083f1ef46c13b"
        )
        version(
            "1.46.0", sha256="94f101111ef3209340d7f09c2aa150ddb4feabd2f9d87d47d9f5bded835b8094"
        )
        version(
            "1.45.0", sha256="3793d8c0d6fa587721d010d0555b7e82443fd4e8b3c91e529eb6607592f52b87"
        )
        version(
            "1.44.2", sha256="8ff28f6ac0d6d2a31d2eeca36aff3d7806706c7d3f5971f5ee013ddb0bdd2e9e"
        )
        version(
            "1.44.1", sha256="b7293cefb470e17774dcf5d62c4c969636172726155b55ceef5092b7554863cc"
        )
        version(
            "1.44.0", sha256="6c52494401cfe8d08fb4ec245882f0bd4b1572b5a8e79d6c418b855422a1a27d"
        )
    version("1.43.0", sha256="90d72bb7ae18de2519d0cac70eb89c319351146b90cd3f91303a492707e693a4")
    version("1.42.0", sha256="43129625155a8aed796ebe90b8d4c990a73985ec717de2b2d5d3a23cfe4deb72")
    version("1.41.1", sha256="65db0c7f2438bc8cd48865de282bf6670027f3557d6e3cb62fb65b2e350a687d")
    version("1.41.0", sha256="1184533907e1ddad9c0dcd30a5abb0fe25288c287ff7fee303fff7b9b2d6eb6e")
    version("1.40.0", sha256="61a90db95bac00adec1cc5ddc767ebbcaabc70242bd1134a7a6b1fb1d498a194")
    version("1.39.0", sha256="5c52de5bdcfb322dbe10f98feb56e45162e668ad08bc28ab4b914d4f79911697")
    version("1.38.1", sha256="0ece7d279e480fa386b066130a562ad1a622079d43d1c30731f2f66cd3f5c647")
    version("1.25.0", sha256="0e927ddc0f1c83899000a63e9286cac5958222f8fb5870a49b0c81804944a912")
    version("1.10.0", sha256="0307a0eec6caddd476f9cad39e18fdd6f22a08aa58103c4b0aead96d638be15e")
    version("1.9.0", sha256="d595b2725abcce851c76239aab038adc126c58714cfb572b2ebb2d21b3593842")

    depends_on("c", type="build")  # generated

    def url_for_version(self, version):
        if self.spec.satisfies("@:1.43") or self.spec.satisfies("build_system=cmake"):
            # This version includes CMake files unlike the '-dist' source distribution below
            url = "https://dist.libuv.org/dist/v{0}/libuv-v{0}.tar.gz"
        else:
            # From 1.44 on, the `-dist` download includes a configure script
            url = "https://dist.libuv.org/dist/v{0}/libuv-v{0}-dist.tar.gz"
        return url.format(version, version)

    # Windows needs a CMake build, but the cmake-enabled sources do not have a
    # pre-generated configure script to enable the autotools build, so: (a)
    # pull different sources if you are on Windows and (b) make sure cmake
    # build is not chosen on Linux
    # (because Linux does not download the cmake-enabled source).
    # new libuv versions should only use CMake to prevent the scenario
    # described above
    build_system(conditional("cmake", when="platform=windows"), "autotools", default="autotools")

    with when("build_system=autotools"):
        depends_on("automake", type="build", when="@:1.43.0")
        depends_on("autoconf", type="build", when="@:1.43.0")
        depends_on("libtool", type="build", when="@:1.43.0")
        depends_on("m4", type="build", when="@:1.43.0")

    with when("build_system=cmake"):
        # explicitly require ownlibs to indicate we're short
        # circuiting the cmake<->libuv cyclic dependency here
        depends_on("cmake+ownlibs")

    conflicts(
        "%gcc@:4.8",
        when="@1.45:",
        msg="libuv version 1.45 and above require <stdatomic.h>. "
        "See: https://github.com/libuv/libuv/blob/v1.45.0/ChangeLog#L11"
        "and https://gcc.gnu.org/gcc-4.9/changes.html",
    )

    # Tries to build an Objective-C file with GCC's C frontend
    # https://github.com/libuv/libuv/issues/2805
    conflicts(
        "%gcc platform=darwin",
        when="@:1.37.9",
        msg="libuv does not compile with GCC on macOS yet, use clang. "
        "See: https://github.com/libuv/libuv/issues/2805",
    )
    conflicts(
        "platform=windows",
        when="@:1.20",
        msg="Build system for Windows in versions older than 1.21 is"
        "broken for versions of MSVC supported by Spack",
    )


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    @when("@:1.43")
    def autoreconf(self, pkg, spec, prefix):
        # This is needed because autogen.sh generates on-the-fly
        # an m4 macro needed during configuration
        Executable("./autogen.sh")()
