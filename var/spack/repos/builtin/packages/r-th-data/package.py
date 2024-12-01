# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RThData(RPackage):
    """TH's Data Archive.

    Contains data sets used in other packages Torsten Hothorn maintains."""

    cran = "TH.data"

    version("1.1-2", sha256="47f94eb57b6fcef42efa30824c1356bf10529c4b94b0d0acdb787b434dddde73")
    version("1.1-1", sha256="edf3ab16b142f4c52d21fc64e41409ed138e5b3e142f2fae964b00f02d53dd7a")
    version("1.1-0", sha256="21b37e251da5635ae91668f64b4c6f6a7ccedbe1f01af769d30fb532af83113e")
    version("1.0-10", sha256="618a1c67a30536d54b1e48ba3af46a6edcd6c2abef17935b5d4ba526a43aff55")
    version("1.0-9", sha256="d8318a172ce2b9f7f284dc297c8a8d5093de8eccbb566c8e7580e70938dfae0f")
    version("1.0-8", sha256="478f109fcc1226500ead8e3bd6e047cecde2294fde4df8ec216d38313db79a9d")
    version("1.0-7", sha256="29e126344daccbebc7df68924730ae4159a0faad77f86302070920684ba6070e")

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.1-0:")
    depends_on("r-survival", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
