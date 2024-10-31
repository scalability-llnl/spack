# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RJsonify(RPackage):
    """Convert Between 'R' Objects and Javascript Object Notation
    (JSON).

    Conversions between 'R' objects and Javascript Object Notation (JSON) using
    the 'rapidjsonr' library
    <https://CRAN.R-project.org/package=rapidjsonr>."""

    cran = "jsonify"

    license("MIT")

    version("1.2.2", sha256="3745e962592f021a3deaed8b2f6b99c4f7181f28e095300a96d1c2b08af4af2f")
    version("1.2.1", sha256="929191ab32e34af6a02ad991e29314cc78ea40763fcf232388ef2d132137fbce")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r-rcpp@0.12.18:", type=("build", "run"))
    depends_on("r-rapidjsonr@1.2.0:", type=("build", "run"))
