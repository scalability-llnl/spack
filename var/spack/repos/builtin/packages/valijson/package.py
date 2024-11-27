# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Valijson(CMakePackage):
    """Header-only C++ library for JSON Schema validation,
    with support for many popular parsers."""

    homepage = "https://github.com/tristanpenman/valijson"
    url = "https://github.com/tristanpenman/valijson/archive/refs/tags/v1.0.tar.gz"
    git = "https://github.com/tristanpenman/valijson.git"

    license("BSD-2-Clause")

    version("master", branch="master")
    version("1.0.2", sha256="35d86e54fc727f1265226434dc996e33000a570f833537a25c8b702b0b824431")
    version("1.0", sha256="6b9f0bc89880feb3fe09aa469cd81f6168897d2fbb4e715853da3b94afd3779a")

    depends_on("cxx", type="build")  # generated
