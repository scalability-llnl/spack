# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Doxygen(CMakePackage):
    """Doxygen is the de facto standard tool for generating documentation
    from annotated C++ sources, but it also supports other popular programming
    languages such as C, Objective-C, C#, PHP, Java, Python, IDL (Corba,
    Microsoft, and UNO/OpenOffice flavors), Fortran, VHDL, Tcl, and to some
    extent D.."""

    homepage = "https://www.doxygen.org"
    url = "https://github.com/doxygen/doxygen/archive/refs/tags/Release_1_9_5.tar.gz"

    license("GPL-2.0-or-later")

    version("1.12.0", sha256="5ca35e1258020df5fe8b21c3656aed156c317def4a81b7fe52f452edc9f35768")
    version("1.11.0", sha256="1fea49c69e51fec3dd2599947f6d48d9b1268bd5115b1bb08dffefc1fd5d19ee")
    version("1.10.0", sha256="795692a53136ca9bb9a6cd72656968af7858a78be7d6d011e12ab1dce6b9533c")
    version("1.9.8", sha256="77371e8a58d22d5e03c52729844d1043e9cbf8d0005ec5112ffa4c8f509ddde8")
    version("1.9.7", sha256="691777992a7240ed1f822a5c2ff2c4273b57c1cf9fc143553d87f91a0c5970ee")
    version("1.9.6", sha256="2a3ee47f7276b759f74bac7614c05a1296a5b028d3f6a79a88e4c213db78e7dc")
    version("1.9.5", sha256="1c5c9cd4445f694e43f089c17529caae6fe889b732fb0b145211025a1fcda1bb")
    version("1.9.4", sha256="1b083d15b29817463129ae1ae73b930d883030eeec090ea7a99b3a04fdb51c76")
    version("1.9.3", sha256="c29426222c9361dc33b762cf1c6447c78cfb0b9c213e5dcdbe31a10540c918c5")
    version("1.9.2", sha256="40f429241027ea60f978f730229d22e971786172fdb4dc74db6406e7f6c034b3")
    version("1.9.1", sha256="96db0b69cd62be1a06b0efe16b6408310e5bd4cd5cb5495b77f29c84c7ccf7d7")
    version("1.9.0", sha256="91b81141b7eeb251ca8069c114efa45e15614bcb9d7121fac4f3e9da592c56ab")
    version("1.8.20", sha256="3dbdf8814d6e68233d5149239cb1f0b40b4e7b32eef2fd53de8828fedd7aca15")
    version("1.8.18", sha256="9c88f733396dca16139483045d5afa5bbf19d67be0b8f0ea43c4e813ecfb2aa2")
    version("1.8.17", sha256="1b5d337e4b73ef1357a88cbd06fc4c301f08f279dac0adb99e876f4d72361f4f")
    version("1.8.16", sha256="75b18117f88ca1930ab74c05f6712690a26dd4fdcfc9d7d5324be43160645fb4")
    version("1.8.15", sha256="cc5492b3e2d1801ae823c88e0e7a38caee61a42303587e987142fe9b68a43078")
    version("1.8.14", sha256="18bc3790b4d5f4d57cb8ee0a77dd63a52518f3f70d7fdff868a7ce7961a6edc3")
    version("1.8.12", sha256="12142d0cb9dda839deb44a8aa16ff2f32fde23124a7c428c772150433c73f793")
    version("1.8.11", sha256="86263cb4ce1caa41937465f73f644651bd73128d685d35f18dea3046c7c42c12")
    version("1.8.10", sha256="0ac08900e5dc3ab5b65976991bf197623a7cc33ec3b32fe29360fb55d0c16b60")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # graphviz appears to be a run-time optional dependency
    variant("graphviz", default=False, description="Build with dot command support from Graphviz.")

    variant("mscgen", default=False, description="Build with support for code graphs from mscgen.")

    tags = ["build-tools"]

    executables = ["doxygen"]

    maintainers("sethrj")

    def url_for_version(self, version):
        url = "https://github.com/doxygen/doxygen/archive/refs/tags/Release_{0}.tar.gz"
        return url.format(version.underscored)

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("-v", output=str, error=str)
        match = re.search(r"^([\d\.]+)$", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version_str):
        variants = ""
        if which("dot"):
            variants += "+graphviz"
        else:
            variants += "~graphviz"

        if which("mscgen"):
            variants += "+mscgen"
        else:
            variants += "~mscgen"

        return variants

    depends_on("cmake@2.8.12:", type="build")
    depends_on("cmake@3.2:", type="build", when="@1.8.16:")
    depends_on("cmake@3.3:", type="build", when="@1.8.18:")
    depends_on("cmake@3.12:", type="build", when="@1.9.8:")
    depends_on("cmake@3.14:", type="build", when="@1.10:")

    depends_on("python", type="build")  # 2 or 3 OK; used in CMake build
    depends_on("iconv")
    depends_on("flex", type="build")
    depends_on("bison", type="build")
    # code.l just checks subminor version <=2.5.4 or >=2.5.33
    # but does not recognize 2.6.x as newer...could be patched if needed
    depends_on("flex@2.5.39", type="build", when="@1.8.10")
    depends_on("bison@2.7:", type="build", when="@1.8.10:")

    # originally bundled dependencies
    depends_on("spdlog", when="@1.9.8:")
    depends_on("sqlite", when="@1.10:")

    # optional dependencies
    depends_on("graphviz", when="+graphviz", type="run")
    depends_on("mscgen", when="+mscgen", type="run")

    # Support C++14's std::shared_ptr. For details about this patch, see
    # https://github.com/Sleepyowl/doxygen/commit/6c380ba91ae41c6d5c409a5163119318932ae2a3?diff=unified
    # Also - https://github.com/doxygen/doxygen/pull/6588
    patch("shared_ptr.patch", when="@1.8.14")

    # Support C++17's nested namespaces a::b::c. For details about this patch, see
    # https://github.com/doxygen/doxygen/pull/6977/commits/788440279e0f0fdc7dce27ec266d7d5c11bcda1c
    patch("cpp17_namespaces.patch", when="@1.8.15")

    # Workaround for gcc getting stuck in an infinite loop
    patch("gcc-partial-inlining-bug.patch", when="@1.8.20: %gcc@7")

    # https://github.com/doxygen/doxygen/issues/9312
    patch(
        "https://github.com/doxygen/doxygen/commit/5198966c8d5fec89116d025c74934ac03ea511fa.patch?full_index=1",
        sha256="94a93f869a2dc63014ec4e9f1a31a45eefcab63931823979fdb4502f0caf625f",
        when="@1.9.4 %gcc@12:",
    )

    # https://github.com/doxygen/doxygen/pull/10896: use correct option name with system sqlite3
    patch(
        "https://github.com/doxygen/doxygen/commit/83de58c5f4f685a129127c2501f4fccd9557f6c4.patch?full_index=1",
        sha256="8b46b763b3f0a2726f765141cbfa3eb6efd746531a4d689531e42ff56fc334e2",
        when="@1.10:1.11.0",
    )

    # Some GCC 7.x get stuck in an infinite loop
    conflicts("%gcc@7.0:7.9", when="@1.9:")

    def patch(self):
        if self.spec["iconv"].name != "libiconv":
            return

        if self.spec.satisfies("@:1.11"):
            # On Linux systems, iconv is provided by libc. Since CMake finds the
            # symbol in libc, it does not look for libiconv, which leads to linker
            # errors. This makes sure that CMake always looks for the external
            # libconv instead.
            filter_file(
                "check_function_exists(iconv_open ICONV_IN_GLIBC)",
                "set(ICONV_IN_GLIBC FALSE)",
                join_path("cmake", "FindIconv.cmake"),
                string=True,
            )

    def cmake_args(self):
        return [
            self.define("use_sys_spdlog", self.spec.satisfies("@1.9.8:")),
            self.define("use_sys_sqlite3", self.spec.satisfies("@1.10:")),
        ]
