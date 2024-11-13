# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fmt(CMakePackage):
    """fmt (formerly cppformat) is an open-source formatting library.
    It can be used as a safe alternative to printf or as a fast alternative
    to C++ IOStreams."""

    homepage = "https://fmt.dev/"
    url = "https://github.com/fmtlib/fmt/releases/download/7.1.3/fmt-7.1.3.zip"
    git = "https://github.com/fmtlib/fmt.git"
    maintainers("msimberg")

    license("MIT")

    version("11.0.2", sha256="40fc58bebcf38c759e11a7bd8fdc163507d2423ef5058bba7f26280c5b9c5465")
    version("11.0.1", sha256="62ca45531814109b5d6cef0cf2fd17db92c32a30dd23012976e768c685534814")
    version("11.0.0", sha256="583ce480ef07fad76ef86e1e2a639fc231c3daa86c4aa6bcba524ce908f30699")
    version("10.2.1", sha256="312151a2d13c8327f5c9c586ac6cf7cddc1658e8f53edae0ec56509c8fa516c9")
    version("10.2.0", sha256="8a942861a94f8461a280f823041cde8f620a6d8b0e0aacc98c15bb5a9dd92399")
    version("10.1.1", sha256="b84e58a310c9b50196cda48d5678d5fa0849bca19e5fdba6b684f0ee93ed9d1b")
    version("10.1.0", sha256="d725fa83a8b57a3cedf238828fa6b167f963041e8f9f7327649bddc68ae316f4")
    version("10.0.0", sha256="4943cb165f3f587f26da834d3056ee8733c397e024145ca7d2a8a96bb71ac281")
    version("9.1.0", sha256="cceb4cb9366e18a5742128cb3524ce5f50e88b476f1e54737a47ffdf4df4c996")
    version("9.0.0", sha256="fc96dd2d2fdf2bded630787adba892c23cb9e35c6fd3273c136b0c57d4651ad6")
    version("8.1.1", sha256="23778bad8edba12d76e4075da06db591f3b0e3c6c04928ced4a7282ca3400e5d")
    version("8.1.0", sha256="d8e9f093b2241c3a9fc3895e23231ef9de00c762cfa0a9c65e4748755bc352ae")
    version("8.0.1", sha256="a627a56eab9554fc1e5dd9a623d0768583b3a383ff70a4312ba68f94c9d415bf")
    version("7.1.3", sha256="5d98c504d0205f912e22449ecdea776b78ce0bb096927334f80781e720084c9f")
    version("7.1.2", sha256="4d6968ab7c01e95cc76df136755703defb985105a117b83057e4fd5d53680ea7")
    version("7.1.0", sha256="308af4e36ee3ab527b51014a2a5d862682c84f5d16f7a597aea34c84853cbcb0")
    version("6.1.2", sha256="63650f3c39a96371f5810c4e41d6f9b0bb10305064e6faf201cbafe297ea30e8")
    version("5.3.0", sha256="4c0741e10183f75d7d6f730b8708a99b329b2f942dad5a9da3385ab92bb4a15c")
    version("5.2.1", sha256="43894ab8fe561fc9e523a8024efc23018431fa86b95d45b06dbe6ddb29ffb6cd")
    version("5.2.0", sha256="c016db7f825bce487a7929e1edb747b9902a2935057af6512cad3df3a080a027")
    version("5.1.0", sha256="77ef9fea638dc846e484409fbc1ea710bb9bcea042e7b35b8805041bf7655ad5")
    version("5.0.0", sha256="8dd58daf13e7e8adca99f8725ef3ae598f9c97efda7d6d8d4c49db5047879097")
    version("4.1.0", sha256="9d49bf02ceb9d0eec51144b203b63b77e69d3798bb402fb82e7d0bdb06c79eeb")
    version("4.0.0", sha256="10a9f184d4d66f135093a08396d3b0a0ebe8d97b79f8b3ddb8559f75fe4fcbc3")
    version("3.0.2", sha256="51407b62a202b29d1a9c0eb5ecd4095d30031aea65407c42c25cb10cb5c59ad4")
    version("3.0.1", sha256="4c9af0dc919a8ae7022b44e1a03c435e42d65c866f44667d8d920d342b098550")
    version("3.0.0", sha256="1b050b66fa31b74f1d75a14f15e99e728ab79572f176a53b2f8ad7c201c30ceb")
    version("master", branch="master")

    depends_on("cxx", type="build")

    variant(
        "cxxstd",
        default="11",
        values=("98", "11", "14", "17", "20", conditional("23", when="^cmake@3.20.3:")),
        multi=False,
        description="Use the specified C++ standard when building",
    )
    variant("shared", default=False, description="Build shared library")
    variant("pic", default=True, description="Build position-independent code")

    depends_on("cmake@3.1.0:", type="build")

    # Supported compilers/standards are detailed here:
    # http://fmtlib.net/latest/index.html#portability
    conflicts("%gcc@:4.3", when="@5:")
    conflicts("%llvm@:2.8", when="@5:")
    # 5 and above require C++11
    conflicts("cxxstd=98", when="@5:")
    # 5.0.0 enables C++14 auto return types in C++11 mode
    conflicts("cxxstd=11", when="@5.0.0")
    # 4.1 fails with C++17 (https://github.com/fmtlib/fmt/issues/722)
    conflicts("cxxstd=17", when="@4.1.0")
    # edg based compilers have issues with fmt 9.0.0 and C++17 standard
    # (https://github.com/fmtlib/fmt/issues/3028)
    conflicts("cxxstd=17", when="@9.0.0%intel")
    conflicts("cxxstd=17", when="@9.0.0%nvhpc")

    # Use CMAKE_CXX_STANDARD to define C++ flag, as in later versions
    patch("fmt-use-cmake-cxx-standard_3.0.0.patch", when="@3.0.0")

    # Remove hardcoding of "-std=c++11/0x" in INTERFACE_COMPILE_OPTIONS
    patch("fmt-no-export-cpp11flag_3.0.0.patch", when="@3.0.0:3.0.1")

    # Only allow [[attributes]] on C++11 and higher
    patch("fmt-attributes-cpp11_4.1.0.patch", when="@4.1.0")

    # Fix compilation with hipcc/dpcpp: https://github.com/fmtlib/fmt/issues/3005
    patch(
        "https://github.com/fmtlib/fmt/commit/0b0f7cfbfcebd021c910078003d413354bd843e2.patch?full_index=1",
        sha256="08fb707bf8b4fc890d6eed29217ead666558cbae38f9249e22ddb82212f0eb4a",
        when="@9.0.0:9.1.0",
    )

    # Fix compilation with clang in CUDA mode: https://github.com/fmtlib/fmt/issues/3740
    patch(
        "https://github.com/fmtlib/fmt/commit/89860eb9013a345608c8144b1aad5f12b0682d7e.patch?full_index=1",
        sha256="6ef12fe60a2b3625139c6d29c748dafd81b51e2a0690c1fa37604ed5b15615e0",
        when="@10.0.0:10.1.1",
    )

    # Fix 'variable "buffer" may not be initialized' compiler error
    patch(
        "fmt-no-variable-initialize_10.0.0.patch", when="@10.0.0:11.0.2%clang@12.0.1.ibm.gcc.8.3.1"
    )
    patch(
        "fmt-no-variable-initialize_10.0.0.patch", when="@10.0.0:11.0.2%clang@14.0.5.ibm.gcc.8.3.1"
    )

    def cmake_args(self):
        spec = self.spec
        args = []

        if self.spec.satisfies("+shared"):
            args.append("-DBUILD_SHARED_LIBS=ON")

        if spec.satisfies("+pic"):
            args.extend(
                [
                    "-DCMAKE_C_FLAGS={0}".format(self.compiler.cc_pic_flag),
                    "-DCMAKE_CXX_FLAGS={0}".format(self.compiler.cxx_pic_flag),
                ]
            )

        args.append("-DCMAKE_CXX_STANDARD={0}".format(spec.variants["cxxstd"].value))
        # Require standard at configure time to guarantee the
        # compiler supports the selected standard.
        args.append("-DCMAKE_CXX_STANDARD_REQUIRED=ON")

        # When cxxstd is 98, must disable FMT_USE_CPP11
        if spec.satisfies("cxxstd=98"):
            args.append("-DFMT_USE_CPP11=OFF")

        # Can't build docs without doxygen+python+virtualenv
        # and call to build "doc" target
        args.append("-DFMT_DOC=OFF")

        # Don't build tests
        args.append(self.define("FMT_TEST", self.run_tests))

        return args
