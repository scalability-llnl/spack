# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# See the Spack documentation for more information on packaging.

from spack.package import *


class Repeatscout(MakefilePackage):
    """RepeatScout - De Novo Repeat Finder, Price A.L., Jones N.C. and Pevzner
    P.A."""

    homepage = "https://www.repeatmasker.org/RepeatModeler/"
    url = "https://www.repeatmasker.org/RepeatScout-1.0.5.tar.gz"

    version("1.0.5", sha256="bda6f782382f2b7dcb6a004b7da586d5046b3c12429b158e24787be62de6199c")

    depends_on("perl", type="run")
    depends_on("trf", type="run")
    depends_on("nseg", type="run")

    def edit(self, spec, prefix):
        filter_file("^INSTDIR.*$", "INSTDIR=%s" % prefix.bin, "Makefile")
