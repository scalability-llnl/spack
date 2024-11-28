# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Aom(CMakePackage):
    """Alliance for Open Media AOM AV1 Codec Library"""

    homepage = "https://aomedia.googlesource.com/aom"
    git = "https://aomedia.googlesource.com/aom"

    license("BSD-2-Clause AND AOM-Patent-License-1.0", checked_by="tgamblin")

    version("v1.0.0-errata1", commit="29d8ce4836630df5cc7ab58f1afc4836765fc212")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("yasm")

    def cmake_args(self):
        args = []
        args.append("-DBUILD_SHARED_LIBS=ON")
        return args
