# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ngmlr(CMakePackage):
    """Ngmlr is a long-read mapper designed to align PacBilo or Oxford
    Nanopore to a reference genome with a focus on reads that span
    structural variations."""

    homepage = "https://github.com/philres/ngmlr"
    url = "https://github.com/philres/ngmlr/archive/v0.2.5.tar.gz"

    license("MIT")

    version("0.2.7", sha256="5126a6b3e726cac0da0713883daac688f38587f118428247a9a3ace5a55b29aa")
    version("0.2.5", sha256="719944a35cc7ff9c321eedbf3385a7375ce2301f609b3fd7be0a850cabbb028b")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api", type="link")
    depends_on("sse2neon", when="target=aarch64:")

    patch("for_aarch64.patch", when="target=aarch64:")
    patch("for_va_list.patch")
