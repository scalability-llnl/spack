# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class Winbison(CMakePackage):
    """Bison is a general-purpose parser generator that converts
    an annotated context-free grammar into a deterministic LR or
    generalized LR (GLR) parser employing LALR(1) parser tables."""

    homepage = "https://github.com/lexxmark/winflexbison#readme"
    url = "https://github.com/lexxmark/winflexbison/archive/v2.5.25.tar.gz"
    tags = ["windows"]

    executables = [r"^bison(.*)?$"]

    license("GFDL-1.3-only")

    version("2.5.25", sha256="8e1b71e037b524ba3f576babb0cf59182061df1f19cd86112f085a882560f60b")
    version("2.5.24", sha256="a49d6e310636e3487e1e066e411d908cfeae2d5b5fde1f3cf74fe1d6d4301062")
    version("2.5.23", sha256="445bd1bcb90e0c84e97f6e44de76869f8e778c60ddbd7c39a7b2142f8ba43e61")
    version("2.5.22", sha256="697c2c4af3308625605b75498bd63a9a294660f8e43a4c35452cf4334fa4a530")
    version("2.5.21", sha256="41e31960cc7e8ccd4b95bd770a6279d31ab7dee156e6fb4e55834f8f220637f4")
    version("2.5.20", sha256="cd29f888f167128c22211444c6e31b5f4823a7de0e23d8039559ee87b80349c9")
    version("2.5.19", sha256="265f930e5b2e8e24d179d703668355550b226d033fdbe0a9232c671591ddfd0b")
    version("2.5.18", sha256="1db991bebaded832427539b6b28a8f36948e5ce3db5701b5104f85b66b8484de")
    version("2.5.17", sha256="2ab4c895f9baf03dfdfbb2dc4abe60e87bf46efe12ed1218c38fd7761f0f58fc")
    version("2.5.16", sha256="39fe57de6a52dc83c8a9ece90b8484d8d2b764e24e22e30ba5dc018328019a4d")
    version("2.5.15", sha256="a5ea5b98bb8d4054961f7bc82f458b4a9ef60c5e2dedcaba23a8e4363c2e6dfc")
    version("2.5.14", sha256="2ace5c964fb4b45279544669950412dbe4e86908c03bd5ebc8c8d306e458e97d")
    version("2.4.12", sha256="fcffc223897e14f2b5dce2db1c832f297cc43a1204e4b3fd713f1dc410e956e4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    build_directory = "spack-build"
    cmake_dir = os.path.join(build_directory, "CMakeBuild")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"bison )\s+(\S+)", output)
        return match.group(1) if match else None
