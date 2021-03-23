# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDask(PythonPackage):
    """Dask is a flexible parallel computing library for analytics."""

    homepage = "https://github.com/dask/dask/"
    pypi = "dask/dask-1.1.0.tar.gz"

    maintainers = ['skosukhin']

    version('2020.12.0', sha256='43e745afd4b464e6c0113131e430a16dce6ac42460b06e24d799093d098f7ab0')
    version('2.16.0', sha256='2af5b0dcd48ce679ce0321cf91de623f4fe376262789b951fefa3c334002f350')
    version('1.2.2', sha256='5e7876bae2a01b355d1969b73aeafa23310febd8c353163910b73e93dc7e492c')
    version('1.1.2', sha256='93b355b9a9c9a3ddbb39fab99d5759aad5cfd346f4520b87788970e80cf97256')
    version('1.1.0', sha256='e76088e8931b326c05a92d2658e07b94a6852b42c13a7560505a8b2354871454')
    version('0.17.4', sha256='c111475a3d1f8cba41c8094e1fb1831c65015390dcef0308042a11a9606a2f6d')
    version('0.8.1',  sha256='43deb1934cd033668e5e60b735f45c9c3ee2813f87bd51c243f975e55267fa43')

    variant('array',       default=True, description='Install requirements for dask.array')
    variant('bag',         default=True, description='Install requirements for dask.bag')
    variant('dataframe',   default=True, description='Install requirements for dask.dataframe')
    variant('distributed', default=True, description='Install requirements for dask.distributed')
    variant('diagnostics', default=False, description='Install requirements for dask.diagnostics')
    variant('delayed',     default=True, description='Install requirements for dask.delayed (dask.imperative)')
    variant('yaml',        default=True, description='Ensure support for YAML configuration files')

    conflicts('+distributed', when='@:0.4.0,0.7.6:0.8.1')
    conflicts('+diagnostics', when='@:0.5.0')
    conflicts('+yaml', when='@:0.17.5')
    conflicts('~yaml', when='@2.17.1:')

    depends_on('python@2.7:2.8,3.5:',   type=('build', 'run'))
    depends_on('python@3.5:',           type=('build', 'run'), when='@2.0.0:')
    depends_on('python@3.6:',           type=('build', 'run'), when='@2.7.0:')

    depends_on('py-setuptools',         type='build')

    # Requirements for dask.array
    depends_on('py-numpy@1.10.4:',      type=('build', 'run'), when='+array')
    depends_on('py-numpy@1.11.0:',      type=('build', 'run'), when='@0.17.3: +array')
    depends_on('py-numpy@1.13.0:',      type=('build', 'run'), when='@1.2.1: +array')
    depends_on('py-numpy@1.15.1:',      type=('build', 'run'), when='@2020.12.0: +array')

    depends_on('py-toolz',              type=('build', 'run'), when='+array')
    depends_on('py-toolz@0.7.2:',       type=('build', 'run'), when='@0.7.0: +array')
    depends_on('py-toolz@0.7.3:',       type=('build', 'run'), when='@0.14.1: +array')
    depends_on('py-toolz@0.8.2:',       type=('build', 'run'), when='@2.13.0: +array')

    # Requirements for dask.bag
    depends_on('py-dill',               type=('build', 'run'), when='@:0.7.5 +bag')
    depends_on('py-cloudpickle',        type=('build', 'run'), when='@0.7.6: +bag')
    depends_on('py-cloudpickle@0.2.1:', type=('build', 'run'), when='@0.8.2: +bag')
    depends_on('py-cloudpickle@0.2.2:', type=('build', 'run'), when='@2.13.0: +bag')

    depends_on('py-fsspec@0.3.3:',      type=('build', 'run'), when='@2.2.0: +bag')
    depends_on('py-fsspec@0.5.1:',      type=('build', 'run'), when='@2.5.0: +bag')
    depends_on('py-fsspec@0.6.0:',      type=('build', 'run'), when='@2.8.0: +bag')

    depends_on('py-toolz',              type=('build', 'run'), when='+bag')
    depends_on('py-toolz@0.7.2:',       type=('build', 'run'), when='@0.7.0: +bag')
    depends_on('py-toolz@0.7.3:',       type=('build', 'run'), when='@0.14.1: +bag')
    depends_on('py-toolz@0.8.2:',       type=('build', 'run'), when='@2.13.0: +bag')

    depends_on('py-partd',              type=('build', 'run'), when='+bag')
    depends_on('py-partd@0.3.2:',       type=('build', 'run'), when='@0.6.0: +bag')
    depends_on('py-partd@0.3.3:',       type=('build', 'run'), when='@0.9.0: +bag')
    depends_on('py-partd@0.3.5:',       type=('build', 'run'), when='@0.10.2: +bag')
    depends_on('py-partd@0.3.6:',       type=('build', 'run'), when='@0.12.0: +bag')
    depends_on('py-partd@0.3.7:',       type=('build', 'run'), when='@0.13.0: +bag')
    depends_on('py-partd@0.3.8:',       type=('build', 'run'), when='@0.15.0: +bag')
    depends_on('py-partd@0.3.10:',      type=('build', 'run'), when='@2.0.0: +bag')

    # Requirements for dask.dataframe
    depends_on('py-numpy@1.10.4:',      type=('build', 'run'), when='+dataframe')
    depends_on('py-numpy@1.11.0:',      type=('build', 'run'), when='@0.17.3: +dataframe')
    depends_on('py-numpy@1.13.0:',      type=('build', 'run'), when='@1.2.1: +dataframe')
    depends_on('py-numpy@1.15.1:',      type=('build', 'run'), when='@2020.12.0: +dataframe')

    depends_on('py-pandas@0.16.0:',     type=('build', 'run'), when='+dataframe')
    depends_on('py-pandas@0.18.0:',     type=('build', 'run'), when='@0.9.0: +dataframe')
    depends_on('py-pandas@0.19.0:',     type=('build', 'run'), when='@0.14.0: +dataframe')
    depends_on('py-pandas@0.21.0:',     type=('build', 'run'), when='@1.2.1: +dataframe')
    depends_on('py-pandas@0.23.0:',     type=('build', 'run'), when='@2.11.0: +dataframe')
    depends_on('py-pandas@0.25.0:',     type=('build', 'run'), when='@2020.12.0: +dataframe')

    depends_on('py-toolz',              type=('build', 'run'), when='+dataframe')
    depends_on('py-toolz@0.7.2:',       type=('build', 'run'), when='@0.7.0: +dataframe')
    depends_on('py-toolz@0.7.3:',       type=('build', 'run'), when='@0.14.1: +dataframe')
    depends_on('py-toolz@0.8.2:',       type=('build', 'run'), when='@2.13.0: +dataframe')

    depends_on('py-partd',              type=('build', 'run'), when='+dataframe')
    depends_on('py-partd@0.3.2:',       type=('build', 'run'), when='@0.6.0: +dataframe')
    depends_on('py-partd@0.3.3:',       type=('build', 'run'), when='@0.9.0: +dataframe')
    depends_on('py-partd@0.3.5:',       type=('build', 'run'), when='@0.10.2: +dataframe')
    depends_on('py-partd@0.3.7:',       type=('build', 'run'), when='@0.13.0: +dataframe')
    depends_on('py-partd@0.3.8:',       type=('build', 'run'), when='@0.15.0: +dataframe')
    depends_on('py-partd@0.3.10:',      type=('build', 'run'), when='@2.0.0: +dataframe')

    depends_on('py-cloudpickle@0.2.1:', type=('build', 'run'), when='@0.8.2:2.6.0 +dataframe')

    depends_on('py-fsspec@0.3.3:',      type=('build', 'run'), when='@2.2.0: +dataframe')
    depends_on('py-fsspec@0.5.1:',      type=('build', 'run'), when='@2.5.0: +dataframe')
    depends_on('py-fsspec@0.6.0:',      type=('build', 'run'), when='@2.8.0: +dataframe')

    # Requirements for dask.distributed
    depends_on('py-dill',               type=('build', 'run'), when='@:0.7.5 +distributed')
    depends_on('py-pyzmq',              type=('build', 'run'), when='@:0.7.5 +distributed')
    depends_on('py-distributed',        type=('build', 'run'), when='@0.8.2: +distributed')
    depends_on('py-distributed@1.9:',   type=('build', 'run'), when='@0.9.0: +distributed')
    depends_on('py-distributed@1.10:',  type=('build', 'run'), when='@0.10.0: +distributed')
    depends_on('py-distributed@1.14:',  type=('build', 'run'), when='@0.12.0: +distributed')
    depends_on('py-distributed@1.15:',  type=('build', 'run'), when='@0.13.0: +distributed')
    depends_on('py-distributed@1.16:',  type=('build', 'run'), when='@0.14.1: +distributed')
    depends_on('py-distributed@1.20:',  type=('build', 'run'), when='@0.16.0: +distributed')
    depends_on('py-distributed@1.21:',  type=('build', 'run'), when='@0.17.0: +distributed')
    depends_on('py-distributed@1.22:',  type=('build', 'run'), when='@0.18.0: +distributed')
    depends_on('py-distributed@2.0:',   type=('build', 'run'), when='@2.0.0: +distributed')

    # Requirements for dask.diagnostics
    depends_on('py-bokeh',              type=('build', 'run'), when='+diagnostics')
    depends_on('py-bokeh@1.0.0:',       type=('build', 'run'), when='@2.0.0: +diagnostics')
    depends_on('py-bokeh@1.0.0:1.999,2.0.1:', type=('build', 'run'), when='@2.26.0: +diagnostics')

    # Requirements for dask.delayed
    depends_on('py-cloudpickle@0.2.1:', type=('build', 'run'), when='@2,7.0: +delayed')
    depends_on('py-cloudpickle@0.2.2:', type=('build', 'run'), when='@2.13.0: +delayed')

    depends_on('py-toolz@0.7.2:',       type=('build', 'run'), when='@0.8.1: +delayed')
    depends_on('py-toolz@0.7.3:',       type=('build', 'run'), when='@0.14.1: +delayed')
    depends_on('py-toolz@0.8.2:',       type=('build', 'run'), when='@2.13.0: +delayed')

    # Support for YAML configuration files
    depends_on('py-pyyaml',             type=('build', 'run'), when='+yaml')

    @property
    def import_modules(self):
        modules = ['dask']

        if self.spec.satisfies('@0.9.0:'):
            modules.append('dask.bytes')

        if self.spec.satisfies('@:0.20.2'):
            modules.append('dask.store')

        if '+array' in self.spec:
            modules.append('dask.array')

        if '+bag' in self.spec:
            modules.append('dask.bag')

        if self.spec.satisfies('@:0.7.5 +distributed'):
            modules.append('dask.distributed')

        if '+dataframe' in self.spec:
            modules.append('dask.dataframe')
            if self.spec.satisfies('@0.8.2:'):
                modules.append('dask.dataframe.tseries')
            if self.spec.satisfies('@0.12.0:'):
                modules.append('dask.dataframe.io')

        if '+diagnostics' in self.spec:
            modules.append('dask.diagnostics')

        return modules
