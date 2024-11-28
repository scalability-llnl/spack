# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libstdcompat(CMakePackage):
    """A compatibility header for C++14, 17, and 20 for C++11"""

    homepage = "https://github.com/robertu94/std_compat"
    url = "https://github.com/robertu94/std_compat/archive/0.0.1.tar.gz"
    git = "https://github.com/robertu94/std_compat"

    maintainers("robertu94")

    version("master", branch="master")
    version("0.0.21", sha256="67cfd57080a74752b4c239e031cc44734286589a89bb1cd51a8bd7039f87a3f3")
    version("0.0.20", sha256="9fdc632eb135f57132953b512d8f9101e8eb4e6a88e6c3b838aaa9c51a2dbfd6")
    version("0.0.19", sha256="584ee52b1f82671e5d8fde786c46aa7e98d30104674c6f4b75dbae8d83b13f21")
    version("0.0.17", sha256="8c8a3f2727dd28c51ab10e02a1114e39b683d6d9ea119d5c2a953f8c41d6bedd")
    version("0.0.16", sha256="1287251b694adb80210536ab6eb75c1ff2c4ed8b77023208a757ae27c9dae0bb")
    version("0.0.15", sha256="af374a8883a32d874f6cd18cce4e4344e32f9d60754be403a5ac7114feca2a28")
    version("0.0.14", sha256="9a794d43a1d79aec3350b89d8c06689b8b32cf75e2742cdfa9dc0e3f2be6f04e")
    version("0.0.13", sha256="460656189e317e108a489af701fa8f33f13a93d96380788e692a1c68100e0388")
    version("0.0.12", sha256="67c1d1724122a1ba7cebcd839658786680fa06a549369f4a7c36a44ad93ddd5d")
    version("0.0.11", sha256="f166cd55e3cf845e4ed9eee1fb25de1f991dee5ef538c1e3ea9cbe7714863ccb")
    version("0.0.10", sha256="d55ad9b7f61efa5a4bbef047f729af5ed9e44f96bb9d54f36023fa99af2bfe40")
    version("0.0.9", sha256="325e816153aab0aee791e4c628e01dbc5b7aa336558d1694bd5de763f34e37e6")
    version("0.0.8", sha256="3103295033fb6723dc462a8979ccfe3b571347c2a458f4cc8d8324981dedead9")
    version("0.0.7", sha256="8cb4ed704aef427bbe4c86ee874a350561e6e059223e7b3d60f1e0d7300ccfe9")
    version("0.0.6", sha256="cf4288422c9e9ab9e7c831c11a6a67907fe19b0da40601cc2b05e76e3be2f795")
    version("0.0.5", sha256="a8599a12253b5ebdb38c6e416e7896444fd48a15167fe481985182ed17fc6883")
    version("0.0.4", sha256="b2aeb4e60105635acb3f41b2c9559956e7b75d999c73b84b14be5b78daa4e6a9")
    version("0.0.3", sha256="098678618a335bb2e8b25ceae8c3498f4c3056fd9e03467948bab18252afb46d")
    version("0.0.2", sha256="36424399e649be38bdb21899aa45f94aebba25c66048bab2751b1b3b9fd27238")
    version("0.0.1", sha256="3d63e901f4e20b9032a67086f4b4281f641ee0dea436cf15f7058faa40d8637b")

    depends_on("cxx", type="build")  # generated

    variant(
        "cpp_compat",
        values=("11", "14", "17", "20", "23", "auto"),
        default="auto",
        multi=False,
        description="version of the c++ standard to use and depend on",
    )
    variant("cpp_unstable", default=True, description="sets CXX_STANDARD_REQUIRED")
    variant("boost", default=False, description="support older compilers using boost")

    depends_on("boost+thread", when="%gcc@:8.0.0")
    depends_on("boost+thread", when="+boost")
    depends_on("boost+thread", when="cpp_compat=11")
    depends_on("boost+thread", when="cpp_compat=14")

    conflicts("~cpp_unstable", when="@0.0.7: cpp_compat=auto")
    conflicts("+cpp_unstable", when="@:0.0.7")
    conflicts("cpp_compat=11", when="@:0.0.7")
    conflicts("cpp_compat=14", when="@:0.0.7")
    conflicts("cpp_compat=17", when="@:0.0.7")
    conflicts("cpp_compat=20", when="@:0.0.7")

    def max_cxx_version(self):
        if self.spec.version >= Version("0.0.20"):
            try:
                self.compiler.cxx23_flag
                return "23"
            except Exception:
                pass
            try:
                self.compiler.cxx20_flag
                return "20"
            except Exception:
                pass
        try:
            self.compiler.cxx17_flag
            return "17"
        except Exception:
            pass
        try:
            self.compiler.cxx14_flag
            return "14"
        except Exception:
            pass
        self.compiler.cxx11_flag
        return "11"

    def cmake_args(self):
        args = []
        cpp_compat = self.spec.variants["cpp_compat"].value

        if self.spec.satisfies("+cpp_unstable"):
            args.append("-DSTDCOMPAT_CXX_UNSTABLE=ON")

        if cpp_compat == "auto":
            args.append("-DSTDCOMPAT_CXX_VERSION=%s" % self.max_cxx_version())
        elif cpp_compat == "11":
            args.append("-DSTDCOMPAT_CXX_VERSION=11")
        elif cpp_compat == "14":
            args.append("-DSTDCOMPAT_CXX_VERSION=14")
        elif cpp_compat == "17":
            args.append("-DSTDCOMPAT_CXX_VERSION=17")
        elif cpp_compat == "20":
            args.append("-DSTDCOMPAT_CXX_VERSION=20")

        if self.run_tests:
            args.append("-DBUILD_TESTING=ON")
        else:
            args.append("-DBUILD_TESTING=OFF")
        return args
