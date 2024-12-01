# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcpptoml(RPackage):
    """'Rcpp' Bindings to Parser for Tom's Obvious Markup Language.

    The configuration format defined by 'TOML' (which expands to "Tom's Obvious
    Markup Language") specifies an excellent format (described at
    <https://toml.io/en/>) suitable for both human editing as well as the
    common uses of a machine-readable format. This package uses 'Rcpp' to
    connect the 'cpptoml' parser written by Chase Geigle (in C++11) to R."""

    cran = "RcppTOML"

    license("JSON")

    version("0.2.2", sha256="371391f9ca82221e76a424082ea9ebc5ea2c50f14e8408469b09d7dc3e6f63aa")
    version("0.1.7", sha256="2f09f00cbee6c6eeff5d5f0195c10de0155496de15fbe8189c18627ee3090541")

    depends_on("cxx", type="build")  # generated

    depends_on("r@3.3.0:", type=("build", "run"))
    depends_on("r-rcpp@0.11.5:", type=("build", "run"))
