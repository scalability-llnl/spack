# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyGraphqlCore(PythonPackage):
    """GraphQL-core 3 is a Python 3.6+ port of GraphQL.js, the
    JavaScript reference implementation for GraphQL, a query language
    for APIs created by Facebook."""

    homepage = "https://github.com/graphql-python/graphql-core"
    url      = "https://github.com/graphql-python/graphql-core/archive/v3.1.2.tar.gz"

    version('3.1.2', sha256='16087360d34f9cfa295b401fc17f9f11bcddef0e6e0dc5a694bbe2298b31949b')
    version('3.0.5', sha256='88021f8b879f18cf56523644e51e1552b126a9ad9ab218f579bf503d236d5272')

    depends_on('python@3.6:3.999', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
