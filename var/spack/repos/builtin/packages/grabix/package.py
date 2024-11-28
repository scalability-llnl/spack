# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Grabix(MakefilePackage):
    """Grabix leverages the fantastic BGZF library in samtools to provide
    random access into text files that have been compressed with bgzip.
    grabix creates it's own index (.gbi) of the bgzipped file. Once indexed,
    one can extract arbitrary lines from the file with the grab command.
    Or choose random lines with the, well, random command.
    """

    homepage = "https://github.com/arq5x/grabix"
    url = "https://github.com/arq5x/grabix/archive/v0.1.7.tar.gz"

    maintainers("robqiao")

    license("MIT")

    version("0.1.7", sha256="d90735c55c0985a4d751858d7ce9e36ad534fff4103257e8e981e34d5c915b28")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    conflicts("%gcc@7:", msg="grabix cannot be compiled with newer versions of GCC")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("LICENSE", prefix)
        install("simrep.chr1.bed", prefix)
        install("grabix", prefix.bin)
