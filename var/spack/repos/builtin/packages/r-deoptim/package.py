# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RDeoptim(RPackage):
    """Global Optimization by Differential Evolution

    Implements the differential evolution algorithm for global optimization
    of a real-valued function of a real-valued parameter vector."""

    homepage = "https://cloud.r-project.org/package=DEoptim"
    url      = "https://cloud.r-project.org/src/contrib/DEoptim_2.2-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/DEoptim"

    version('2.2-5', sha256='ae12dedcd4a43994e811e7285f8c12bfdb688e7c99d65515cf7e8cb6db13955a')
    version('2.2-4', sha256='0a547784090d1e9b93efc53768110621f35bed3692864f6ce5c0dda2ebd6d482')
    version('2.2-3', sha256='af2120feea3a736ee7a5a93c6767d464abc0d45ce75568074b233405e73c9a5d')
