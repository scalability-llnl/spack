# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class JwtCpp(CMakePackage):
    """A header only library for creating and validating JSON Web Tokens in C++11."""

    homepage = "https://thalhammer.github.io/jwt-cpp/"
    url = "https://github.com/Thalhammer/jwt-cpp/archive/refs/tags/v0.4.0.tar.gz"

    maintainers("gartung", "greenc-FNAL", "marcmengel", "vitodb")

    license("MIT")

    version("0.7.0", sha256="b9eb270e3ba8221e4b2bc38723c9a1cb4fa6c241a42908b9a334daff31137406")
    version("0.6.0", sha256="0227bd6e0356b211341075c7997c837f0b388c01379bd256aa525566a5553f03")
    version("0.5.2", sha256="d3188f9611597eb1bb285169879e1d87202bf10a08e4e7734c9f2097bfd4a850")
    version("0.5.1", sha256="d8f5ffb361824630b3b6f4aad26c730c915081071040c232ac57947d6177ef4f")
    version("0.5.0", sha256="079a273f070dd11213e301712319a65881e51ab81535cc436d5313191df852a2")
    version("0.4.0", sha256="f0dcc7b0e8bef8f9c3f434e7121f9941145042c9fe3055a5bdd709085a4f2be4")

    depends_on("cxx", type="build")  # generated

    # TODO: jwt-cpp>=0.5.0 has an embedded copy of picojson which can be packaged seperately

    # TODO: jwt-cpp>=0.6.0 supports wolfSSL for which there is currently
    # no Spack recipe.
    variant(
        "ssl",
        default="openssl",
        values=("openssl", "libressl"),
        multi=False,
        when="@0.5.0:",
        description="SSL library to use",
    )

    depends_on("openssl@1.0.2:", when="@0.4.0:0.4.99")
    depends_on("openssl@1.0.2:", when="@0.5.0:0.5.99 ssl=openssl")
    depends_on("openssl@1.0.1:", when="@0.6.0: ssl=openssl")
    depends_on("libressl@3:", when="@0.5.0: ssl=libressl")
    depends_on("nlohmann-json", when="@0.7.0:")

    def cmake_args(self):
        spec = self.spec
        define = self.define
        args = []
        if spec.satisfies("@0.5.0:"):
            ssl_library_dict = {"openssl": "OpenSSL", "libressl": "LibreSSL"}
            args.append(define("JWT_SSL_LIBRARY", ssl_library_dict[spec.variants["ssl"].value]))
            args += [define("JWT_BUILD_TESTS", False), define("JWT_BUILD_EXAMPLES", False)]
        else:
            args.append(define("BUILD_TESTS", False))
        return args
