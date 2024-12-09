# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Orfm(AutotoolsPackage):
    """A simple and not slow open reading frame (ORF) caller. No bells or
    whistles like frameshift detection, just a straightforward goal of
    returning a FASTA file of open reading frames over a certain length
    from a FASTA/Q file of nucleotide sequences."""

    homepage = "https://github.com/wwood/OrfM"
    url = "https://github.com/wwood/OrfM/releases/download/v0.7.1/orfm-0.7.1.tar.gz"

    version("0.7.1", sha256="19f39c72bcc48127b757613c5eef4abae95ee6c82dccf96b041db527b27f319a")

    depends_on("c", type="build")  # generated

    depends_on("zlib-api", type="link")
