# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyarrow(PythonPackage, CudaPackage):
    """A cross-language development platform for in-memory data.

    This package contains the Python bindings.
    """

    homepage = "https://arrow.apache.org"
    url = 'https://pypi.io/packages/source/p/pyarrow/pyarrow-0.17.1.tar.gz'

    version('0.17.1', sha256='278d11800c2e0f9bea6314ef718b2368b4046ba24b6c631c14edad5a1d351e49')
    version('0.15.1', sha256='7ad074690ba38313067bf3bbda1258966d38e2037c035d08b9ffe3cce07747a5')
    version('0.12.1', sha256='10db6e486c918c3af999d0114a22d92770687e3a6607ea3f14e6748854824c2a')
    version('0.11.0', sha256='07a6fd71c5d7440f2c42383dd2c5daa12d7f0a012f1e88288ed08a247032aead')
    version('0.9.0', sha256='7db8ce2f0eff5a00d6da918ce9f9cfec265e13f8a119b4adb1595e5b19fd6242')

    variant('parquet', default=False, description="Build with Parquet support")
    variant('orc', default=False, description='Build with orc support')

    depends_on('cmake@3.0.0:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('python@3.5:', type=('build', 'run'), when='@0.17:')
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build', when='@0.15.0:')
    depends_on('py-cython', type='build')
    depends_on('py-cython@0.29:', type='build', when='@0.15.0:')
    depends_on('py-numpy@1.14:', type=('build', 'run'), when='@0.15.0:')
    depends_on('py-six@1.0.0:', type=('build', 'run'), when='@0.15.0:')
    depends_on('py-futures', type=('build', 'run'), when='@0.15.0:^python@:3.1.99')
    depends_on('py-enum34@1.1.6:', type=('build', 'run'), when='@0.15.0:^python@:3.3.99')

    for v in ('@0.9.0', '@0.11.0', '@0.12.1', '@0.15.1', '@0.17.1'):
        depends_on('arrow+python' + v, when=v)
        depends_on('arrow+parquet+python' + v, when='+parquet' + v)
        depends_on('arrow+cuda' + v, when='+cuda' + v)
        depends_on('arrow+orc' + v, when='+orc' + v)

    phases = ['build_ext', 'install']

    patch('for_aarch64.patch', when='target=aarch64:')

    def build_ext_args(self, spec, prefix):
        args = []
        if spec.satisfies('+parquet'):
            args.append('--with-parquet')
        if spec.satisfies('+cuda'):
            args.append('--with-cuda')
        if spec.satisfies('+orc'):
            args.append('--with-orc')
        return args
