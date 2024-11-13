# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Smartdenovo(MakefilePackage):
    """SMARTdenovo is a de novo assembler for PacBio and Oxford Nanopore
    (ONT) data."""

    homepage = "https://github.com/ruanjue/smartdenovo"
    git = "https://github.com/ruanjue/smartdenovo.git"

    license("GPL-3.0-only")

    version("master", branch="master")

    depends_on("c", type="build")  # generated

    depends_on("sse2neon", when="target=aarch64:")

    patch(
        "aarch64.patch",
        sha256="7dd4bca28aafb0680cc1823aa58ac9000819993538e92628554666c4b3acc470",
        when="target=aarch64:",
    )
    patch(
        "inline-limit.patch",
        sha256="9f514ed72c37cf52ee2ffbe06f9ca1ed5a3e0819dab5876ecd83107c5e5bed81",
    )

    def install(self, spec, prefix):
        install_files = [
            "pairaln",
            "wtpre",
            "wtcyc",
            "wtmer",
            "wtzmo",
            "wtobt",
            "wtclp",
            "wtext",
            "wtgbo",
            "wtlay",
            "wtcns",
            "wtmsa",
        ]
        mkdirp(prefix.bin)
        for f in install_files:
            install(f, prefix.bin)
