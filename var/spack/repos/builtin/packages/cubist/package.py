# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Cubist(MakefilePackage):
    """Cubist is a powerful tool for generating rule-based models that
    balance the need for accurate prediction against the requirements of
    intelligibility.

    Cubist models generally give better results than those
    produced by simple techniques such as multivariate linear regression,
    while also being easier to understand than neural networks."""

    homepage = "https://www.rulequest.com"
    url = "https://www.rulequest.com/GPL/Cubist.tgz"

    license("GPL-3.0-only")

    version("2.07", sha256="f2b20807cd3275e775c42263a4efd3f50df6e495a8b6dc8989ea2d41b973ac1a")

    depends_on("c", type="build")  # generated

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")
        makefile.filter("SHELL .*", "SHELL  = /bin/bash")

    def install(self, spec, prefix):
        mkdirp(self.prefix.bin)
        install("cubist", prefix.bin)
        install("summary", prefix.bin)
        install("xval", prefix.bin)
