# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHardhat(RPackage):
    """Construct Modeling Packages.

    Building modeling packages is hard. A large amount of effort generally goes
    into providing an implementation for a new method that is efficient, fast,
    and correct, but often less emphasis is put on the user interface. A good
    interface requires specialized knowledge about S3 methods and formulas,
    which the average package developer might not have. The goal of 'hardhat'
    is to reduce the burden around building new modeling packages by providing
    functionality for preprocessing, predicting, and validating input."""

    cran = "hardhat"

    license("MIT")

    version("1.4.0", sha256="46d023ddfc8f940cd889478fa91c42e894a0df58a10f3b6c0eb688a500b2b3ad")
    version("1.3.0", sha256="fe9ff009e2ba6dd4d70cbb541430f88d85c0a28d6a1c2772e4910c79b81fe82e")
    version("1.2.0", sha256="f9320eccb1b5f624a46fa074e3ccc202c383b77098ecd08b193aeb47daedad78")
    version("1.0.0", sha256="2740dc243a440e7d32370a78f9258255faea6d900075901cf6009c651769e7bd")
    version("0.2.0", sha256="9497ca0fe6206c54d1da79f248d44c5faffc7d375b630091ef45dfca46c29628")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@1.0.0:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-cli@3.6.0:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-glue", type=("build", "run"))
    depends_on("r-glue@1.6.2:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-rlang@0.4.2:", type=("build", "run"))
    depends_on("r-rlang@1.0.2:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-rlang@1.0.3:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-rlang@1.1.0:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-tibble@3.1.7:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-tibble@3.2.1:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-vctrs@0.3.0:", type=("build", "run"))
    depends_on("r-vctrs@0.4.1:", type=("build", "run"), when="@1.0.0:")
    depends_on("r-vctrs@0.6.0:", type=("build", "run"), when="@1.3.0:")
