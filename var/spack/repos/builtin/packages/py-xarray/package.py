# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXarray(PythonPackage):
    """N-D labeled arrays and datasets in Python"""

    homepage = "https://github.com/pydata/xarray"
    pypi = "xarray/xarray-0.9.1.tar.gz"

    # 'xarray.tests' requires pytest
    import_modules = [
        'xarray', 'xarray.core', 'xarray.plot', 'xarray.util',
        'xarray.backends', 'xarray.coding'
    ]

    version('0.16.2', sha256='38e8439d6c91bcd5b7c0fca349daf8e0643ac68850c987262d53526e9d7d01e4')
    version('0.14.0', sha256='a8b93e1b0af27fa7de199a2d36933f1f5acc9854783646b0f1b37fed9b4da091')
    version('0.13.0', sha256='80e5746ffdebb96b997dba0430ff02d98028ef3828e6db6106cbbd6d62e32825')
    version('0.12.0', sha256='856fd062c55208a248ac3784cac8d3524b355585387043efc92a4188eede57f3')
    version('0.11.0', sha256='636964baccfca0e5d69220ac4ecb948d561addc76f47704064dcbe399e03a818')
    version('0.9.1', sha256='89772ed0e23f0e71c3fb8323746374999ecbe79c113e3fadc7ae6374e6dc0525')

    variant('io', default=False, description='Build io backends')

    depends_on('python@2.7:2.8,3.5:',   when='@0.11:',  type=('build', 'run'))
    depends_on('python@3.5:',           when='@0.12',   type=('build', 'run'))
    depends_on('python@3.5.3:',         when='@0.13',   type=('build', 'run'))
    depends_on('python@3.6:',           when='@0.14:',  type=('build', 'run'))

    depends_on('py-setuptools',       when='@:0.15', type='build')
    depends_on('py-setuptools@38.4:', when='@0.16:', type=('build', 'run'))
    depends_on('py-setuptools-scm',   when='@0.15:', type='build')

    depends_on('py-pandas@0.15.0:', when='@0.9.1',      type=('build', 'run'))
    depends_on('py-pandas@0.19.2:', when='@0.11:0.13',  type=('build', 'run'))
    depends_on('py-pandas@0.24:',   when='@0.14.0',     type=('build', 'run'))
    depends_on('py-pandas@0.25:',   when='@0.15:',      type=('build', 'run'))

    depends_on('py-numpy@1.7:',     when='@0.9.1',      type=('build', 'run'))
    depends_on('py-numpy@1.12:',    when='@0.11:0.13',  type=('build', 'run'))
    depends_on('py-numpy@1.14:',    when='@0.14.0',     type=('build', 'run'))
    depends_on('py-numpy@1.15:',    when='@0.15:',      type=('build', 'run'))

    depends_on('py-netcdf4',  when='+io', type=('build', 'run'))
    depends_on('py-h5netcdf', when='+io', type=('build', 'run'))
    depends_on('py-scipy',    when='+io', type=('build', 'run'))
    depends_on('py-pydap',    when='+io', type=('build', 'run'))
    depends_on('py-zarr',     when='+io', type=('build', 'run'))
    depends_on('py-fsspec',   when='+io', type=('build', 'run'))
    depends_on('py-cftime',   when='+io', type=('build', 'run'))
    depends_on('py-rasterio', when='+io', type=('build', 'run'))
    depends_on('py-cfgrib',   when='+io', type=('build', 'run'))
