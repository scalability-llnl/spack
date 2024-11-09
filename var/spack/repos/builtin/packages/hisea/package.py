# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


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

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants)

    def patch(self):
        if self.spec.target.family == "aarch64":
            filter_file("-mpopcnt", "", "Makefile")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("hisea", prefix.bin)
