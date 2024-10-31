# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cityhash(AutotoolsPackage):
    """CityHash, a family of hash functions for strings."""

    homepage = "https://github.com/google/cityhash"
    git = "https://github.com/google/cityhash.git"

    version("master", branch="master")
    version("2013-07-31", commit="8af9b8c2b889d80c22d6bc26ba0df1afb79a30db")

    depends_on("cxx", type="build")  # generated

    def configure_args(self):
        return ["--enable-sse4.2"]
