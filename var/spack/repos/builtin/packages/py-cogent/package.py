# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyCogent(PythonPackage):
    """A toolkit for statistical analysis of biological sequences."""

    homepage = "http://pycogent.org"
    url      = "https://pypi.io/packages/source/c/cogent/cogent-1.9.tar.gz"

    version('1.9', sha256='57d8c58e0273ffe4f2b907874f9b49dadfd0600f5507b7666369f4e44d56ce14')
    version('1.5.3', url="https://pypi.io/packages/source/c/cogent/cogent-1.5.3.tgz",
            sha256='1215ac219070b7b2207b0b47b4388510f3e30ccd88160aa9f02f25d24bcbcd95')

    variant('matplotlib', default=False, description="graphs related to codon usage")
    variant('mpi', default=False, description='MPI required for parallel computation.')
    variant('mysql', default=False, description='Required for the Ensembl querying code.')

    depends_on('py-setuptools', type=('build'), when='@1.9')
    depends_on('python@2.6:2.999', type=('build', 'run'))
    depends_on('py-numpy@1.3:', type=('build', 'run'))
    depends_on('zlib')
    depends_on('py-matplotlib', when='+matplotlib', type=('build', 'run'))
    depends_on('py-mpi4py', when='+mpi', type=('build', 'run'))
    depends_on('py-sqlalchemy', when='+mysql', type=('build', 'run'))
    depends_on('py-pymysql', when='+mysql', type=('build', 'run'))
    depends_on('py-cython@0.17.1:', type='build')

    def setup_build_environment(self, env):
        env.set('DONT_USE_PYREX', '1')
