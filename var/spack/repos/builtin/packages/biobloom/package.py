# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Biobloom(AutotoolsPackage):
    """BioBloom Tools (BBT) provides the means to create filters for a given
    reference and then to categorize sequences."""

    homepage = "https://github.com/bcgsc/biobloom"
    url = "https://github.com/bcgsc/biobloom/releases/download/2.2.0/biobloomtools-2.2.0.tar.gz"

    version("2.3.5", sha256="03fbc0d0fc867f76d64f756d556598e5fe5f015363df8f97fbed4cfd541c6749")
    version("2.2.0", sha256="5d09f8690f0b6402f967ac09c5b0f769961f3fe3791000f8f73af6af7324f02c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("boost+exception+math+serialization+container")
    depends_on("sdsl-lite")
    depends_on("sparsehash")
    depends_on("zlib-api")

    def configure_args(self):
        # newer versions of sdsl-lite introduce tolerable warnings
        # they must disabled to allow the build to continue

        return ["CXXFLAGS=-w", "CPPFLAGS=-w"]
