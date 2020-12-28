# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Su2(MesonPackage):
    """SU2 is a suite of open-source software tools written in C++ for
    the numerical solution of partial differential equations (PDE) and
    performing PDE constrained optimization."""

    homepage = "https://su2code.github.io"
    url      = "https://github.com/su2code/SU2/archive/v7.0.3.tar.gz"

    version('7.0.3', sha256='7fc01deaad9baabbe0ccd162a4b565172d49e573e79abcb65433b51ff29bda06')
    version('7.0.2', sha256='69e51d52c5a84fb572bd6a83faf8f9fd04471fbf7d5b70d967c7306c1d4e17d9')
    version('7.0.1', sha256='eb0550c82ccaef8cb71e4a8775aa71d2020ef085ec3dd19dfafff5d301034f6f')
    version('7.0.0', sha256='6207dcca15eaebc11ce12b2866c937b4ad9b93274edf6f23d0487948ac3963b8')
    version('6.2.0', sha256='ffc953326e8432a1a6534556a5f6cf086046d3149cfcec6b4e7390eebe30ce2e')

    depends_on('python@3:', type=('build', 'run'))
