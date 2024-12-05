# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgsignif(RPackage):
    """Significance Brackets for 'ggplot2'.

    Enrich your 'ggplots' with group-wise comparisons. This package provides an
    easy way to indicate if two groups are significantly different. Commonly
    this is shown by a bracket on top connecting the groups of interest which
    itself is annotated with the level of significance (NS, *, **, ***). The
    package provides a single layer (geom_signif()) that takes the groups for
    comparison and the test (t.test(), wilcox.text() etc.) as arguments and
    adds the annotation to the plot."""

    cran = "ggsignif"

    license("GPL-3.0-only OR custom")

    version("0.6.4", sha256="112051af425a0c0f2998ce187dacad066bc16f55af01e3e7b76d62ff6954b20a")
    version("0.6.3", sha256="ca8545b25590e531512a90a18449a2cbab945f7434a1d60188c41f7d1839a7a9")
    version("0.6.0", sha256="6fe13efda31386483e64d466ba2f5a53a2a235ae04f5c17bba3ccc63d283499e")

    depends_on("r-ggplot2@2.0.0:", type=("build", "run"))
    depends_on("r-ggplot2@3.3.5:", type=("build", "run"), when="@0.6.3:")
