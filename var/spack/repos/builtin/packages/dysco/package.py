# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dysco(CMakePackage):
    """Dysco is a compressing storage manager for Casacore mearement sets."""

    homepage = "https://github.com/aroffringa/dysco"
    url = "https://github.com/aroffringa/dysco/archive/v1.2.tar.gz"

    license("GPL-3.0-only")

    version("1.3", sha256="02cb53cc0a95a17a04fbaa6063b39641725b81f279b08e85761b01e8f186609f")
    version("1.2", sha256="dd992c5a13df67173aa1d3f6dc5df9b51b0bea2fe77bc08f5be7a839be741269")

    depends_on("cxx", type="build")  # generated

    depends_on("casacore")
    depends_on("gsl")
    depends_on("boost+date_time+python+container+exception")
