# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Pugixml(CMakePackage):
    """Light-weight, simple, and fast XML parser for C++ with XPath support"""

    homepage = "https://pugixml.org/"
    url = "https://github.com/zeux/pugixml/releases/download/v1.10/pugixml-1.10.tar.gz"

    license("MIT")

    version("1.14", sha256="2f10e276870c64b1db6809050a75e11a897a8d7456c4be5c6b2e35a11168a015")
    version("1.13", sha256="40c0b3914ec131485640fa57e55bf1136446026b41db91c1bef678186a12abbe")
    version("1.11.4", sha256="8ddf57b65fb860416979a3f0640c2ad45ddddbbafa82508ef0a0af3ce7061716")
    version("1.11", sha256="26913d3e63b9c07431401cf826df17ed832a20d19333d043991e611d23beaa2c")
    version("1.10", sha256="55f399fbb470942410d348584dc953bcaec926415d3462f471ef350f29b5870a")
    version("1.8.1", sha256="929c4657c207260f8cc28e5b788b7499dffdba60d83d59f55ea33d873d729cd4")

    depends_on("cxx", type="build")  # generated

    variant("pic", default=True, description="Build position-independent code")
    variant("shared", default=True, description="Build shared libraries")

    conflicts("+shared", when="~pic")

    def cmake_args(self):
        return [
            self.define("BUILD_SHARED_AND_STATIC_LIBS", False),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
        ]
