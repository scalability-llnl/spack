# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNp(RPackage):
    """Nonparametric Kernel Smoothing Methods for Mixed Data Types.

    This package provides a variety of nonparametric (and semiparametric)
    kernel methods that seamlessly handle a mix of continuous, unordered, and
    ordered factor data types. We would like to gratefully acknowledge support
    from the Natural Sciences and Engineering Research Council of Canada
    (NSERC:www.nserc.ca), the Social Sciences and Humanities Research Council
    of Canada (SSHRC:www.sshrc.ca), and the Shared Hierarchical Academic
    Research Computing Network (SHARCNET:www.sharcnet.ca)."""

    cran = "np"

    license("GPL-2.0-or-later")

    version("0.60-17", sha256="d97957cb234ec2e570fc2d02d305eadff3d71939484b3d1054ed8b67a3427f36")
    version("0.60-16", sha256="bef967c0195059e53c68e64d7540bf4627415c832f050c8806520ab8796e01b0")
    version("0.60-14", sha256="342b7f51e44eee556a9bb1f2ac9a143006019ca398fdccbb9c4562db3883d56c")
    version("0.60-11", sha256="a3b31b8ad70c42826076786b2b1b63b79cdbadfa55fe126773bc357686fd33a9")
    version("0.60-10", sha256="a27b4bbca8b83a289c98920c1c8f5e9979ba9772086893252a4297dd2698081a")
    version("0.60-9", sha256="fe31a8985f0b1a576a7775022b7131093b1c9a8337734136d5fcad85fa6592fc")
    version("0.60-8", sha256="924c342feb2a862fa3871a45db5f8434dbbfb900cfc40c001a0872108a3a069e")
    version("0.60-2", sha256="25d667fc1056899516584b9d5d933377e6f4694d8e5e868dd047db572b69417f")

    depends_on("c", type="build")  # generated

    depends_on("r-boot", type=("build", "run"))
    depends_on("r-cubature", type=("build", "run"))
    depends_on("r-quadprog", type=("build", "run"), when="@0.60-8:")
    depends_on("r-quantreg", type=("build", "run"), when="@0.60-8:")
