# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPscbs(RPackage):
    """Segmentation of allele-specific DNA copy number data and detection of
    regions with abnormal copy number within each parental chromosome. Both
    tumor-normal paired and tumor-only analyses are supported."""

    homepage = "https://github.com/HenrikBengtsson/PSCBS"
    url      = "https://cloud.r-project.org/src/contrib/PSCBS_0.65.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/PSCBS"

    version('0.65.0', sha256='3365065d5375c599eb024bfff12c5f6b10a6b1a4fe4ba6f200f7e83618dd399a')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-r-methodss3@1.7.1:', type=('build', 'run'))
    depends_on('r-r-oo@1.22.1:', type=('build', 'run'))
    depends_on('r-r-utils@2.8.0:', type=('build', 'run'))
    depends_on('r-r-cache@0.13.0:', type=('build', 'run'))
    depends_on('r-matrixstats@0.54.0:', type=('build', 'run'))
    depends_on('r-aroma-light@2.4.0:', type=('build', 'run'))
    depends_on('r-dnacopy@1.42.0:', type=('build', 'run'))
    depends_on('r-listenv@0.7.0:', type=('build', 'run'))
    depends_on('r-future@1.12.0:', type=('build', 'run'))
