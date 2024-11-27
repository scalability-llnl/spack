# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bamaddrg(MakefilePackage):
    """bamaddrg adds read groups to input BAM files,
    streams BAM output on stdout"""

    homepage = "https://github.com/ekg/bamaddrg"
    url = "https://github.com/ilbiondo/bamaddrg/archive/v0.1.tar.gz"
    git = "https://github.com/ilbiondo/bamaddrg.git"

    version("0.1", sha256="725a689d8326d72f865837b231005a9211d6c70a25b7a3a754df4f90d2996355")

    depends_on("cxx", type="build")  # generated

    depends_on("bamtools", type="build")

    def setup_build_environment(self, env):
        env.set("BAMTOOLS_ROOT", self.spec["bamtools"].prefix)
        env.set("PREFIX", self.prefix)
