# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeeptools(PythonPackage):
    """deepTools addresses the challenge of handling the large amounts of data
       that are now routinely generated from DNA sequencing centers."""

    homepage = "https://pypi.io/packages/source/d/deepTools"
    # The test suite and associated test data is missing in the pypi tarball.
    url      = "https://github.com/deeptools/deepTools/archive/3.3.0.tar.gz"

    version('3.3.0', sha256='a7aaf79fe939ca307fe6ec5e156750389fdfa4324bf0dd6bf5f53d5fda109358')
    version('3.2.1', sha256='dbee7676951a9fdb1b88956fe4a3294c99950ef193ea1e9edfba1ca500bd6a75')
    version('2.5.2', sha256='16d0cfed29af37eb3c4cedd9da89b4952591dc1a7cd8ec71fcba87c89c62bf79')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.9.0:', type=('build', 'run'))
    depends_on('py-scipy@0.17.0:', type=('build', 'run'))
    depends_on('py-py2bit@0.2.0:', type=('build', 'run'))
    depends_on('py-pybigwig@0.2.1:', type=('build', 'run'))
    depends_on('py-pysam@0.14.0:', type=('build', 'run'))
    depends_on('py-matplotlib@2.1.2:', type=('build', 'run'))
    depends_on('py-numpydoc@0.5:', type=('build', 'run'))
    depends_on('py-plotly@2.0.0:', type=('build', 'run'))
    depends_on('py-deeptoolsintervals@0.1.8:', type=('build', 'run'))

    def patch(self):
        # Add nosetest hook for "python setup.py test" argument.
        filter_file(r'^setup\(',
                    r'''setup(
    tests_require='nose',
    test_suite='nose.collector',''',
                    'setup.py')
