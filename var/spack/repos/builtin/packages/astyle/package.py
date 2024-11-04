# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems import makefile
from spack.package import *


class Astyle(CMakePackage, MakefilePackage):
    """A Free, Fast, and Small Automatic Formatter for C, C++, C++/CLI,
    Objective-C, C#, and Java Source Code.
    """

    homepage = "https://astyle.sourceforge.net/"
    url = "https://sourceforge.net/projects/astyle/files/astyle/astyle%204.1.11/astyle-4.1.11.tar.bz2"
    list_url = "https://sourceforge.net/projects/astyle/files/astyle"
    list_depth = 1

    maintainers("cessenat")

    license("MIT")

    version("3.4.11", sha256="15b22bc6cbc038ccd8cef3804efec02f35c6f2538b75c93bc7f76e4de98aba92")
    version("3.3.1", sha256="246979db8ba82948d2925f823293321617e4a51dcac8719b370b670782e9c57d")
    version("3.2.1", sha256="191576fbd1f4abe55a25769c176da78294ec590f96f27037a4746bda0f84fe60")
    version("3.1", sha256="cbcc4cf996294534bb56f025d6f199ebfde81aa4c271ccbd5ee1c1a3192745d7")
    version("3.0.1", sha256="6c3ab029e0e4a75e2e603d449014374aa8269218fdd03a4aaa46ab743b1912fd")
    version("2.06", sha256="3b7212210dc139e8f648e004b758c0be1b3ceb1694b22a879202d2b833db7c7e")
    version("2.05.1", sha256="fbdfc6f1966a972d19a215927266c76d4183eee235ed1e2bd7ec551c2a270eac")
    version("2.04", sha256="70b37f4853c418d1e2632612967eebf1bdb93dfbe558c51d7d013c9b4e116b60")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.8.0:", type="build", when="@3.2.0:")

    build_system(conditional("cmake", when="@3.2.0:"), "makefile", default="cmake")

    parallel = False

    conflicts("%oneapi", when="@:3.1.99")

    def url_for_version(self, version):
        root = self.url.rsplit("/", 2)[0]
        url = f"{root}/astyle%20{version.up_to(2)}/astyle-{version}.tar.bz2"
        if version < Version("3.2.0"):
            url = f"{root}/astyle%20{version.up_to(2)}/astyle_{version}_linux.tar.gz"
        return url


class MakefileBuilder(makefile.MakefileBuilder):
    @property
    def build_directory(self):
        return join_path(self.stage.source_path, "build", self.pkg.compiler.name)

    def edit(self, pkg, spec, prefix):
        makefile = join_path(self.build_directory, "Makefile")
        filter_file(r"^CXX\s*=.*", f"CXX={spack_cxx}", makefile)
        # If the group is not a user account, the installation will fail,
        # so remove the -o $ (USER) -g $ (USER) parameter.
        filter_file(r"^INSTALL=.*", "INSTALL=install", makefile)

    @property
    def install_targets(self):
        return ["install", f"prefix={self.prefix}"]
