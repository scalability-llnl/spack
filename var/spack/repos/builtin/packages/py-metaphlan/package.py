# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMetaphlan(PythonPackage):
    """MetaPhlAn is a computational tool for profiling the composition of
    microbial communities (Bacteria, Archaea and Eukaryotes) from metagenomic
    shotgun sequencing data (i.e. not 16S) with species-level."""

    homepage = "https://github.com/biobakery/MetaPhlAn/"
    pypi = "MetaPhlAn/MetaPhlAn-4.0.2.tar.gz"

    version("4.0.2", sha256="2549fdf2de97a0024551a7bb8d639613b8a7b612054506c88cdb719353f466ff")
    version("3.1.0", sha256="4e7a7a36d07ed6f4f945afc4216db7f691d44a22b059c2404c917a160a687a6b")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-biom-format", type=("build", "run"))
    depends_on("py-biopython", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-hclust2", type=("build", "run"), when="@4.0.2:")
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-dendropy", type=("build", "run"))
    depends_on("py-pysam", type=("build", "run"))
    depends_on("py-cmseq", type=("build", "run"))
    depends_on("py-phylophlan", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("bowtie2@2.3:", type=("build", "run"))
    depends_on("muscle@3.8.1551:", type=("build", "run"))
    depends_on("blast-plus@2.6:", type=("build", "run"))
    depends_on("raxml@8.2.10:", type=("build", "run"))
    depends_on("samtools@1.9:", type=("build", "run"))
