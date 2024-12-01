# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fq(Package):
    """fq is a library to generate and validate FASTQ file pairs.

    fq provides subcommands for filtering, generating, subsampling, and validating FASTQ files."""

    homepage = "https://github.com/stjude-rust-labs/fq"
    url = "https://github.com/stjude-rust-labs/fq/archive/refs/tags/v0.10.0.tar.gz"
    maintainers("pabloaledo")

    license("MIT")

    version("0.10.0", sha256="34007ab71a873e1b066d910e90c5bdac3dcc4299ae6c9891ac6d8233cffeabb8")

    depends_on("rust")

    def install(self, spec, prefix):
        cargo = which("cargo")
        cargo("install", "--root", prefix, "--path", ".")
