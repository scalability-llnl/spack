# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Davix(CMakePackage):
    """High-performance file management over WebDAV/HTTP."""

    homepage = "https://davix.web.cern.ch/davix/docs/devel/index.html"
    url = "https://github.com/cern-fts/davix/releases/download/R_0_8_7/davix-0.8.7.tar.gz"

    maintainers("gartung", "greenc-FNAL", "marcmengel", "vitodb")

    license("LGPL-2.1-or-later")

    version("0.8.7", sha256="78c24e14edd7e4e560392d67147ec8658c2aa0d3640415bdf6bc513afcf695e6")
    version("0.8.6", sha256="7383b6f6595c77a9dc8c03c5483c67dc32bd6d23751e956cf9c174768e7eeb5b")
    version("0.8.5", sha256="f9ce21bcc2ed248f7825059d17577876616258c35177d74fad8f854a818a87f9")
    version("0.8.4", sha256="519d56f746e86ea3fd615bc49e559b520df07e051e1ca3d8c092067958f3b2b7")
    version("0.8.3", sha256="7e30b5541e08d32dbf5ae03c6bcabeaec063aec10a6647787822227b4541ae3e")
    version("0.8.2", sha256="8817a24c23f1309b9de233b9a882455f457c42edc2a649dc70fe2524cf76d94c")
    version(
        "0.8.1",
        sha256="582e407a8192265f81d88870bfc99bf63effa1ba49913b4837aeafa4251134a6",
        url="https://github.com/cern-fts/davix/releases/download/R_0_8_1-1/davix-0.8.1.tar.gz",
    )
    version(
        "0.8.0",
        sha256="215f6d5e5ac172164bf0fd18f2e536c610784960152736b8859215bf30bc539a",
        url="https://github.com/cern-fts/davix/releases/download/R_0_8_0-1/davix-0.8.0.tar.gz",
    )
    version("0.7.6", sha256="a2e7fdff29f7ba247a3bcdb08ab1db6d6ed745de2d3971b46526986caf360673")
    version("0.7.5", sha256="d920ca976846875d83af4dc50c99280bb3741fcf8351d5733453e70fa5fe6fc8")
    version(
        "0.7.3",
        sha256="cd46276e72c6a0da1e2ad30eb66ec509a4c023687767c62a66713fa8c23d328a",
        deprecated=True,
    )
    version(
        "0.6.9",
        sha256="fbd97eb5fdf82ca48770d06bf8e2805b35f23255478aa381a9d25a49eb98e348",
        deprecated=True,
    )
    version(
        "0.6.8",
        sha256="e1820f4cc3fc44858ae97197a3922cce2a1130ff553b080ba19e06eb8383ddf7",
        deprecated=True,
    )

    variant(
        "cxxstd",
        default="11",
        values=("11", "14", "17"),
        multi=False,
        description="Use the specified C++ standard when building.",
    )

    depends_on("pkgconfig", type="build")
    depends_on("libxml2")
    depends_on("uuid")
    depends_on("openssl")
    depends_on("curl")
    depends_on("rapidjson", when="@0.8.7:")

    variant("thirdparty", default=False, description="Build vendored libraries")
    depends_on("gsoap", when="+thirdparty")

    def cmake_args(self):
        cmake_args = [
            self.define_from_variant("CMAKE_CXX_STANDARD", variant="cxxstd"),
            self.define_from_variant("ENABLE_THIRD_PARTY_COPY", variant="thirdparty"),
        ]

        # Disable the use of embedded packages; use Spack to fetch them instead.
        cmake_args.append("-DEMBEDDED_LIBCURL=OFF")

        if "darwin" in self.spec.architecture:
            cmake_args.append("-DCMAKE_MACOSX_RPATH=ON")
        return cmake_args
