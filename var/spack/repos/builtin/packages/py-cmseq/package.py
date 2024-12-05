# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCmseq(PythonPackage):
    """CMSeq is a set of commands to provide an interface
    to .bam files for coverage and sequence consensus."""

    homepage = "https://github.com/SegataLab/cmseq"
    pypi = "CMSeq/CMSeq-1.0.4.tar.gz"

    license("MIT")

    version("1.0.4", sha256="93038a6dba826e29a66df3ec8ab2b3e3872acac7af9df245e4a5a624584aca5c")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-bcbio-gff", type=("build", "run"))
    depends_on("samtools@1.2:", type=("build", "run"))
    depends_on("py-pysam", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-biopython@:1.76", type=("build", "run"))
    depends_on("py-setuptools@:57", type=("build"))
