# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Dsrc(MakefilePackage):
    """DNA Sequence Reads Compression is an application designed for
    compression of data files containing reads from DNA sequencing in
    FASTQ format."""

    homepage = "http://sun.aei.polsl.pl/dsrc"
    url = "https://github.com/refresh-bio/DSRC/archive/v2.0.2.tar.gz"

    version("2.0.2", sha256="6d7abe0d72a501054a2115ccafff2e85e6383de627ec3e94ff4f03b7bb96a806")

    depends_on("cxx", type="build")  # generated

    parallel = False

    def install(self, spec, prefix):
        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)
        install_tree("include", prefix.include)
        install_tree("examples", prefix.examples)
