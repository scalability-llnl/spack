# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCaracas(RPackage):
    """Computer algebra via the 'SymPy' library (<https://www.sympy.org/>).
       This makes it possible to solve equations symbolically, find symbolic
       integrals, symbolic sums and other important quantities.
    """

    homepage = "https://cloud.r-project.org/package=caracas"
    url      = "https://cloud.r-project.org/src/contrib/caracas_1.0.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/caracas"

    version('1.0.0', sha256='0da6f1d94d1dacb1c11a3635bdff8f7cd8f84373deffa7126636d0876d48e42b')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-reticulate@1.14:', type=('build', 'run'))
    depends_on('python@3.6:', type=('build', 'run'))
