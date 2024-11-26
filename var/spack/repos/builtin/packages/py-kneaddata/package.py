# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKneaddata(PythonPackage):
    """
    Quality control tool on metagenomic and metatranscriptomic sequencing data,
    especially data from microbiome experiments
    """

    homepage = "https://github.com/biobakery/kneaddata"
    pypi = "kneaddata/kneaddata-0.12.0.tar.gz"

    version("0.12.0", sha256="b211bf973ea50cc89dd5935761ca3b101d422cfb62b215aae08f5ed92a624a58")

    maintainers("Pandapip1")

    depends_on("py-setuptools", type="build")
    depends_on("trimmomatic@0.33", type=("build", "run"))
    depends_on("bowtie2@2.2:", type=("build", "run"))
    depends_on("python", type=("build", "run"))
    depends_on("java", type=("build", "run"))

    variant("bam", default=True, description="Enable support for input files in BAM format")
    depends_on("samtools", when="+bam", type=("build", "run"))

    variant("trf", default=True, description="Enable support for Tandem Repeats Finder")
    depends_on("trf", when="+trf", type=("build", "run"))

    variant("fastqc", default=True, description="Enable support for FastQC")
    depends_on("fastqc", when="+fastqc", type=("build", "run"))
