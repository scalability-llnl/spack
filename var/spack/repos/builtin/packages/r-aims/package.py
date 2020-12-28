# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAims(RPackage):
    """AIMS : Absolute Assignment of Breast Cancer Intrinsic Molecular Subtype.

       This package contains the AIMS implementation. It contains necessary
       functions to assign the five intrinsic molecular subtypes (Luminal A,
       Luminal B, Her2-enriched, Basal-like, Normal-like). Assignments could be
       done on individual samples as well as on dataset of gene expression
       data."""

    homepage = "https://bioconductor.org/packages/AIMS"
    git      = "https://git.bioconductor.org/packages/AIMS.git"

    version('1.16.0', commit='86cb8c998ade3003cd34a5405b218ae07d97bf84')
    version('1.14.1', commit='4125c4217a7e4f00169b5ba65dcc3778fdd33c6f')
    version('1.12.0', commit='d7eaa723d19a6aca37df244fd0b3d5426ed0a626')
    version('1.10.0', commit='972945980b39168502a02ac3aa396f9b99fb3d71')
    version('1.8.0', commit='86b866c20e191047492c51b43e3f73082c3f8357')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-e1071', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
