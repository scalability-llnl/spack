# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLabelled(RPackage):
    """Manipulating Labelled Data.

    Work with labelled data imported from 'SPSS' or 'Stata' with 'haven' or
    'foreign'. This package provides useful functions to deal with
    "haven_labelled" and "haven_labelled_spss" classes introduced by 'haven'
    package."""

    cran = "labelled"

    license("GPL-3.0-or-later")

    version("2.13.0", sha256="9e2e82a42343b62f8a476d4dd7b13e9ffb3ee2c4e23bdf2cd29ef25b3dffa237")
    version("2.11.0", sha256="eddc5299ca448ea9c244960af65b95f4164495febd609f719e0f453598a0e5dd")
    version("2.10.0", sha256="5e93e29dcbbf0f6273b502b744695426e238ffe106f1db2bb5daeb1f17c9c40a")
    version("2.9.1", sha256="9eb10b245f64f3fb7346121aa4cd98638946e1cc4208dd5e28791ef8fd62fa40")
    version("2.9.0", sha256="36ac0e169ee065a8bced9417efeb85d62e1504a590d4321667d8a6213285d639")
    version("2.7.0", sha256="b1b66b34d3ad682e492fc5bb6431780760576d29dbac40d87bef3c0960054bdb")

    depends_on("r@3.0:", type=("build", "run"), when="@2.9.0:")
    depends_on("r-haven@2.3.1:", type=("build", "run"))
    depends_on("r-haven@2.4.1:", type=("build", "run"), when="@2.9.0:")
    depends_on("r-dplyr", type=("build", "run"))
    depends_on("r-dplyr@1.0.0:", type=("build", "run"), when="@2.9.0:")
    depends_on("r-lifecycle", type=("build", "run"))
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-vctrs", type=("build", "run"))
    depends_on("r-stringr", type=("build", "run"), when="@2.9.0:")
    depends_on("r-tidyr", type=("build", "run"))
    depends_on("r-tidyselect", type=("build", "run"), when="@2.13.0:")

    depends_on("r-pillar", type=("build", "run"), when="@:2.7.0")
