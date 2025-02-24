# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNetwork(RPackage):
    """Classes for Relational Data.

    Tools to create and modify network objects. The network class can represent
    a range of relational data types, and supports arbitrary vertex/edge/graph
    attributes."""

    cran = "network"

    license("GPL-2.0-or-later")

    version("1.18.2", sha256="bf33892db9cabba9cd1597f09ef0e1277d63520a8cebd2d919e0d41fc706a27b")
    version("1.18.1", sha256="c80d70352967d8480cfa801f2a31bfe130e2ad4dbf2c07b0046e57f3013cd243")
    version("1.18.0", sha256="59f4b10174c87c8742c6b3c93c5e47833042375f5f872fdd23155b4a5244ce5b")
    version("1.17.2", sha256="9588a198807c8c68da147f479ca9af5bcb4468cf91b6a90b8044d313d9fa30f7")
    version("1.17.1", sha256="fc3c3a0014f8895a11c33994c9b44c6ef6cc49c7d026cd41ae6bba5ef63005a7")
    version("1.16.1", sha256="eb6435794cacc81abe1664391e8dcf1c10112bbb76fff9016dd6dbb8e83efeb1")
    version("1.15", sha256="5cbe5c0369e5f8363e33a86f14fd33ce8727166106381627ecd13b7452e14cb3")
    version("1.14-377", sha256="013c02f8d97f1f87f2c421760534df9353d2a8c2277f20b46b59fb79822d3e46")
    version("1.13.0", sha256="7a04ea89261cdf32ccb52222810699d5fca59a849053e306b5ec9dd5c1184f87")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-tibble", type=("build", "run"), when="@1.14-377:")
    depends_on("r-magrittr", type=("build", "run"), when="@1.14-377:")
    depends_on("r-statnet-common@4.5:", type=("build", "run"), when="@1.17.1:")
