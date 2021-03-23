# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack import *


class PyXgboost(PythonPackage):
    """XGBoost is an optimized distributed gradient boosting library designed to be
    highly efficient, flexible and portable."""

    homepage  = 'https://xgboost.ai/'
    pypi = 'xgboost/xgboost-1.3.3.tar.gz'

    maintainers = ['adamjstewart']
    import_modules = ['xgboost']

    version('1.3.3', sha256='397051647bb837915f3ff24afc7d49f7fca57630ffd00fb5ef66ae2a0881fb43')
    version('0.90',  sha256='d69f90d61a63e8889fd39a31ad00c629bac1ca627f8406b9b6d4594c9e29ab84', deprecated=True)

    variant('pandas',       default=False, description='Enable Pandas extensions for training.')
    variant('scikit-learn', default=False, description='Enable scikit-learn extensions for training.')
    variant('dask',         default=False, description='Enables Dask extensions for distributed training.')
    variant('plotting',     default=False, description='Enables tree and importance plotting.')

    for ver in ['1.3.3']:
        depends_on('xgboost@' + ver, when='@' + ver)

    depends_on('cmake@3.12:', when='@1.0:1.2.999', type='build')
    depends_on('llvm-openmp', when='@:1.2.999 %apple-clang')
    depends_on('python@3.6:', when='@1.2:', type=('build', 'run'))
    depends_on('python@3.5:', when='@1.0:', type=('build', 'run'))
    depends_on('python@3.4:',   type=('build', 'run'))
    depends_on('py-setuptools', type=('build'))
    depends_on('py-numpy',      type=('build', 'run'))
    depends_on('py-scipy',      type=('build', 'run'))

    depends_on('py-pandas', when='+pandas', type=('build', 'run'))

    depends_on('py-scikit-learn', when='+scikit-learn', type=('build', 'run'))

    depends_on('py-dask',        when='+dask', type=('build', 'run'))
    depends_on('py-pandas',      when='+dask', type=('build', 'run'))
    depends_on('py-distributed', when='+dask', type=('build', 'run'))

    depends_on('py-graphviz',   when='+plotting', type=('build', 'run'))
    depends_on('py-matplotlib', when='+plotting', type=('build', 'run'))

    conflicts('+pandas', when='@:0.999')
    conflicts('+scikit-learn', when='@:0.999')
    conflicts('+dask', when='@:0.999')
    conflicts('+plotting', when='@:0.999')

    # `--use-system-libxgboost` is only valid for the 'install' phase, but we want to
    # skip building of the C++ library and rely on an external dependency
    phases = ['install']

    @when('@:0.90')
    def patch(self):
        # Fix OpenMP support on macOS
        filter_file("OPENMP_FLAGS = -fopenmp",
                    "OPENMP_FLAGS = {0}".format(self.compiler.openmp_flag),
                    os.path.join("xgboost", "Makefile"), string=True)

    @when('@1.3:')
    def patch(self):
        # https://github.com/dmlc/xgboost/issues/6706
        # 'setup.py' is hard-coded to search in Python installation prefix
        filter_file("lib_path = os.path.join(sys.prefix, 'lib')",
                    "lib_path = '{0}'".format(self.spec['xgboost'].libs.directories[0]),
                    "setup.py", string=True)

        # Same for run-time search
        filter_file("os.path.join(curr_path, 'lib'),",
                    "'{0}',".format(self.spec['xgboost'].libs.directories[0]),
                    os.path.join('xgboost', 'libpath.py'), string=True)

    @when('@1.3:')
    def install_args(self, spec, prefix):
        args = super(PyXgboost, self).install_args(spec, prefix)
        args.append('--use-system-libxgboost')
        return args

    # Tests need to be re-added since `phases` was overridden
    run_after('install')(
        PythonPackage._run_default_install_time_test_callbacks)
    run_after('install')(PythonPackage.sanity_check_prefix)
