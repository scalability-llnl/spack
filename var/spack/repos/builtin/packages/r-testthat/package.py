# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTestthat(RPackage):
    """Unit Testing for R.

    Software testing is important, but, in part because it is frustrating and
    boring, many of us avoid it. 'testthat' is a testing framework for R that
    is easy to learn and use, and integrates with your existing 'workflow'."""

    cran = "testthat"

    license("MIT")

    version("3.2.1.1", sha256="d785ce3975939e28b61048b0e28d881c80904534ff21e5b1a79a0a934124e9f7")
    version("3.1.7", sha256="1ad86b1739481c6c46359a6634ecc706bf513f34b26d7a62cbc719bbd4658eab")
    version("3.1.5", sha256="a8f56b9426206ddfc30b550c82ff2f042ebe1c2f5bfd4184aec8facac8f5b7fc")
    version("3.1.4", sha256="a47eec031b4e186a8bd331031371b2347063a283050eca2adbfaa37d7a6c9c09")
    version("3.1.2", sha256="ed41a6168ca22869b6aebe1e5865bb2f5338a7c35ca0a13cf69ac2f5c6aeb659")
    version("3.1.1", sha256="e6755fb4f5388751af952edfd555533bb55d6252606f6fcef07bdb6268c8cf80")
    version("3.0.1", sha256="297fc45c719684f11ddf9dc9088f5528fdf9b44625165543384eaf579f243ad0")
    version("2.3.2", sha256="1a268d8df07f7cd8d282d03bb96ac2d96a24a95c9aa52f4cca5138a09dd8e06c")
    version("2.2.1", sha256="67ee0512bb312695c81fd74338bb8ce9e2e58763681ddbcdfdf35f52dfdb0b78")
    version("2.1.0", sha256="cf5fa7108111b32b86e70819352f86b57ab4e835221bb1e83642d52a1fdbcdd4")
    version("1.0.2", sha256="0ef7df0ace1fddf821d329f9d9a5d42296085350ae0d94af62c45bd203c8415e")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-brio", type=("build", "run"), when="@3.0.1:")
    depends_on("r-brio@1.1.3:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-callr@3.5.1:", type=("build", "run"), when="@3.0.1:")
    depends_on("r-callr@3.7.3:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-cli", type=("build", "run"), when="@2.0.0:")
    depends_on("r-cli@2.2.0:", type=("build", "run"), when="@3.0.1:")
    depends_on("r-cli@3.3.0:", type=("build", "run"), when="@3.1.4:")
    depends_on("r-cli@3.4.0:", type=("build", "run"), when="@3.1.5:")
    depends_on("r-cli@3.6.1:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-desc", type=("build", "run"), when="@3.0.1:")
    depends_on("r-desc@1.4.2:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-digest", type=("build", "run"))
    depends_on("r-digest@0.6.33:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-evaluate", type=("build", "run"), when="@2.2.0:")
    depends_on("r-evaluate@0.21:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-jsonlite", type=("build", "run"), when="@3.0.1:")
    depends_on("r-jsonlite@1.8.7:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-lifecycle", type=("build", "run"), when="@3.0.1:")
    depends_on("r-lifecycle@1.0.3:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-magrittr@2.0.3:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-pkgload", type=("build", "run"), when="@2.3.2:")
    depends_on("r-pkgload@1.3.2.1:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-praise", type=("build", "run"))
    depends_on("r-praise@1.0.0:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-processx", type=("build", "run"), when="@3.0.1:")
    depends_on("r-processx@3.8.2:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-ps@1.3.4:", type=("build", "run"), when="@3.0.1:")
    depends_on("r-ps@1.7.5:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-r6@2.2.0:", type=("build", "run"))
    depends_on("r-r6@2.5.1:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-rlang@0.3.0:", type=("build", "run"), when="@2.0.0:")
    depends_on("r-rlang@0.4.1:", type=("build", "run"), when="@2.3.2:")
    depends_on("r-rlang@0.4.9:", type=("build", "run"), when="@3.0.1:")
    depends_on("r-rlang@1.0.1:", type=("build", "run"), when="@3.1.4:")
    depends_on("r-rlang@1.1.1:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-waldo@0.2.1:", type=("build", "run"), when="@3.0.1:")
    depends_on("r-waldo@0.2.4:", type=("build", "run"), when="@3.1.1:")
    depends_on("r-waldo@0.4.0:", type=("build", "run"), when="@3.1.4:")
    depends_on("r-waldo@0.5.1:", type=("build", "run"), when="@3.2.0:")
    depends_on("r-withr@2.0.0:", type=("build", "run"), when="@2.0.0:")
    depends_on("r-withr@2.3.0:", type=("build", "run"), when="@3.0.1:")
    depends_on("r-withr@2.4.3:", type=("build", "run"), when="@3.1.2:")
    depends_on("r-withr@2.5.0:", type=("build", "run"), when="@3.2.0:")

    depends_on("r-crayon@1.3.4:", type=("build", "run"), when="@:3.1.4")
    depends_on("r-ellipsis", type=("build", "run"), when="@2.3.2:3.2.0")
    depends_on("r-ellipsis@0.2.0:", type=("build", "run"), when="@3.0.1:3.2.0")
