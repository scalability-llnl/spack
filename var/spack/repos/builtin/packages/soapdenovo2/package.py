# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Soapdenovo2(MakefilePackage):
    """SOAPdenovo is a novel short-read assembly method that can build a de
    novo draft assembly for the human-sized genomes. The program is
    specially designed to assemble Illumina GA short reads. It creates
    new opportunities for building reference sequences and carrying out
    accurate analyses of unexplored genomes in a cost effective way."""

    homepage = "https://github.com/aquaskyline/SOAPdenovo2"
    url = "https://github.com/aquaskyline/SOAPdenovo2/archive/r240.tar.gz"
    maintainers("snehring")

    license("GPL-3.0-only")

    version("242", sha256="a0043ceb41bc17a1c3fd2b8abe4f9029a60ad3edceb2b15af3c2cfabd36aa11b")
    version("240", sha256="cc9e9f216072c0bbcace5efdead947e1c3f41f09baec5508c7b90f933a090909")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def flag_handler(self, name, flags):
        if name.lower() == "cflags" and self.spec.satisfies("%gcc@10:"):
            flags.append("-fcommon")
        if name.lower() in ["cflags", "cxxflags", "cppflags"]:
            opt_flag = re.compile("-O.*")
            # This package cannot compile with any optimization flag other
            # than the -O3 specified in the makefile
            flags = [f for f in flags if not opt_flag.match(f)]
        return (flags, None, None)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("SOAPdenovo-63mer", prefix.bin)
        install("SOAPdenovo-127mer", prefix.bin)
