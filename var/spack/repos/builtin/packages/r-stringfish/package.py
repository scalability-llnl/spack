# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RStringfish(RPackage):
    """Alt String Implementation

    Provides an extendable, performant and multithreaded 'alt-string'
    implementation backed by 'C++' vectors and strings."""

    homepage = "https://github.com/traversc/stringfish"
    url      = "https://cloud.r-project.org/src/contrib/stringfish_0.14.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/stringfish"

    maintainers = ['dorton21']

    version('0.14.2', sha256='9373cfc715cda1527fd20179435977b8e59e19d8c5ef82a31e519f93fb624ced')

    depends_on('gmake', type='build')
    depends_on('r@3.5.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.18.3:', type=('build', 'run'))
    depends_on('r-rcppparallel', type=('build', 'run'))
