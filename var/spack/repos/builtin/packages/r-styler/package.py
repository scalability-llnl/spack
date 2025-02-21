# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RStyler(RPackage):
    """Non-Invasive Pretty Printing of R Code.

    Pretty-prints R code without changing the user's formatting intent."""

    cran = "styler"

    license("MIT")

    version("1.10.3", sha256="adb9c22111a8669bdce6d4a5c09e0ad353e07c3488373484a258028203bfda41")
    version("1.9.1", sha256="c80fa3c062f007645ec820b5b087d4d5784e7797cc88d030ab59fb5823ded0bb")
    version("1.8.1", sha256="15505fa85f0aa2902bc8af3f00b2aeb205d41a92b77bffbd176d657753ee81e9")
    version("1.8.0", sha256="4f8b74c1ac158b0a4433b6008da6bb708f3c9ed1c7fb9bb5d79748858cb484c7")
    version("1.7.0", sha256="3e49f3ac2e65f9bdab15837a4e629db35c8fd0a15a74daa057354ba01e3022ce")
    version("1.6.2", sha256="a62fcc76aac851069f33874f9eaabdd580973b619cfc625d6ec910476015f75c")
    version("1.3.2", sha256="3fcf574382c607c2147479bad4f9fa8b823f54fb1462d19ec4a330e135a44ff1")

    depends_on("r@3.4.0:", type=("build", "run"), when="@1.7.0:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.8.0:")
    depends_on("r@3.6.0:", type=("build", "run"), when="@1.10.0:")
    depends_on("r-cli@1.1.0:", type=("build", "run"))
    depends_on("r-cli@3.1.1:", type=("build", "run"), when="@1.7.0:")
    depends_on("r-magrittr@1.0.1:", type=("build", "run"))
    depends_on("r-magrittr@2.0.0:", type=("build", "run"), when="@1.6.2:")
    depends_on("r-purrr@0.2.3:", type=("build", "run"))
    depends_on("r-r-cache@0.14.0:", type=("build", "run"))
    depends_on("r-r-cache@0.15.0:", type=("build", "run"), when="@1.6.2:")
    depends_on("r-rlang@0.1.1:", type=("build", "run"))
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@1.10.0:")
    depends_on("r-rprojroot@1.1:", type=("build", "run"))
    depends_on("r-vctrs@0.4.1:", type=("build", "run"), when="@1.8.0:")
    depends_on("r-withr@1.0.0:", type=("build", "run"))
    depends_on("r-withr@2.3.0:", type=("build", "run"), when="@1.8.1:")

    depends_on("r-backports@1.1.0:", type=("build", "run"), when="@:1.6.2")
    depends_on("r-xfun@0.1:", type=("build", "run"), when="@:1.6.2")
    depends_on("r-glue", type=("build", "run"), when="@1.6.2:1.7.0")
    depends_on("r-rematch2@2.0.1:", type=("build", "run"), when="@:1.7.0")
    depends_on("r-tibble@1.4.2:", type=("build", "run"), when="@:1.7.0")
