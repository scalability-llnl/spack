# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPhylophlan(PythonPackage):
    """PhyloPhlAn 3.0 is an integrated pipeline for large-scale
    phylogenetic profiling of genomes and metagenomes."""

    homepage = "https://github.com/biobakery/phylophlan"
    url = "https://github.com/biobakery/phylophlan/archive/refs/tags/3.0.3.tar.gz"

    license("MIT")

    version("3.0.3", sha256="d8d0082c95d58d7b11a60c1e2214b35c1a23a65675005f1393e7647d76c6a054")
    version("3.0.2", sha256="c342116662bbfbb49f0665291fc7c0be5a0d04a02a7be2da81de0322eb2256b4")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-biopython@1.73:", type=("build", "run"))
    depends_on("py-dendropy@4.4.0:", type=("build", "run"))
    depends_on("py-matplotlib@3.1.0:", type=("build", "run"))
    depends_on("py-numpy@1.15.4:", type=("build", "run"))
    depends_on("py-pandas@0.24.2:", type=("build", "run"))
    depends_on("py-seaborn@0.9.0:", type=("build", "run"))
    depends_on("blast-plus@2.6.0:", type=("build", "run"))
    depends_on("diamond@0.9:", type=("build", "run"))
    depends_on("trimal@1.4.1:", type=("build", "run"))
    depends_on("muscle@3.8.1551:", type=("build", "run"))
    depends_on("mafft@7.310:", type=("build", "run"))
    depends_on("fasttree@2.1.8:", type=("build", "run"))
    depends_on("raxml@8.2.10:", type=("build", "run"))
    depends_on("iq-tree@2", type=("build", "run"))
    depends_on("mash", type=("build", "run"))
