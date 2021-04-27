# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRanger(RPackage):
    """A Fast Implementation of Random Forests

    A fast implementation of Random Forests, particularly suited for high
    dimensional data. Ensembles of classification, regression, survival and
    probability prediction trees are supported. Data from genome-wide
    association studies can be analyzed efficiently. In addition to data
    frames, datasets of class 'gwaa.data' (R package 'GenABEL') and 'dgCMatrix'
    (R package 'Matrix')  can be directly analyzed."""

    homepage = "https://cloud.r-project.org/package=ranger"
    url      = "https://cloud.r-project.org/src/contrib/ranger_0.8.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ranger"

    version('0.12.1', sha256='fc308e0ac06718272799928e1a19612de16b05bde481d8f38e11a101df5425ef')
    version('0.11.2', sha256='13ac8a9433fdd92f62f66de44abc52477dcbb436b2045c1947951a266bffbeeb')
    version('0.11.1', sha256='999fb114602e27601ff0fe8ab461c39d667c6f5e8434e7feb3d21c7caf0dcffb')
    version('0.8.0', sha256='7f0fdee2f2d553a0aec56c2a4a4ff9dd972e1c7284118d9ea570749e0eaaabb9')
    version('0.7.0', sha256='83f4b06c6e63da979a20b757aaf0042928db453c12d89281afd40046e6b5393c')
    version('0.6.0', sha256='2759c2a3271098a4cfb63cd3ea68acaf645c92cb24c86fba098ada06e2e298bb')
    version('0.5.0', sha256='bc55811e723c9076c35aac4d82f29770ef84b40846198235d8b0ea9a4e91f144')
    version('0.4.0', sha256='d9f5761c3b07357aa586270cf7cbc97fc3db56ba731b6d0f3baf296f635f2be5')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-rcpp@0.11.2:', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-rcppeigen', type=('build', 'run'))
