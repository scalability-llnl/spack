# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class XalanC(CMakePackage):
    """Xalan-C++ version is a robust implementation of the W3C Recommendations for
    XSL Transformations (XSLT) and the XML Path Language (XPath). It works with
    the Xerces-C++ XML parser.

    """

    homepage = "https://xalan.apache.org"
    url = "https://dlcdn.apache.org/xalan/xalan-c/sources/xalan_c-1.12.tar.gz"

    maintainers("omsai")

    license("Apache-2.0")

    version("1.12", sha256="ee7d4b0b08c5676f5e586c7154d94a5b32b299ac3cbb946e24c4375a25552da7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "transcoder",
        default="default",
        values=("default", "icu"),
        multi=False,
        description="Use the default UTF-16 transcoder or ICU",
    )

    depends_on("xerces-c@3:")
    depends_on("icu4c", type="link", when="transcoder=icu")

    def cmake_args(self):
        args = []

        if "transcoder=icu" in self.spec:
            args.append("-Dtranscoder=icu")

        return args
