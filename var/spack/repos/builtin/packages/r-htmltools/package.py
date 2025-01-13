# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHtmltools(RPackage):
    """Tools for HTML.

    Tools for HTML generation and output."""

    cran = "htmltools"

    license("GPL-2.0-or-later")

    version("0.5.8.1", sha256="f9f62293ec06c353c4584db6ccedb06a2da12e485208bd26b856f17dd013f176")
    version("0.5.5", sha256="c8b23fab855a89c6ed0f6d6c7cad0ff9c5ae329c0bdb479940443ee752f26659")
    version("0.5.3", sha256="2c451b369ea8918358e2b280f548816664fe0143222c609e6bfb1f9cd2f7324f")
    version("0.5.2", sha256="7dc7d50436e5a82a5801f85bcd2f572a06a98b4027d71aa17b4854ec9b2767fb")
    version("0.5.1.1", sha256="f0bfe72ffe330f3d6c9ead5857f3a4aef80e002e32558074a3e643f2ab67a4ba")
    version("0.5.1", sha256="6ac82e4451f9558ceb541ea659a736b2ab3245827832b44d3661e7a4d91f6307")
    version("0.3.6", sha256="44affb82f9c2fd76c9e2b58f9229adb003217932b68c3fdbf1327c8d74c868a2")
    version("0.3.5", sha256="29fb7e075744bbffdff8ba4fce3860076de66f39a59a100ee4cfb4fc00722b49")

    depends_on("r@2.14.1:", type=("build", "run"))
    depends_on("r-digest", type=("build", "run"))
    depends_on("r-base64enc", type=("build", "run"), when="@0.5.1:")
    depends_on("r-rlang", type=("build", "run"), when="@0.5.1:")
    depends_on("r-rlang@0.4.10:", type=("build", "run"), when="@0.5.2:")
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@0.5.7:")
    depends_on("r-fastmap@1.1.0:", type=("build", "run"), when="@0.5.2:")

    depends_on("r-ellipsis", type=("build", "run"), when="@0.5.5:0.5.7")
    depends_on("r-rcpp", type=("build", "run"), when="@:0.3.6")
