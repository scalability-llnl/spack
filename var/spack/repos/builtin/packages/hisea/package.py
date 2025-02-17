# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hisea(MakefilePackage):
    """HISEA is an efficient all-vs-all long read aligner for SMRT sequencing
    data. Its algorithm is designed to produce highest alignment sensitivity
    among others."""

    homepage = "https://doi.org/10.1186/s12859-017-1953-9"

    license("GPL-3.0-only")

    version(
        "2017.12.26",
        sha256="3c6ddfb8490a327cc5f9e45f64cd4312abc6ef5719661ce8892db8a20a1e9c5e",
        url="https://github.com/lucian-ilie/HISEA/tarball/39e01e98caa0f2101da806ca59306296effe789c",
    )

    depends_on("cxx", type="build")  # generated
    depends_on("boost")

    def patch(self):
        if self.spec.target.family == "aarch64":
            filter_file("-mpopcnt", "", "Makefile")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("hisea", prefix.bin)
