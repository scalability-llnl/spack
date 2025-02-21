# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RXgboost(RPackage):
    """Extreme Gradient Boosting.

    Extreme Gradient Boosting, which is an efficient implementation of gradient
    boosting framework. This package is its R interface. The package includes
    efficient linear model solver and tree learning algorithms. The package can
    automatically do parallel computation on a single machine which could be
    more than 10 times faster than existing gradient boosting packages. It
    supports various objective functions, including regression, classification
    and ranking. The package is made to be extensible, so that users are also
    allowed to define their own objectives easily."""

    cran = "xgboost"

    license("Apache-2.0 OR custom")

    version("1.7.8.1", sha256="394d6fd00b2fe97549c7a7e6598df86448cdfbd7c0af45b0c17f7b9e81bc1be9")
    version("1.7.5.1", sha256="4ec0833f206f84e5983e9f373ea64903bec488f751fba6f75a6f4702b1c965bc")
    version("1.6.0.1", sha256="9ae99a20997e1b02ffd21cabada2a55e53f5754746238ee900de5eb6cd964ebd")
    version("1.5.0.2", sha256="4750b9a289d8cb685291939eed7c493bb42c5cc154ef98e13100abb1727eab13")
    version("1.3.2.1", sha256="2ff462b81ad51a4810bd7860cb014b9b88831a8b1d45774249a808547147f884")
    version("0.90.0.2", sha256="240584c1b4d54a95b4fef9074480752fae9a5b096e8f84747457d641decfc9bf")
    version("0.81.0.1", sha256="3e7ada32e66881ea5c90aeafdab948927014c76cfff60a8e3d7f9e1f8a9ed7ce")
    version("0.6-4", sha256="9fc51dd1b910c70930357f617d1ac7a74c5056e8847d4188175db27c09f9d1ed")
    version("0.4-4", sha256="b955fc3352fcdc4894178c82fd62fbaf5e099c9d794f1e9daa2dd7b3494b61ff")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r@2.15.1:", type=("build", "run"), when="@0.6-0:")
    depends_on("r@3.3.0:", type=("build", "run"), when="@0.6-3:")
    depends_on("r-matrix@1.1-0:", type=("build", "run"))
    depends_on("r-data-table@1.9.6:", type=("build", "run"))
    depends_on("r-jsonlite@1.0:", type=("build", "run"), when="@1.5.0.2:")
    depends_on("gmake", type="build")

    depends_on("r-stringr", type=("build", "run"), when="@:0.7")
    depends_on("r-stringi@0.5.2:", type=("build", "run"), when="@:0.90.0.2")
    depends_on("r-magrittr@1.5:", type=("build", "run"), when="@:1.3.2.1")
