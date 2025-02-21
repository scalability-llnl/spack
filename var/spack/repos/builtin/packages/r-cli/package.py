# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCli(RPackage):
    """Helpers for Developing Command Line Interfaces.

    A suite of tools to build attractive command line interfaces ('CLIs'), from
    semantic elements: headings, lists, alerts, paragraphs, etc.  Supports
    custom themes via a 'CSS'-like language. It also contains a number of lower
    level 'CLI' elements: rules, boxes, trees, and 'Unicode' symbols with
    'ASCII' alternatives. It integrates with the 'crayon' package to support
    'ANSI' terminal colors."""

    cran = "cli"

    license("MIT")

    version("3.6.3", sha256="4295085f11221c54b1dd2b1d39a675a85dfd9f900294297567e1d36f65ac4841")
    version("3.6.1", sha256="be3006cec7e67f9ae25e21b4658c4bec680038c2ef7467df5f14da3311a05e36")
    version("3.4.1", sha256="1c585efbfd8b8685c66fac34bcb60f28c351691bb4b9931df214e6e47fd9744e")
    version("3.3.0", sha256="c3a9ebbcb9017fb9aeda4f7df5ca981e42b169cbd7ce13e592cda2cd74250d63")
    version("3.2.0", sha256="cd5a1b754d09de33f088f25ecdb0494100f9a42bc0a66622bfd7d8ec5498e862")
    version("3.1.1", sha256="c8b3e6014ad60593ba21897255acfe90c0e3f98bd4f7e22c1f3acb2644cf54cf")
    version("3.1.0", sha256="c70a61830bf706a84c59eb74a809978846cee93742198ab4192742a5df1ace11")
    version("3.0.1", sha256="d89a25b6cd760e157605676e104ce65473a7d8d64c289efdd9640e949968b4fd")
    version("2.2.0", sha256="39a77af61724f8cc1f5117011e17bb2a488cbac61a7c112db078a675d3ac40b8")
    version("2.0.2", sha256="490834e5b80eb036befa0e150996bcab1c4d5d168c3d45209926e52d0d5413b6")
    version("1.1.0", sha256="4fc00fcdf4fdbdf9b5792faee8c7cf1ed5c4f45b1221d961332cda82dbe60d0a")
    version("1.0.1", sha256="ef80fbcde15760fd55abbf9413b306e3971b2a7034ab8c415fb52dc0088c5ee4")
    version("1.0.0", sha256="8fa3dbfc954ca61b8510f767ede9e8a365dac2ef95fe87c715a0f37d721b5a1d")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r@3.4:", type=("build", "run"), when="@3.3.0:")

    depends_on("r-assertthat", type=("build", "run"), when="@:2.3")
    depends_on("r-crayon@1.3.4:", type=("build", "run"), when="@:2.2")
    depends_on("r-fansi", type=("build", "run"), when="@2:2.2")
    depends_on("r-glue", type=("build", "run"), when="@2:3.4.1")
    depends_on("r-glue@1.6.0:", type=("build", "run"), when="@3.3.0")
