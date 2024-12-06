# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSplitstackshape(RPackage):
    """Stack and Reshape Datasets After Splitting Concatenated Values.

    Online data collection tools like Google Forms often export
    multiple-response questions with data concatenated in cells. The
    concat.split (cSplit) family of functions splits such data into separate
    cells. The package also includes functions to stack groups of columns and
    to reshape wide data, even when the data are "unbalanced" something which
    reshape (from base R) does not handle, and which melt and dcast from
    reshape2 do not easily handle."""

    cran = "splitstackshape"

    license("GPL-3.0-only")

    version("1.4.8", sha256="656032c3f1e3dd5b8a3ee19ffcae617e07104c0e342fc3da4d863637a770fe56")
    version("1.4.6", sha256="b9888f9508babdb8e09f57674facaa8b158a06255ef1e61c8df813f58881860f")
    version("1.4.4", sha256="78c27fb55459b0cc858cef5c2201a10ae2472a1a0be179e05df05ced2f590f6e")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-data-table@1.9.4:", type=("build", "run"))
