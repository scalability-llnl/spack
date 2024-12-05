# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cjson(CMakePackage):
    """Ultralightweight JSON parser in ANSI C."""

    homepage = "https://github.com/DaveGamble/cJSON"
    git = "https://github.com/DaveGamble/cJSON"
    url = "https://github.com/DaveGamble/cJSON/archive/refs/tags/v1.7.15.zip"

    license("MIT")

    version("1.7.18", sha256="cc6d93cc3b659037c34193ecc7be5a874a18c2ac67b24efe82db6a759b486b5d")
    version("1.7.17", sha256="51f3b07aece8d1786e74b951fd92556506586cb36670741b6bfb79bf5d484216")
    version("1.7.15", sha256="c55519316d940757ef93a779f1db1ca809dbf979c551861f339d35aaea1c907c")
