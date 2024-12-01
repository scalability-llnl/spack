# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cppcodec(CMakePackage):
    """Header-only C++11 library to encode/decode base64, base64url, base32,
    base32hex and hex (a.k.a. base16) as specified in RFC 4648, plus
    Crockford's base32. MIT licensed with consistent, flexible API."""

    maintainers("vmiheer")
    homepage = "https://github.com/tplgy/cppcodec"
    url = "https://github.com/tplgy/cppcodec/archive/refs/tags/v0.2.tar.gz"

    license("MIT")

    version("0.2", sha256="0edaea2a9d9709d456aa99a1c3e17812ed130f9ef2b5c2d152c230a5cbc5c482")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.8:", type="build")
