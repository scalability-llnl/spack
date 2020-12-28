# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyCvxpy(PythonPackage):
    """Convex optimization, for everyone."""

    homepage = "https://www.cvxpy.org/index.html"
    url      = "https://www.pypi.io/packages/source/c/cvxpy/cvxpy-1.0.25.tar.gz"

    version('1.0.25', sha256='8535529ddb807067b0d59661dce1d9a6ddb2a218398a38ea7772328ad8a6ea13')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.15:',        type=('build', 'run'))
    depends_on('py-scipy@1.1.0:',        type=('build', 'run'))
    depends_on('py-ecos@2:',        type=('build', 'run'))
    depends_on('py-scs@1.1.3:',        type=('build', 'run'))
    depends_on('py-osqp@0.4.1',        type=('build', 'run'))
    depends_on('py-multiprocess', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
