# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rapidjson(CMakePackage):
    """A fast JSON parser/generator for C++ with both SAX/DOM style API"""

    homepage = "https://rapidjson.org"
    url = "https://github.com/Tencent/rapidjson/archive/v1.1.0.tar.gz"
    git = "https://github.com/Tencent/rapidjson.git"

    license("MIT")

    version("1.2.0-2024-08-16", commit="7c73dd7de7c4f14379b781418c6e947ad464c818")
    version("1.2.0-2022-03-09", commit="8261c1ddf43f10de00fd8c9a67811d1486b2c784")
    version("1.2.0-2021-08-13", commit="00dbcf2c6e03c47d6c399338b6de060c71356464")
    version("1.1.0", sha256="bf7ced29704a1e696fbccf2a2b4ea068e7774fa37f6d7dd4039d0787f8bed98e")
    version("1.0.2", sha256="c3711ed2b3c76a5565ee9f0128bb4ec6753dbcc23450b713842df8f236d08666")
    version("1.0.1", sha256="a9003ad5c6384896ed4fd1f4a42af108e88e1b582261766df32d717ba744ee73")
    version("1.0.0", sha256="4189b32b9c285f34b37ffe4c0fd5627c1e59c2444daacffe5a96fdfbf08d139b")

    depends_on("cxx", type="build")  # generated

    variant("doc", default=False, description="Build and install documentation")

    depends_on("doxygen+graphviz", when="+doc")

    # -march=native causes issues on ARM, with older GCC, and with Fujitsu
    # Spack injects the appropriate optimization flags anyway
    # https://github.com/Tencent/rapidjson/issues/1816
    patch("no_march-1.2-2024.patch", when="@1.2.0-2024-08-16:")
    patch("no_march-1.2.patch", when="@1.2:1.2.0-2022-03-09")
    patch("no_march-1.1.patch", when="@1.1")
    patch("no_march-1.0.patch", when="@1.0")

    conflicts("%gcc@14", when="@:1.2.0-2022-03-09")

    def cmake_args(self):
        args = []
        args.append(self.define_from_variant("RAPIDJSON_BUILD_DOC", "doc"))
        return args
