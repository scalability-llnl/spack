# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBroom(RPackage):
    """Convert Statistical Objects into Tidy Tibbles.

    Summarizes key information about statistical objects in tidy tibbles. This
    makes it easy to report results, create plots and consistently work with
    large numbers of models at once. Broom provides three verbs that each
    provide different types of information about a model. tidy() summarizes
    information about model components such as coefficients of a regression.
    glance() reports information about an entire model, such as goodness of fit
    measures like AIC and BIC. augment() adds information about individual
    observations to a dataset, such as fitted values or influence measures."""

    cran = "broom"

    license("MIT")

    version("1.0.6", sha256="24cf36248dffbde38d3d81befa679e362bfd0526b9843bc536a85452a19fbccf")
    version("1.0.4", sha256="1d5f11b509786a8a45ffdd137243e24d6445f2944947cbd62a0734a06add0ad6")
    version("1.0.1", sha256="4b5e5aa485f0e23ed993088fc84159e31a00087e3a12327071dda25193382892")
    version("0.8.0", sha256="66a1095d4430450dc810a5cea61cd7e7bee0e23739dcf5ddc5b57c9894fcf999")
    version("0.7.12", sha256="04fac12b2546689603a474fb92a0572f4241ae87b51b21b0808814a489227bd9")
    version("0.7.11", sha256="9e3999d2635ac72e8f4c3a81decd50ee5d464c001c155375b5a970a629ba2e19")
    version("0.7.10", sha256="129fd5a53abef7f42b7efac6c64ebd71269b136aa648846d640562357927464f")
    version("0.7.9", sha256="1d5695f97b378b2b77fb8f64a4a54b72b278913d4adf9d61a7ca4f38a1c7c5fc")
    version("0.7.3", sha256="de5650e46ca6884876b63bc401d22bef9eace671147774466406d43324aebc2f")
    version("0.5.2", sha256="16af7b446b24bc14461efbda9bea1521cf738c778c5e48fcc7bad45660a4ac62")
    version("0.5.1", sha256="da9e6bf7cb8f960b83309cf107743976cc32b54524675f6471982abe3d1aae2e")
    version("0.4.2", sha256="9f409413623cf25e7110452e6215353af5114f7044d73af182bd6c10971c5a44")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.5:", type=("build", "run"), when="@1.0.4:")
    depends_on("r-backports", type=("build", "run"), when="@0.5.0:")
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-dplyr@1.0.0:", type=("build", "run"), when="@0.7.3:")
    depends_on("r-generics@0.0.2:", type=("build", "run"), when="@0.5.1:")
    depends_on("r-glue", type=("build", "run"), when="@0.7.3:")
    depends_on("r-lifecycle", type=("build", "run"), when="@1.0.4:")
    depends_on("r-purrr", type=("build", "run"), when="@0.5.0:")
    depends_on("r-rlang", type=("build", "run"), when="@0.7.3:")
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-tibble", type=("build", "run"), when="@0.5.0:")
    depends_on("r-tibble@3.0.0:", type=("build", "run"), when="@0.7.3:")
    depends_on("r-tidyr", type=("build", "run"))
    depends_on("r-tidyr@1.0.0:", type=("build", "run"), when="@0.7.3:")

    depends_on("r-ellipsis", type=("build", "run"), when="@0.7.3:1.0.5")
    depends_on("r-plyr", type=("build", "run"), when="@:0.4.2")
    depends_on("r-psych", type=("build", "run"), when="@:0.4.2")
    depends_on("r-reshape2", type=("build", "run"), when="@:0.5.2")
    depends_on("r-nlme", type=("build", "run"), when="@:0.5.2")
    depends_on("r-ggplot2", type=("build", "run"), when="@0.7.10:1.0.1")
