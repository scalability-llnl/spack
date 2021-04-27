# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyDaskGlm(PythonPackage):
    """Dask-glm is a library for fitting Generalized Linear Models on
       large datasets."""

    homepage = "https://dask-glm.readthedocs.io/en/latest/"
    pypi = "dask-glm/dask-glm-0.2.0.tar.gz"

    version('0.2.0', sha256='58b86cebf04fe5b9e58092e1c467e32e60d01e11b71fdc628baaa9fc6d1adee5')

    variant('docs', default=False, description='Build HTML documentation')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-cloudpickle@0.2.2:', type=('build', 'run'))
    depends_on('py-dask+array', type=('build', 'run'))
    depends_on('py-multipledispatch@0.4.9:', type=('build', 'run'))
    depends_on('py-scipy@0.18.1:', type=('build', 'run'))
    depends_on('py-scikit-learn@0.18:', type=('build', 'run'), when='~docs')
    depends_on('py-scikit-learn@0.18:0.21.999', type=('build', 'run'), when='+docs')
    depends_on('py-jupyter', type='build', when='+docs')
    depends_on('py-nbsphinx', type='build', when='+docs')
    depends_on('py-notebook', type='build', when='+docs')
    depends_on('py-numpydoc', type='build', when='+docs')
    depends_on('py-sphinx', type='build', when='+docs')
    depends_on('py-sphinx-rtd-theme', type='build', when='+docs')
    depends_on('pandoc', type='build', when='+docs')
    depends_on('py-pip', type='build', when='+docs')
    depends_on('py-s3fs', type='build', when='+docs')
    depends_on('py-matplotlib', type='build', when='+docs')
    depends_on('llvm@:10.0.1~flang', type='build', when='+docs')
    depends_on('cairo+X+ft+fc+pdf+gobject', type='build', when='+docs')
    depends_on('harfbuzz+graphite2', type='build', when='+docs')

    @run_after('install')
    def install_docs(self):
        if '+docs' in self.spec:
            with working_dir('docs'):
                make('html')
            install_tree('docs', self.prefix.docs)
