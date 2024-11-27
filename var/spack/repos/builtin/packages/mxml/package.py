# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mxml(AutotoolsPackage):
    """Mini-XML is a small XML library that you can use to read and write XML
    and XML-like data files in your application without requiring large
    non-standard libraries.
    """

    homepage = "https://michaelrsweet.github.io/mxml/"
    url = "https://github.com/michaelrsweet/mxml/releases/download/release-2.10/mxml-2.10.tar.gz"

    license("Apache-2.0")

    version("2.10", sha256="267ff58b64ddc767170d71dab0c729c06f45e1df9a9b6f75180b564f09767891")
    version("2.9", sha256="cded54653c584b24c4a78a7fa1b3b4377d49ac4f451ddf170ebbc8161d85ff92")
    version("2.8", sha256="0c9369f91a718d82e32cb007c0bd41b6642822c9a0ffe1d10eccbdea9a3011d5")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def url_for_version(self, version):
        if version <= Version("2.7"):
            return "https://github.com/michaelrsweet/mxml/archive/release-{0}.tar.gz".format(
                version
            )
        else:
            return "https://github.com/michaelrsweet/mxml/releases/download/release-{0}/mxml-{0}.tar.gz".format(
                version
            )

    def configure_args(self):
        return [
            # ADIOS build with -fPIC, so we need it too (avoid linkage issue)
            "CFLAGS={0}".format(self.compiler.cc_pic_flag),
            # Default is non-shared, but avoid any future surprises
            "--disable-shared",
        ]
