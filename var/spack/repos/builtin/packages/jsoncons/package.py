# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Jsoncons(CMakePackage):
    """A C++, header-only library for constructing JSON and JSON-like
    data formats, with JSON Pointer, JSON Patch, JSON Schema,
    JSONPath, JMESPath, CSV, MessagePack, CBOR, BSON, UBJSON
    """

    homepage = "https://danielaparker.github.io/jsoncons/"
    url = "https://github.com/danielaparker/jsoncons/archive/refs/tags/v1.2.0.tar.gz"

    license("BSL-1.0", checked_by="pranav-sivaraman")

    version("1.2.0", sha256="3bdc0c8ceba1943b5deb889559911ebe97377971453a11227ed0a51a05e5d5d8")

    depends_on("cxx", type="build")

    def cmake_args(self):
        return [self.define("JSONCONS_BUILD_TESTS", self.run_tests)]
