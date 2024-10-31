# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jsoncpp(CMakePackage, MesonPackage):
    """JsonCpp is a C++ library that allows manipulating JSON values,
    including serialization and deserialization to and from strings.
    It can also preserve existing comment in unserialization/serialization
    steps, making it a convenient format to store user input files."""

    homepage = "https://github.com/open-source-parsers/jsoncpp"
    url = "https://github.com/open-source-parsers/jsoncpp/archive/1.7.3.tar.gz"
    tags = ["windows"]

    license("Public-Domain")

    version("1.9.5", sha256="f409856e5920c18d0c2fb85276e24ee607d2a09b5e7d5f0a371368903c275da2")
    version("1.9.4", sha256="e34a628a8142643b976c7233ef381457efad79468c67cb1ae0b83a33d7493999")
    version("1.9.3", sha256="8593c1d69e703563d94d8c12244e2e18893eeb9a8a9f8aa3d09a327aa45c8f7d")
    version("1.9.2", sha256="77a402fb577b2e0e5d0bdc1cf9c65278915cdb25171e3452c68b6da8a561f8f0")
    version("1.9.1", sha256="c7b40f5605dd972108f503f031b20186f5e5bca2b65cd4b8bd6c3e4ba8126697")
    version("1.9.0", sha256="bdd3ba9ed1f110b3eb57474d9094e90ab239b93b4803b4f9b1722c281e85a4ac")
    version("1.8.4", sha256="c49deac9e0933bcb7044f08516861a2d560988540b23de2ac1ad443b219afdb6")
    version("1.8.3", sha256="3671ba6051e0f30849942cc66d1798fdf0362d089343a83f704c09ee7156604f")
    version("1.8.2", sha256="811f5aee20df2ef0868a73a976ec6f9aab61f4ca71c66eddf38094b2b3078eef")
    version("1.8.1", sha256="858db2faf348f89fdf1062bd3e79256772e897e7f17df73e0624edf004f2f9ac")
    version("1.8.0", sha256="5deb2462cbf0c0121c9d6c9823ec72fe71417e34242e3509bc7c003d526465bc")
    version("1.7.7", sha256="087640ebcf7fbcfe8e2717a0b9528fff89c52fcf69fa2a18cc2b538008098f97")
    version("1.7.6", sha256="07cf5d4f184394ec0a9aa657dd4c13ea682c52a1ab4da2fb176cb2d5501101e8")
    version("1.7.5", sha256="4338c6cab8af8dee6cdfd54e6218bd0533785f552c6162bb083f8dd28bf8fbbe")
    version("1.7.4", sha256="10dcd0677e80727e572a1e462193e51a5fde3e023b99e144b2ee1a469835f769")
    version("1.7.3", sha256="1cfcad14054039ba97c22531888796cb9369e6353f257aacaad34fda956ada53")

    depends_on("cxx", type="build")  # generated

    # From 1.9.3 onwards CMAKE_CXX_STANDARD is finally set to 11.
    variant(
        "cxxstd",
        default="default",
        values=("default", conditional("98", when="@:1.8"), "11", "14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
        when="@:1.9.2 build_system=cmake",
    )

    build_system("cmake", conditional("meson", when="@1.9.2:"), default="cmake")

    with when("build_system=cmake"):
        depends_on("cmake@3.1:", type="build")
        depends_on("cmake@3.9:", when="@1.9:", type="build")

    with when("build_system=meson"):
        depends_on("meson@0.49.0:", type="build")

    depends_on("python", type="test")

    # Ref: https://github.com/open-source-parsers/jsoncpp/pull/1023
    # Released in 1.9.2, patch does not apply cleanly across releases.
    # May apply to more compilers in the future.
    @when("@:1.9.1 %clang@10.0.0:")
    def patch(self):
        filter_file(
            "return d >= min && d <= max;",
            "return d >= static_cast<double>(min) && " "d <= static_cast<double>(max);",
            "src/lib_json/json_value.cpp",
        )


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        args = [
            self.define("BUILD_SHARED_LIBS", True),
            self.define("JSONCPP_WITH_TESTS", self.pkg.run_tests),
        ]
        if "cxxstd" in self.spec.variants:
            cxxstd = self.spec.variants["cxxstd"].value
            if cxxstd != "default":
                args.append(self.define("CMAKE_CXX_STANDARD", cxxstd))
        return args


class MesonBuilder(spack.build_systems.meson.MesonBuilder):
    def meson_args(self):
        return ["-Dtests={}".format("true" if self.pkg.run_tests else "false")]
