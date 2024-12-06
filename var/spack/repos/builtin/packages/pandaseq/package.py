# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pandaseq(AutotoolsPackage):
    """PANDASEQ is a program to align Illumina reads, optionally with PCR
    primers embedded in the sequence, and reconstruct an overlapping
    sequence."""

    homepage = "https://github.com/neufeld/pandaseq"
    url = "https://github.com/neufeld/pandaseq/archive/v2.11.tar.gz"

    license("GPL-3.0-only")

    version("2.11", sha256="6e3e35d88c95f57d612d559e093656404c1d48c341a8baa6bef7bb0f09fc8f82")
    version("2.10", sha256="93cd34fc26a7357e14e386b9c9ba9b28361cf4da7cf62562dc8501e220f9a561")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type=("build", "link"))
    depends_on("m4", type="build")
    depends_on("zlib-api", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("bzip2", type="link")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")
