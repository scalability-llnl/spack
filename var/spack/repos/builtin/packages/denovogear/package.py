# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Denovogear(CMakePackage):
    """DeNovoGear is a software package to detect de novo mutations using
    next-generation sequencing data. It supports the analysis of many
    differential experimental designs and uses advanced statistical models
    to reduce the false positve rate."""

    homepage = "https://github.com/denovogear/denovogear"
    url = "https://github.com/denovogear/denovogear/archive/v1.1.1.tar.gz"

    license("GPL-3.0-or-later")

    version("1.1.1", sha256="799fe99193e9cf12320893cf020a3251022f60a49de8677a1c5a18c578fe4be2")
    version("1.1.0", sha256="f818f80cd67183294c8aae312cad8311e6a9abede1f687567bb079d29f79c005")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.1:", type=("build"))
    depends_on(
        "boost@1.47:1.60"
        "+exception+filesystem+system+serialization+graph+iostreams+regex+math+container",
        type="build",
    )
    depends_on("htslib@1.2:", type=("build"))
    depends_on("eigen", type=("build"))
    depends_on("zlib-api", type=("link"))

    patch("stream-open.patch", when="@:1.1.1")
    # fix: ordered comparison between pointer and zero.
    patch("newmat6.cpp.patch")
