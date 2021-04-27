# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RSeurat(RPackage):
    """Tools for Single Cell Genomics

    A toolkit for quality control, analysis, and exploration of single cell RNA
    sequencing data. 'Seurat' aims to enable users to identify and interpret
    sources of heterogeneity from single cell transcriptomic measurements, and
    to integrate diverse types of single cell data. See Satija R, Farrell J,
    Gennert D, et al (2015) <doi:10.1038/nbt.3192>, Macosko E, Basu A, Satija
    R, et al (2015) <doi:10.1016/j.cell.2015.05.002>, and Stuart T, Butler A,
    et al (2019) <doi:10.1016/j.cell.2019.05.031> for more details."""

    homepage = "http://satijalab.org/seurat/"
    url      = "https://cloud.r-project.org/src/contrib/Seurat_2.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Seurat"

    version('3.2.3', sha256='83aa48f75c3756bee23e108a8b01028366e24f237fe990cb441f3525e0613f87')
    version('3.1.0', sha256='d8d3fad2950a8f791376e3d20c72ea07c68bf8d82d800661cab5ce696db39d45')
    version('3.0.2', sha256='16df5dec6b41d49320c5bf5ce30eb3b7dedeea69b054b55b77528f2f2b7bce04')
    version('3.0.1', sha256='8c467bdbfdb9aff51bde6a897ff98a7389941f688639d8f1d36c71dde076a257')
    version('2.1.0', sha256='7d20d231b979a4aa63cd7dae7e725405212e8975889f12b8d779c6c896c10ac3')
    version('2.0.1', sha256='6aa33aa3afb29a8be364ab083c7071cfbc56ad042a019bcf6f939e0c8c7744f0')

    depends_on('r@3.2.0:', when='@:2.3.0', type=('build', 'run'))
    depends_on('r@3.4.0:', when='@2.3.1:', type=('build', 'run'))
    depends_on('r@3.6.0:', when='@3.2.3:', type=('build', 'run'))
    depends_on('r-cluster', when='@2.3.0:', type=('build', 'run'))
    depends_on('r-cowplot', type=('build', 'run'))
    depends_on('r-fitdistrplus', when='@2.3.0:', type=('build', 'run'))
    depends_on('r-future', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-future-apply', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-ggplot2@3.0.0:', type=('build', 'run'))
    depends_on('r-ggplot2@3.3.0:', when='@3.2.3:', type=('build', 'run'))
    depends_on('r-ggrepel', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-ggridges', when='@2.2.0:', type=('build', 'run'))
    depends_on('r-httr', when='@2.3.4:', type=('build', 'run'))
    depends_on('r-ica', type=('build', 'run'))
    depends_on('r-igraph', type=('build', 'run'))
    depends_on('r-irlba', type=('build', 'run'))
    depends_on('r-jsonlite', when='@3.2.3:', type=('build', 'run'))
    depends_on('r-kernsmooth', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-leiden@0.3.1:', when='@3.1.0:', type=('build', 'run'))
    depends_on('r-lmtest', when='@2.3.0:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-matrix@1.2.14:', type=('build', 'run'))
    depends_on('r-matrixstats', when='@3.2.3:', type=('build', 'run'))
    depends_on('r-miniui', when='@3.2.3:', type=('build', 'run'))
    depends_on('r-patchwork', when='@3.2.3:', type=('build', 'run'))
    depends_on('r-pbapply', type=('build', 'run'))
    depends_on('r-plotly', type=('build', 'run'))
    depends_on('r-plotly@4.9.0:', when='@3.2.3:', type=('build', 'run'))
    depends_on('r-png', when='@2.3.0:', type=('build', 'run'))
    depends_on('r-rann', when='@2.3.0:', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
    depends_on('r-rcppannoy', when='@3.1.0:', type=('build', 'run'))
    depends_on('r-reticulate', when='@2.3.1:', type=('build', 'run'))
    depends_on('r-rlang', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-rocr', type=('build', 'run'))
    depends_on('r-rsvd', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-rtsne', type=('build', 'run'))
    depends_on('r-scales', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-scattermore@0.7:', when='@3.2.3:', type=('build', 'run'))
    depends_on('r-sctransform@0.2.0:', when='@3.0.0:', type=('build', 'run'))
    depends_on('r-sctransform@0.3.1:', when='@3.2.3:', type=('build', 'run'))
    depends_on('r-shiny', when='@3.2.3:', type=('build', 'run'))
    depends_on('r-spatstat', when='@3.2.3:', type=('build', 'run'))
    depends_on('r-tibble', when='@3.2.3:', type=('build', 'run'))
    depends_on('r-uwot', when='@3.1.0:', type=('build', 'run'))
    depends_on('r-uwot@0.1.9:', when='@3.2.3:', type=('build', 'run'))
    depends_on('r-rcppeigen', type=('build', 'run'))
    depends_on('r-rcppprogress', type=('build', 'run'))
    depends_on('r-gplots', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-reshape2', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-ape', when='@:3.1.0', type=('build', 'run'))
    depends_on('r-tidyr', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-caret', when='@:2.3.2', type=('build', 'run'))
    depends_on('r-gdata', when='@:2.3.2', type=('build', 'run'))
    depends_on('r-gridextra', when='@:2.3.0', type=('build', 'run'))
    depends_on('r-hmisc', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-nmf', when='@:2.2.0', type=('build', 'run'))
    depends_on('r-fpc', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-lars', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-dtw', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-mixtools', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-diffusionmap', when='@:2.3.3', type=('build', 'run'))
    depends_on('r-tsne', when='@:3.1.0', type=('build', 'run'))
    depends_on('r-ranger', when='@:2.3.2', type=('build', 'run'))
    depends_on('r-ggjoy', when='@:2.1.0', type=('build', 'run'))
    depends_on('r-sdmtools', when='@:3.1.0', type=('build', 'run'))
    depends_on('r-tclust', when='@:2.3.2', type=('build', 'run'))
    depends_on('r-fnn', when='@:2.3.2', type=('build', 'run'))
    depends_on('r-vgam', when='@:2.3.2', type=('build', 'run'))
    depends_on('r-e1071', when='@:2.0.1', type=('build', 'run'))
    depends_on('r-compositions', when='@:2.0.1', type=('build', 'run'))
    depends_on('r-nmof', when='@:2.0.1', type=('build', 'run'))
    depends_on('r-metap', when='@2.2.1:3.1.0', type=('build', 'run'))
    depends_on('r-stringr', when='@:2.3.2', type=('build', 'run'))
    depends_on('r-dplyr', when='@:2.3.4', type=('build', 'run'))
    depends_on('r-dosnow', when='@2.3.0:2.3.4', type=('build', 'run'))
    depends_on('r-foreach', when='@2.3.0:2.3.4', type=('build', 'run'))
    depends_on('r-hdf5r', when='@2.3.2:2.3.4', type=('build', 'run'))
    depends_on('java', when='@:2.3.0')
