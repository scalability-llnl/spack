# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dcmtk(CMakePackage):
    """DCMTK is a collection of libraries and applications implementing large
    parts of the DICOM standard."""

    homepage = "https://dicom.offis.de"
    url = "https://github.com/DCMTK/dcmtk/archive/DCMTK-3.6.3.tar.gz"

    license("BSD-3-Clause", checked_by="wdconinc")

    version("3.6.8", sha256="fca429a215739702fe8d96178964036246a35e2ea8adb12da33851e2be8e9a07")
    version("3.6.7", sha256="17705dcdb2047d1266bb4e92dbf4aa6d4967819e8e3e94f39b7df697661b4860")
    version("3.6.6", sha256="117097da6d50ddbad0e48bb1e6cdc61468e82ba1d32001dd8e2366b445133a8c")
    version("3.6.5", sha256="37dad355d5513b4de4a86b5b7b0c3e9ec059860d88781b80916bba2a04e6d5b8")
    version("3.6.4", sha256="e4b1de804a3fef38fe8cb9edd00262c3cbbd114b305511c14479dd888a9337d2")
    version("3.6.3", sha256="57f4f71ee4af9114be6408ff6fcafc441c349e4c2954e17c9c22c8ce0fb065bf")
    version("3.6.2", sha256="e9bf6e8805bbcf8a25274566541798785fd4e73bd046045ef27a0109ab520924")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    variant("ssl", default=True, description="Suuport DICOM Security Enhancements one")
    depends_on("openssl", type=("build", "link"), when="+ssl")

    variant(
        "zlib",
        default=True,
        description="Support 'Deflated Explicit VR Little Endian' Transfer Syntax",
    )
    depends_on("zlib-api", type=("build", "link"), when="+zlib")

    variant("tiff", default=True, description="Support for TIFF output")
    depends_on("libtiff", type=("build", "link"), when="+tiff")

    variant("png", default=True, description="Support for PNG output")
    depends_on("libpng", type=("build", "link"), when="+png")

    variant("xml", default=True, description="Support for XML input")
    depends_on("libxml2", type=("build", "link"), when="+xml")

    variant("iconv", default=True, description="Charset conversion support (iconv)")
    depends_on("iconv", type=("build", "link"))

    variant("pic", default=False, description="Produce position-independent code")
    variant("cxx11", default=False, description="Enable c++11 features")
    variant("stl", default=True, description="Use native STL implementation")

    conflicts("platform=darwin target=aarch64:", when="@:3.6.6")

    patch("tiff-3.6.7.patch", when="@3.6.7:3.6.8")

    def patch(self):
        # Backport 3.6.4
        if self.spec.satisfies("@:3.6.3 %fj"):
            filter_file(
                "OFintegral_constant<size_t,-1>",
                "OFintegral_constant<size_t,~OFstatic_cast(size_t,0)>",
                "ofstd/include/dcmtk/ofstd/variadic/helpers.h",
                string=True,
            )

    def cmake_args(self):
        args = [
            self.define_from_variant("DCMTK_WITH_OPENSSL", "ssl"),
            self.define_from_variant("DCMTK_WITH_ZLIB", "zlib"),
            self.define_from_variant("DCMTK_WITH_TIFF", "tiff"),
            self.define_from_variant("DCMTK_WITH_PNG", "png"),
            self.define_from_variant("DCMTK_WITH_XML", "xml"),
            self.define_from_variant("DCMTK_WITH_ICONV", "iconv"),
            self.define_from_variant("DCMTK_ENABLE_CXX11", "cxx11"),
            self.define_from_variant("DCMTK_ENABLE_STL", "stl"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
        ]
        return args
