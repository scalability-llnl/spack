# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RPartykit(RPackage):
    """A Toolkit for Recursive Partytioning.

    A toolkit with infrastructure for representing, summarizing, and
    visualizing tree-structured regression and classification models. This
    unified infrastructure can be used for reading/coercing tree models from
    different sources ('rpart', 'RWeka', 'PMML') yielding objects that share
    functionality for print()/plot()/predict() methods. Furthermore, new and
    improved reimplementations of conditional inference trees (ctree()) and
    model-based recursive partitioning (mob()) from the 'party' package are
    provided based on the new infrastructure. A description of this package was
    published by Hothorn and Zeileis (2015)
    <https://jmlr.org/papers/v16/hothorn15a.html>."""

    cran = "partykit"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("1.2-22", sha256="0f0015aa970b10a85d1fabfd2fcf35a6552e292fe151766e348c105f7f5c0adb")
    version("1.2-20", sha256="63509aa3ed2d7417ad284c037cef66bc837fdb7a97967957e79b9fee8ed2e0da")
    version("1.2-16", sha256="e643d4e29c1894497e3dd5fe274783319d0044dec50282ed807cebc21736ddb2")
    version("1.2-15", sha256="b2e9454b2f4b9a39c9581c5871462f00acef4eeee5696ce3e32cfa1468d1e3ac")
    version("1.2-11", sha256="3a83332d782a235cfb5ba60cc8f1c51d46ca5477b22979a614f514d1c951c602")
    version("1.2-5", sha256="f48e30790f93fa5d03e68e8ce71ce33d009d107d46d45d85da2016b38b27629c")
    version("1.2-3", sha256="56749b246e283f94ac2ad2cdcfc0a477e05cd44b5e8f6e462c26f4dff818da35")
    version("1.1-1", sha256="d9f4762690cd85ee4e3dc44f5a14069d10a1900afdfbcdc284d2a94b4a8e8332")

    depends_on("c", type="build")  # generated

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.2-11:")
    depends_on("r-libcoin@1.0-0:", type=("build", "run"), when="@1.2-0:")
    depends_on("r-mvtnorm", type=("build", "run"), when="@1.2-0:")
    depends_on("r-survival", type=("build", "run"))
    depends_on("r-formula@1.2-1:", type=("build", "run"))
    depends_on("r-inum@1.0-0:", type=("build", "run"), when="@1.2-0:")
    depends_on("r-rpart@4.1-11:", type=("build", "run"), when="@1.2-0:")
