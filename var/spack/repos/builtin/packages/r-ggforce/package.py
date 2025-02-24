# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgforce(RPackage):
    """Accelerating 'ggplot2'.

    The aim of 'ggplot2' is to aid in visual data investigations. This focus
    has led to a lack of facilities for composing specialised plots. 'ggforce'
    aims to be a collection of mainly new stats and geoms that fills this gap.
    All additional functionality is aimed to come through the official
    extension system so using 'ggforce' should be a stable experience."""

    cran = "ggforce"

    license("MIT")

    version("0.4.2", sha256="c145b0e6ed6847d409ed2fe103b81234855bc0661cde2bfb4410fb23680e51a8")
    version("0.4.1", sha256="b44219fb63c45fa003c64bca323452f16dcace635204bc0127d3244c0f451873")
    version("0.3.3", sha256="2a283bb409da6b96929863a926b153bcc59b2c6f00551805db1d1d43e5929f2f")
    version("0.3.2", sha256="4cce8acb60ce06af44c1c76bbacd7de129eed9b51ed6a85e03a9bf55b0eff4d2")
    version("0.3.1", sha256="a05271da9b226c12ae5fe6bc6eddb9ad7bfe19e1737e2bfcd6d7a89631332211")

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r-ggplot2@3.0.0:", type=("build", "run"))
    depends_on("r-ggplot2@3.3.6:", type=("build", "run"), when="@0.4.1:")
    depends_on("r-rcpp@0.12.2:", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-tweenr@0.1.5:", type=("build", "run"))
    depends_on("r-gtable", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-polyclip", type=("build", "run"))
    depends_on("r-tidyselect", type=("build", "run"))
    depends_on("r-withr", type=("build", "run"))
    depends_on("r-systemfonts", type=("build", "run"), when="@0.4.1:")
    depends_on("r-vctrs", type=("build", "run"), when="@0.4.1:")
    depends_on("r-cli", type=("build", "run"), when="@0.4.1:")
    depends_on("r-lifecycle", type=("build", "run"), when="@0.4.1:")
    depends_on("r-rcppeigen", type=("build", "run"))
