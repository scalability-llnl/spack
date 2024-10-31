# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGower(RPackage):
    """Gower's Distance.

    Compute Gower's distance (or similarity) coefficient between records.
    Compute the top-n matches between records. Core algorithms are executed in
    parallel on systems supporting OpenMP."""

    cran = "gower"

    license("GPL-3.0-only")

    version("1.0.1", sha256="296a9d8e5efa8c3a8cc6b92cf38880915753afdef30281629af9dc8eae8315fc")
    version("1.0.0", sha256="671cb7baafe05140d822e8f26f9cd3576fc3bf4c6572b7223fb54da754ea385d")
    version("0.2.2", sha256="3f022010199fafe34f6e7431730642a76893e6b4249b84e5a61012cb83483631")
    version("0.2.1", sha256="af3fbe91cf818c0841b2c0ec4ddf282c182a588031228c8d88f7291b2cdff100")

    depends_on("c", type="build")  # generated
