# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Swipl(CMakePackage):
    """SWI-Prolog is a versatile implementation of the Prolog language.
    Although SWI-Prolog gained its popularity primarily in education,
    its development is mostly driven by the needs for application development.
    This is facilitated by a rich interface to other IT components by
    supporting many document types and (network) protocols as well as a
    comprehensive low-level interface to C that is the basis for high-level
    interfaces to C++, Java (bundled), C#, Python, etc (externally available).

    Data type extensions such as dicts and strings as well as full support
    for Unicode and unbounded integers simplify smooth exchange of data
    with other components."""

    homepage = "https://www.swi-prolog.org"
    url = "https://www.swi-prolog.org/download/stable/src/swipl-8.0.3.tar.gz"

    maintainers("alexrobomind")

    version("8.2.0", sha256="d8c9f3adb9cd997a5fed7b5f5dbfe971d2defda969b9066ada158e4202c09c3c")
    version("8.0.3", sha256="cee59c0a477c8166d722703f6e52f962028f3ac43a5f41240ecb45dbdbe2d6ae")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("gmp", default=True, description="bignum and rational number support")
    variant("xpce", default=True, description="GUI support")
    variant("ssl", default=True, description="SSL support")
    variant("zlib", default=True, description="Compressed streams support")
    variant("odbc", default=True, description="ODBC database access")
    variant("unwind", default=True, description="Build with stack traces in crash reports")
    variant("html", default=True, description="Install the HTML documentation")
    variant("pdfdoc", default=False, description="Build the PDF documentation")

    depends_on("uuid")
    depends_on("readline")

    depends_on("libarchive", when="+html")

    depends_on("gmp", when="+gmp")
    depends_on("unwind", when="+unwind")
    depends_on("unixodbc", when="+odbc")
    depends_on("openssl", when="+ssl")
    depends_on("zlib-api", when="+zlib")

    depends_on("libxt", when="+xpce")
    depends_on("libx11", when="+xpce")
    depends_on("libjpeg", when="+xpce")
    depends_on("libxpm", when="+xpce")

    depends_on("libxft", when="+xpce")
    depends_on("fontconfig", when="+xpce")
    depends_on("pkgconfig", when="+xpce", type="build")

    conflicts("%intel", msg="Test builds with ICC failed when creating startup image")

    def cmake_args(self):
        args = []

        def append_switch(variant, cmake_flag):
            val = "ON" if variant in self.spec else "OFF"

            flagdef = "-D" + cmake_flag + ":BOOL=" + val
            args.append(flagdef)

        append_switch("+gmp", "USE_GMP")
        append_switch("+xpce", "SWIPL_PACKAGES_X")
        append_switch("+odbc", "SWIPL_PACKAGES_ODBC")
        append_switch("+html", "INSTALL_DOCUMENTATION")
        append_switch("+pdfdoc", "BUILD_PDF_DOCUMENTATION")

        # The variants ssl and zlib are implicitly set up by CMake

        return args
