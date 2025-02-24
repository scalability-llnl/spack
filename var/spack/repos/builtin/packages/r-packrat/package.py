# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPackrat(RPackage):
    """A Dependency Management System for Projects and their R Package
    Dependencies.

    Manage the R packages your project depends on in an isolated, portable, and
    reproducible way."""

    cran = "packrat"

    license("GPL-2.0-only")

    version("0.9.2", sha256="69df5943257e6c4d06f3d907241b668b53dedece72158ca935260b8b8e1672d7")
    version("0.9.1", sha256="414013c6044d2985e69bbc8494c152716b6f81ca15b329c731cfe8f965fd3344")
    version("0.8.1", sha256="45db0301fa6a0a6944b070ac219cd1fa754bac24e517e59758cdc51e8aed23da")
    version("0.8.0", sha256="3025b9052974bec00fb09299226b80004d48e611e15a65e5a0bc49d3538844ef")
    version("0.7.0", sha256="e8bce1fd78f28f3a7bf56e65a2ae2c6802e69bf55466c24e1d1a4b8a5f83dcc2")
    version("0.5.0", sha256="d6a09290fbe037a6c740921c5dcd70b500e5b36e4713eae4010adf0c456bc5f7")
    version("0.4.9-3", sha256="87299938a751defc54eb00a029aecd3522d6349d900aaa8b3e1aa6bf31e98234")
    version("0.4.8-1", sha256="a283caf4fda419e6571ae9ca6210a59002a030721feb8a50c0d0787fd6f672f3")
    version("0.4.7-1", sha256="6e5067edd41a4086bb828617d3378210a3dbc995e223b02af811549519f3223a")

    depends_on("r@3.0.0:", type=("build", "run"))
