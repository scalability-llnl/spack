# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class XercesC(AutotoolsPackage):
    """Xerces-C++ is a validating XML parser written in a portable subset of
    C++. Xerces-C++ makes it easy to give your application the ability to read
    and write XML data. A shared library is provided for parsing, generating,
    manipulating, and validating XML documents using the DOM, SAX, and SAX2
    APIs."""

    homepage = "https://xerces.apache.org/xerces-c"
    url = "https://archive.apache.org/dist/xerces/c/3/sources/xerces-c-3.2.1.tar.bz2"

    license("Apache-2.0")

    version("3.2.5", sha256="1db4028c9b7f1f778efbf4a9462d65e13f9938f2c22f9e9994e12c49ba97e252")
    version("3.2.4", sha256="74aa626fc71e729ee227602870dd29a5a01cd8c9c1c7330837a51da2eb5722cc")
    version("3.2.3", sha256="45c2329e684405f2b8854ecbddfb8d5b055cdf0fe4d35736cc352c504989bbb6")
    version("3.2.2", sha256="1f2a4d1dbd0086ce0f52b718ac0fa4af3dc1ce7a7ff73a581a05fbe78a82bce0")
    version("3.2.1", sha256="a36b6e162913ec218cfb84772d2535d43c3365355a601d45d4b8ce11f0ece0da")
    version("3.1.4", sha256="9408f12c1628ecf80730bedbe8b2caad810edd01bb4c66f77b60c873e8cc6891")
    version("3.1.3", sha256="fc5e5e0247b108b8d64d75aeb124cabdee9b7fcd725a89fe2242b4637b25c1fa")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Whilst still using Autotools, can use full cxxstd with 'default'
    # If build is moved to CMake, then will also need a patch to Xerces-C's
    # CMakeLists.txt as a specific standard cannot be forced
    variant(
        "cxxstd",
        default="default",
        values=("default", "98", "11", "14", "17", "20"),
        multi=False,
        description="Use the specified C++ standard when building",
    )

    variant(
        "netaccessor",
        default="curl",
        # todo: add additional values (platform-specific)
        # 'socket', 'cfurl', 'winsock'
        values=("curl", "none"),
        multi=False,
        description="Net Accessor (used to access network resources",
    )

    # It's best to be explicit about the transcoder or else xerces may
    # choose another value.
    if sys.platform == "darwin":
        default_transcoder = "macos"
    elif sys.platform.startswith("win") or sys.platform == "cygwin":
        default_transcoder = "windows"
    else:
        default_transcoder = "gnuiconv"

    variant(
        "transcoder",
        default=default_transcoder,
        values=("gnuiconv", "iconv", "icu", "macos", "windows", "none"),
        multi=False,
        description="Use the specified transcoder",
    )

    depends_on("iconv", type="link", when="transcoder=gnuiconv")
    depends_on("icu4c", type="link", when="transcoder=icu")
    depends_on("curl", when="netaccessor=curl")

    # Pass flags to configure.  This is necessary for CXXFLAGS or else
    # the xerces default will override the spack wrapper.
    def flag_handler(self, name, flags):
        spec = self.spec

        # Need to pass -std flag explicitly
        if name == "cxxflags" and spec.variants["cxxstd"].value != "default":
            flags.append(
                getattr(self.compiler, "cxx{0}_flag".format(spec.variants["cxxstd"].value))
            )

        # There is no --with-pkg for gnuiconv.
        if name == "ldflags" and "transcoder=gnuiconv" in spec:
            flags.append(spec["iconv"].libs.ld_flags)

        return (None, None, flags)

    def configure_args(self):
        spec = self.spec
        args = []

        if "netaccessor=curl" in spec:
            args.append("--enable-netaccessor-curl")
        else:
            args.append("--disable-network")

        transcoder = spec.variants["transcoder"].value
        if transcoder == "none":
            args.append("--without-icu")
        elif transcoder == "icu":
            args.extend(["--enable-transcoder-icu", "--with-icu=" + spec["icu4c"].prefix])
        elif transcoder == "macos":
            args.append("--enable-transcoder-macosunicodeconverter")
        else:
            args.append("--enable-transcoder-" + transcoder)

        return args
