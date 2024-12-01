# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackportsLzma(PythonPackage):
    """Backport of Python 3.3's standard library module
    lzma for LZMA/XY compressed files."""

    homepage = "https://github.com/peterjc/backports.lzma"
    url = "https://github.com/peterjc/backports.lzma/archive/backports.lzma.v0.0.14.tar.gz"

    license("BSD-3-Clause")

    version("0.0.14", sha256="904854d152825b475ebf0f6074fa545474b4ef4eac833f2d9a565e2820dc3a2d")
    version("0.0.13", sha256="42c9d15fa16f691c07e3b325c90f7f9449811e9f7fc46bf4ad43c29bdbaf0b71")
    version("0.0.12", sha256="648592f13d34c7d10791cfb6ce1556cfa25f3657a24e349f266a87708f3af112")
    version("0.0.11", sha256="a4eeb1316fffad0d3ba0857e1a64faa37f02bd77232dd2d5d9798fddc7f094ef")
    version("0.0.10", sha256="5635fd0698beb3294572918ce6e4d01d6bfccb1a3ee27e5013d927b826330e02")
    version("0.0.9", sha256="abd4c6bb808c4732a2b6ebc7a27f63e64c56185a47d8801e49ccfbe809d14d7a")
    version("0.0.8", sha256="ecbad3f91ff125ee6b2095952b6380677e448da20f03597ef779475326a6c713")
    version("0.0.7", sha256="f5de56b740ce47e03de02d5c4983e0e2f19b4f6b0bc4597af6369905177f62cd")
    version("0.0.6", sha256="8e70936641398a6814d70f6eae6399be2ae514578d38b7f9b15c277438bbd853")
    version("0.0.4", sha256="7c973edbd50c1467fed2247117e128a924d25404394a57e30d5b6c52cfcd342d")

    depends_on("c", type="build")  # generated

    depends_on("python@2.6:3.0,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
