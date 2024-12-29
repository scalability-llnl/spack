# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TclTclxml(AutotoolsPackage):
    """TclXML is an API for parsing XML documents using the Tcl scripting
    language. It is also a package including a DOM implementation (TclDOM) and
    XSL Transformations (TclXSLT). These allow Tcl scripts to read, manipulate
    and write XML documents."""

    homepage = "https://tclxml.sourceforge.net/tclxml.html"
    url = "https://sourceforge.net/projects/tclxml/files/TclXML/3.2/tclxml-3.2.tar.gz"
    list_url = "https://sourceforge.net/projects/tclxml/files/TclXML/"
    list_depth = 1

    version("3.2", sha256="f4116b6680b249ce74b856a121762361ca09e6256f0c8ad578d1c661b822cb39")
    version("3.1", sha256="9b017f29c7a06fa1a57d1658bd1d3867297c26013604bdcc4d7b0ca2333552c9")

    depends_on("c", type="build")  # generated

    extends("tcl")

    depends_on("tcl-tcllib")
    depends_on("libxml2")
    depends_on("libxslt")

    # Results in C99 build error
    conflicts("%apple-clang@12:")

    def configure_args(self):
        return [
            "--exec-prefix={0}".format(self.prefix),
            "--with-tcl={0}".format(self.spec["tcl"].libs.directories[0]),
            "--with-xml2-config={0}".format(self.spec["libxml2"].prefix.bin.join("xml2-config")),
            "--with-xslt-config={0}".format(self.spec["libxslt"].prefix.bin.join("xslt-config")),
        ]
