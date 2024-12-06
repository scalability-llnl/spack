# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Bitsery(CMakePackage):
    """Header only C++ binary serialization library. It is designed around the
    networking requirements for real-time data delivery, especially for
    games."""

    homepage = "https://github.com/fraillt/bitsery"
    url = "https://github.com/fraillt/bitsery/archive/v5.1.0.tar.gz"

    license("MIT")

    version("5.1.0", sha256="8f46667db5d0b62fdaab33612108498bcbcbe9cfa48d2cd220b2129734440a8d")

    depends_on("cxx", type="build")  # generated
