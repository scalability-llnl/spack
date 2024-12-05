# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fastp(MakefilePackage):
    """A tool designed to provide fast
    all-in-one preprocessing for FastQ files."""

    homepage = "https://github.com/OpenGene/fastp"
    url = "https://github.com/OpenGene/fastp/archive/v0.20.0.tar.gz"

    license("MIT")

    version("0.23.4", sha256="4fad6db156e769d46071add8a778a13a5cb5186bc1e1a5f9b1ffd499d84d72b5")
    version("0.23.3", sha256="a37ee4b5dcf836a5a19baec645657b71d9dcd69ee843998f41f921e9b67350e3")
    version("0.20.0", sha256="8d751d2746db11ff233032fc49e3bcc8b53758dd4596fdcf4b4099a4d702ac22")

    depends_on("cxx", type="build")  # generated

    depends_on("libisal", type=("build", "link"), when="@0.23:")
    depends_on("libdeflate", type=("build", "link"), when="@0.23:")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        make("install", "PREFIX={0}".format(prefix))
