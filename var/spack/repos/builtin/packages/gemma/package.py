# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gemma(MakefilePackage):
    """GEMMA is a software toolkit for fast application of linear mixed models
    (LMMs) and related models to genome-wide association studies (GWAS) and
    other large-scale data sets."""

    homepage = "https://github.com/genetics-statistics/GEMMA"
    url = "https://github.com/genetics-statistics/GEMMA/archive/refs/tags/v0.98.5.tar.gz"

    maintainers("snehring", "dlkuehn")

    license("GPL-3.0-or-later")

    version("0.98.5", sha256="3ed336deee29e370f96ec8f1a240f7b62550e57dcd1694245ce7ec8f42241677")

    depends_on("cxx", type="build")  # generated

    depends_on("zlib-api")
    # openblas is the default
    # other lapack implementors can be made to work
    # but must provide cblas, blas, and lapack libs
    depends_on("openblas")
    depends_on("gsl@2:")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("bin/gemma", prefix.bin)
