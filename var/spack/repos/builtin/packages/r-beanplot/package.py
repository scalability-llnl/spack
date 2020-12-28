# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBeanplot(RPackage):
    """Plots univariate comparison graphs, an alternative to
       boxplot/stripchart/violin plot."""

    homepage = "https://cloud.r-project.org/package=beanplot"
    url      = "https://cloud.r-project.org/src/contrib/beanplot_1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/beanplot"

    version('1.2', sha256='49da299139a47171c5b4ccdea79ffbbc152894e05d552e676f135147c0c9b372')
