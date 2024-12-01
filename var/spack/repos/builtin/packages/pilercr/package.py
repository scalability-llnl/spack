# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Pilercr(MakefilePackage):
    """Identification and analysis of CRISPR repeats."""

    homepage = "http://www.drive5.com/pilercr/"
    url = "http://www.drive5.com/pilercr/pilercr1.06.tar.gz"

    version("1.06", sha256="50175f7aa171674cda5ba255631f340f9cc7f80e8cc25135a4cb857147d91068")

    depends_on("cxx", type="build")  # generated

    @property
    def build_targets(self):
        targets = []
        targets.append("GPP = {0}".format(spack_cxx))
        targets.append("CFLAGS = -O3 -DNDEBUG=1")
        targets.append("LDLIBS = -lm")
        return targets

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("pilercr", prefix.bin)
