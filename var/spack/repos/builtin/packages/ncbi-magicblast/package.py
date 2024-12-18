# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class NcbiMagicblast(AutotoolsPackage):
    """Magic-BLAST is a tool for mapping large next-generation RNA or DNA
    sequencing runs against a whole genome or transcriptome."""

    homepage = "https://ncbi.github.io/magicblast/"
    url = "ftp://ftp.ncbi.nlm.nih.gov/blast/executables/magicblast/1.3.0/ncbi-magicblast-1.3.0-src.tar.gz"

    version("1.5.0", sha256="b261914d9f7ffc0e655079ceba3e348ba11df1a1f73c4e47a4b1ca154754985c")
    version("1.3.0", sha256="47b9b65d595b5cb0c4fef22bc7f7c038fb8d4a0accdbe560d7232820575aff67")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cpio", type="build")
    depends_on("lmdb")

    configure_directory = "c++"

    def configure_args(self):
        return ["--without-internal"]
