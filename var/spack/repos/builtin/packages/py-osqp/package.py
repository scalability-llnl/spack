# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyOsqp(PythonPackage):
    """OSQP: The Operator Splitting QP Solver"""

    homepage = "https://osqp.org/"
    url      = "https://pypi.io/packages/source/o/osqp/osqp-0.6.1.tar.gz"

    version('0.6.1', sha256='47b17996526d6ecdf35cfaead6e3e05d34bc2ad48bcb743153cefe555ecc0e8c')

    depends_on('cmake', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.7:',        type=('build', 'run'))
    depends_on('py-scipy@0.13.2:',        type=('build', 'run'))
    depends_on('py-future',        type=('build', 'run'))
