# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgsignif(RPackage):
    """Enrich your 'ggplots' with group-wise comparisons. This package provides
    an easy way to indicate if two groups are significantly different. Commonly
    this is shown by a bracket on top connecting the groups of interest which
    itself is annotated with the level of significance (NS, *, **, ***). The
    package provides a single layer (geom_signif()) that takes the groups for
    comparison and the test (t.test(), wilcox.text() etc.) as arguments and
    adds the annotation to the plot."""

    homepage = "https://github.com/const-ae/ggsignif"
    url      = "https://cloud.r-project.org/src/contrib/ggsignif_0.6.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ggsignif"

    version('0.6.0', sha256='6fe13efda31386483e64d466ba2f5a53a2a235ae04f5c17bba3ccc63d283499e')

    depends_on('r-ggplot2@2.0.0:', type=('build', 'run'))
