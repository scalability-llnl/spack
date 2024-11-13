# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class BamReadcount(CMakePackage):
    """Bam-readcount generates metrics at single nucleotide positions."""

    homepage = "https://github.com/genome/bam-readcount"
    url = "https://github.com/genome/bam-readcount/archive/v0.8.0.tar.gz"

    license("MIT")

    version("1.0.1", sha256="8ebf84d9efee0f2d3b43f0452dbf16b27337c960e25128f6a7173119e62588b8")
    version("0.8.0", sha256="4f4dd558e3c6bfb24d6a57ec441568f7524be6639b24f13ea6f2bb350c7ea65f")

    depends_on("cxx", type="build")  # generated

    def setup_build_environment(self, env):
        env.append_flags("CFLAGS", self.compiler.cc_pic_flag)
