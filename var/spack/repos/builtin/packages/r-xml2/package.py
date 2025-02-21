# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXml2(RPackage):
    """Package required POI jars for the xlsx package.

    Work with XML files using a simple, consistent interface. Built on top of
    the 'libxml2' C library."""

    cran = "xml2"

    license("MIT")

    version("1.3.6", sha256="e81991ff99bff3616dde8683c1327194e3ea64fa3b8062f52d8ce32673dd308f")
    version("1.3.3", sha256="cb4e9c0d31618ed67d2bfa4c7b5e52680e11612ed356a8164b541d44163c1c8d")
    version("1.3.2", sha256="df22f9e7e3189d8c9b8804eaf0105324fdac983cffe743552f6d76613600a4cf")
    version("1.2.2", sha256="3050f147c4335be2925a576557bbda36bd52a5bba3110d47b740a2dd811a78f4")
    version("1.2.1", sha256="5615bbc94607efc3bc192551992b349091df802ae34b855cfa817733f2690605")
    version("1.1.1", sha256="00f3e3b66b76760c19da5f6dddc98e6f30de36a96b211e59e1a3f4ff58763116")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@1.3.6:")
    depends_on("libxml2")

    depends_on("r-bh", type=("build", "run"), when="@:1.1.1")
    depends_on("r-cli", type=("build", "run"), when="@1.3.6:")
    depends_on("r-rcpp@0.12.12:", type=("build", "run"), when="@:1.2")
    depends_on("r-rlang@1.1.0:", type=("build", "run"), when="@1.3.6:")
