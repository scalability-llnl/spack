# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RParamhelpers(RPackage):
    """Helpers for Parameters in Black-Box Optimization, Tuning and Machine
     Learning.

    Functions for parameter descriptions and operations in black-box
    optimization, tuning and machine learning. Parameters can be described
    (type, constraints, defaults, etc.), combined to parameter sets and can in
    general be programmed on. A useful OptPath object (archive) to log function
    evaluations is also provided."""

    cran = "ParamHelpers"

    version("1.14.1", sha256="0450ff8489b0d4d0842130f6a9713ede97da936d7909c43d43587bf2d5a01a21")
    version("1.14", sha256="b17652d0a69de3241a69f20be4ad1bfe02c413328a17f3c1ac7b73886a6ba2eb")
    version("1.12", sha256="b54db9e6608ba530345c380c757a60cb2b78ab08992a890b1a41914ce7abcc14")
    version("1.11", sha256="1614f4c0842cf822befc01228ab7263417f3423dd6a1dc24347b14f8491637a0")
    version("1.10", sha256="80629ba62e93b0b706bf2e451578b94fbb9c5b95ff109ecfb5b011bfe0a0fa5b")

    depends_on("c", type="build")  # generated

    depends_on("r-backports", type=("build", "run"), when="@1.11:")
    depends_on("r-bbmisc@1.10:", type=("build", "run"))
    depends_on("r-checkmate@1.8.2:", type=("build", "run"))
    depends_on("r-fastmatch", type=("build", "run"), when="@1.11:")
