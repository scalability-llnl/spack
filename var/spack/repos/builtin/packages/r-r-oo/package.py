# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RROo(RPackage):
    """R Object-Oriented Programming with or without References.

    Methods and classes for object-oriented programming in R with or without
    references. Large effort has been made on making definition of methods as
    simple as possible with a minimum of maintenance for package developers.
    The package has been developed since 2001 and is now considered very
    stable. This is a cross-platform package implemented in pure R that defines
    standard S3 classes without any tricks."""

    cran = "R.oo"

    version("1.26.0", sha256="f7602b388c2216fbb4d1a31d4040ed92b40dc83d3e3746db7011637db4d44365")
    version("1.25.0", sha256="b8b19061774918ee7d9d4330c16c0ea505f7cd02d01343df1e8b2e4fb847beef")
    version("1.24.0", sha256="37a1dab8dd668ceba69a1ba36c0c60e9809e29b74bd56d1e8ed519e19c8e3bb6")
    version("1.23.0", sha256="f5124ce3dbb0a62e8ef1bfce2de2d1dc2f776e8c48fd8cac358f7f5feb592ea1")
    version("1.22.0", sha256="c0862e4608fb2b8f91ec4494d46c2f3ba7bc44999f9aa3d7b9625d3792e7dd4c")
    version("1.21.0", sha256="645ceec2f815ed39650ca72db87fb4ece7357857875a4ec73e18bfaf647f431c")

    depends_on("r@2.13.0:", type=("build", "run"))
    depends_on("r-r-methodss3@1.7.1:", type=("build", "run"))
    depends_on("r-r-methodss3@1.8.0:", type=("build", "run"), when="@1.24.0:")
    depends_on("r-r-methodss3@1.8.1:", type=("build", "run"), when="@1.25.0:")
    depends_on("r-r-methodss3@1.8.2:", type=("build", "run"), when="@1.26.0:")
