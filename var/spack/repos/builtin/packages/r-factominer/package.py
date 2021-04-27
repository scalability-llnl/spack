# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RFactominer(RPackage):
    """Multivariate Exploratory Data Analysis and Data Mining

    Exploratory data analysis methods to summarize, visualize and describe
    datasets. The main principal component methods are available, those with
    the largest potential in terms of applications: principal component
    analysis (PCA) when variables are quantitative, correspondence analysis
    (CA) and multiple correspondence analysis (MCA) when variables are
    categorical, Multiple Factor Analysis when variables are structured in
    groups, etc. and hierarchical cluster analysis. F. Husson, S. Le and J.
    Pages (2017)."""

    homepage = "http://factominer.free.fr"
    url      = "https://cloud.r-project.org/src/contrib/FactoMineR_1.35.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/FactoMineR"

    version('2.4', sha256='b9e3adce9a66b4daccc85fa67cb0769d6be230beeb126921b386ccde5db2e851')
    version('1.42', sha256='4cd9efb3681767c3bd48ddc3504ebead1493fcbbc0a9f759a00955b16c3481fa')
    version('1.41', sha256='a9889d69e298b8a01e8d0a5a54260730e742c95681e367d759829aad9a8740c0')
    version('1.40', sha256='68cb778fe7581b55666a5ae4aa7a5e7fa3ecbd133ae8cff1b2371a737b6d95e8')
    version('1.39', sha256='b0bb1d6d7d1f3cb11a4b63c377321e10078a36f29bc78dfa3b80c7c149f4a08a')
    version('1.38', sha256='f13059c84c53f8761bd5a61e980f8609e2119e36c5d35233fc2baac93268086f')
    version('1.36', sha256='2198c3facaa41a23df6f9373d4ccb636b98a8810896e379e5deb686ab31b36de')
    version('1.35', sha256='afe176fe561d1d16c5965ecb2b80ec90a56d0fbcd75c43ec8025a401a5b715a9')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r@3.5.0:', when='@2.4:', type=('build', 'run'))
    depends_on('r-car', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-dt', when='@2.4:', type=('build', 'run'))
    depends_on('r-ellipse', type=('build', 'run'))
    depends_on('r-flashclust', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-leaps', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-scatterplot3d', type=('build', 'run'))
    depends_on('r-ggplot2', when='@2.4:', type=('build', 'run'))
    depends_on('r-ggrepel', when='@2.4:', type=('build', 'run'))
