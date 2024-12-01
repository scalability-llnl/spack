# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSnprelate(RPackage):
    """Parallel Computing Toolset for Relatedness and Principal Component
    Analysis of SNP Data.

    Genome-wide association studies (GWAS) are widely used to investigate
    the genetic basis of diseases and traits, but they pose many
    computational challenges. We developed an R package SNPRelate to provide
    a binary format for single-nucleotide polymorphism (SNP) data in GWAS
    utilizing CoreArray Genomic Data Structure (GDS) data files. The GDS
    format offers the efficient operations specifically designed for
    integers with two bits, since a SNP could occupy only two bits.
    SNPRelate is also designed to accelerate two key computations on SNP
    data using parallel computing for multi-core symmetric multiprocessing
    computer architectures: Principal Component Analysis (PCA) and
    relatedness analysis using Identity-By-Descent measures. The SNP GDS
    format is also used by the GWASTools package with the support of S4
    classes and generic functions. The extended GDS format is implemented in
    the SeqArray package to support the storage of single nucleotide
    variations (SNVs), insertion/deletion polymorphism (indel) and
    structural variation calls."""

    bioc = "SNPRelate"

    version("1.34.0", commit="27a7c9658b974f9887f48a4a3ed1a7621b141488")
    version("1.32.0", commit="2e8cc807baa74fca5137148b672f3945c36689b2")
    version("1.30.1", commit="baef8a71d3908287a2307768348c02db0720d125")
    version("1.28.0", commit="8fcd837f4627a3bb77cb8d992b2baedd0589d123")
    version("1.24.0", commit="419b13b761ea39a8b1b9bc73097fb0359c59f1c2")
    version("1.18.1", commit="81c581bf76392efdc8ba237ca2e42ca1dba788ca")
    version("1.16.0", commit="0e38e8df4af87dff6c27a23af2867661998c0d85")
    version("1.14.0", commit="9501cbfc411aa320e58654a865fda2e9077977af")
    version("1.12.2", commit="dce2e2b6f36483a9f905bb5df6ae834a9f1136fe")
    version("1.10.2", commit="3f5c4010871df742e7a460586b38ad0c2fd37aeb")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@2.15:", type=("build", "run"))
    depends_on("r-gdsfmt@1.8.3:", type=("build", "run"))
