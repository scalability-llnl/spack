# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHmisc(RPackage):
    """Harrell Miscellaneous.

    Contains many functions useful for data analysis, high-level graphics,
    utility operations, functions for computing sample size and power,
    importing and annotating datasets, imputing missing values, advanced table
    making, variable clustering, character string manipulation, conversion of R
    objects to LaTeX and html code, and recoding variables."""

    cran = "Hmisc"

    version("5.1-3", sha256="3c61772ff7a78ca5855189faa810c74117dc5df240103adc6e90eb94e9c605eb")
    version("5.0-1", sha256="db390f8f8a150cb5cffb812e9609a8e8632ceae0dc198528f190fd670ba8fa59")
    version("4.7-1", sha256="325d571a68b2198eabd258a8d86143cac659ffa70e474088a18e9b58ab882e7f")
    version("4.7-0", sha256="29ec2d9ca11c790c350e93323126bef4f498c69c41c31bb335fd04671e0f87bd")
    version("4.6-0", sha256="2c1ce906b2333c6dc946dc7f10b74cfa552bce2b12dbebf295d143163562a1ad")
    version("4.4-2", sha256="490ac64dd8558868e7c6fdd9523af102e17ea536c450d62c48b04155279bfbc8")
    version("4.4-0", sha256="f16ecf4c5ee2202d51f426282a54f8000ffa8b9747c3e910205f34f878556ec7")
    version("4.2-0", sha256="9e9614673288dd00295f250fa0bf96fc9e9fed692c69bf97691081c1a01411d9")
    version("4.1-1", sha256="991db21cdf73ffbf5b0239a4876b2e76fd243ea33528afd88dc968792f281498")

    depends_on("r@4.1.0:", type=("build", "run"), when="@5.1-2:")
    depends_on("r-formula", type=("build", "run"))
    depends_on("r-ggplot2@2.2:", type=("build", "run"))
    depends_on("r-cluster", type=("build", "run"))
    depends_on("r-rpart", type=("build", "run"))
    depends_on("r-nnet", type=("build", "run"))
    depends_on("r-foreign", type=("build", "run"))
    depends_on("r-gtable", type=("build", "run"))
    depends_on("r-gridextra", type=("build", "run"))
    depends_on("r-data-table", type=("build", "run"))
    depends_on("r-htmltable@1.11.0:", type=("build", "run"))
    depends_on("r-viridis", type=("build", "run"))
    depends_on("r-htmltools", type=("build", "run"))
    depends_on("r-base64enc", type=("build", "run"))
    depends_on("r-knitr", type=("build", "run"), when="@5.0-1:")
    depends_on("r-rmarkdown", type=("build", "run"), when="@5.0-1:")
    depends_on("r-colorspace", type=("build", "run"), when="@5.0-1:")

    depends_on("r-acepack", type=("build", "run"), when="@:4.4-0")
    depends_on("r-lattice", type=("build", "run"), when="@:4.7-1")
    depends_on("r-latticeextra", type=("build", "run"), when="@:4.7-1")
    depends_on("r-survival@2.40-1:", type=("build", "run"), when="@:4.7-1")
    depends_on("r-survival@3.1-6:", type=("build", "run"), when="@4.4:4.7-1")
