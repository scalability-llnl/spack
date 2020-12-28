# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNleqslv(RPackage):
    """nleqslv: Solve Systems of Nonlinear Equations"""

    homepage = "https://cloud.r-project.org/package=nleqslv"
    url      = "https://cloud.r-project.org/src/contrib/nleqslv_3.3.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/nleqslv"

    version('3.3.2', sha256='f54956cf67f9970bb3c6803684c84a27ac78165055745e444efc45cfecb63fed')
