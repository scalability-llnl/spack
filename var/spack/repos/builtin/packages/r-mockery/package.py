# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMockery(RPackage):
    """The two main functionalities of this package are creating mock
    objects (functions) and selectively intercepting calls to a given
    function that originate in some other function. It can be used with
    any testing framework available for R. Mock objects can be injected
    with either this package's own stub() function or a similar
    with_mock() facility present in the 'testthat' package."""

    homepage = "https://github.com/r-lib/mockery"
    url      = "https://cran.r-project.org/src/contrib/mockery_0.4.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/mockery"

    version('0.4.2', sha256='988e249c366ee7faf277de004084cf5ca24b5c8a8c6e3842f1b1362ce2f7ea9b')
    version('0.4.1', sha256='959d83f8b21e9a89c06c73f310356790c2d63d5ba39b2b60c6777a4eb33909c1')
    version('0.4.0', sha256='cecbd865b67d8d29b47d6c931e386189625d5885328a2931a65ade3ff9bc8e7b')
    version('0.3.0', sha256='6d23461ce6ffdc707ac2fcef58c5942587fab4b2a794a3085ac858fe1beeaff9')

    depends_on('r-testthat', type=('build', 'run'))
