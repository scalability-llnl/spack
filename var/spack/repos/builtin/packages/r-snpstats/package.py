# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSnpstats(RPackage):
    """SnpMatrix and XSnpMatrix classes and methods.

    Classes and statistical methods for large SNP association studies. This
    extends the earlier snpMatrix package, allowing for uncertainty in
    genotypes."""

    bioc = "snpStats"

    version("1.50.0", commit="b6d42f93f2ce510cc10a1668809218f317c23d2a")
    version("1.48.0", commit="7d4cec7275b9360d98cb59d15c4140bed3e6a74c")
    version("1.46.0", commit="1e70784b113eaca231bc5f91fc8ae5aadb151ddb")
    version("1.44.0", commit="72392dab4e75de2da459b1e95f1d48947811597b")
    version("1.40.0", commit="5fcac6f3b4bb6f45c19dff8f3089b693b74a56ce")
    version("1.34.0", commit="e31cdfb18a9e12d70d6a3e8e6fbf7cf8faa3ea5b")
    version("1.32.0", commit="7c31158183b4e39da6dc30c7da275acc36b2e32f")
    version("1.30.0", commit="0dc1e4246f015feaf2579d60268b10ab5149ce09")
    version("1.28.0", commit="8df9f4188f720dfbb4f4f4ec255cd2e22f3f4426")
    version("1.26.0", commit="7c9b3304073e0556d694a8531882b349822fdda8")

    depends_on("c", type="build")  # generated

    depends_on("r@2.10.0:", type=("build", "run"))
    depends_on("r-survival", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))
    depends_on("r-biocgenerics", type=("build", "run"))
    depends_on("r-zlibbioc", type=("build", "run"))
    depends_on("zlib-api")
