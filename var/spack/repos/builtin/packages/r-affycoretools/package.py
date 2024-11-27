# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RAffycoretools(RPackage):
    """Functions useful for those doing repetitive analyses with Affymetrix
    GeneChips.

    Various wrapper functions that have been written to streamline the more
    common analyses that a core Biostatistician might see."""

    bioc = "affycoretools"

    version("1.72.0", commit="229ae09efc1a66e64ea395019c32d16387bf81ac")
    version("1.70.0", commit="f09a788aa83e1e052a7c5f148a451a99fe9c9c96")
    version("1.68.1", commit="69546b1fe5edd71eca130d53d33f0fb0fcf62c97")
    version("1.66.0", commit="6bf769d70e196634097f465ed2fa85cce5312a6d")
    version("1.62.0", commit="c9779e4da648fd174c9bd575c6020be1c03047c4")
    version("1.56.0", commit="71eab04056a8d696470420a600b14900186be898")
    version("1.54.0", commit="1e1f9680bc3e1fa443f4a81ce5ab81349959b845")
    version("1.52.2", commit="2f98c74fad238b94c1e453b972524ab7b573b0de")
    version("1.50.6", commit="4be92bcb55d7bace2a110865b7530dcfac14e76e")
    version("1.48.0", commit="e0d52e34eead1ac45d3e60c59efd940e4889eb99")

    depends_on("r+X", type=("build", "run"))
    depends_on("r-biobase", type=("build", "run"))
    depends_on("r-affy", type=("build", "run"))
    depends_on("r-limma", type=("build", "run"))
    depends_on("r-gostats", type=("build", "run"))
    depends_on("r-gcrma", type=("build", "run"))
    depends_on("r-xtable", type=("build", "run"))
    depends_on("r-annotationdbi", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-gplots", type=("build", "run"))
    depends_on("r-oligoclasses", type=("build", "run"))
    depends_on("r-reportingtools", type=("build", "run"))
    depends_on("r-hwriter", type=("build", "run"))
    depends_on("r-lattice", type=("build", "run"))
    depends_on("r-s4vectors", type=("build", "run"))
    depends_on("r-edger", type=("build", "run"))
    depends_on("r-rsqlite", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-dbi", type=("build", "run"), when="@1.50.6:")
    depends_on("r-glimma", type=("build", "run"), when="@1.62.0:")
