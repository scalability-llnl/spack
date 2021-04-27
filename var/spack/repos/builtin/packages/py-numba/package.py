# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyNumba(PythonPackage):
    """NumPy aware dynamic Python compiler using LLVM"""

    homepage = "https://numba.pydata.org/"
    pypi = "numba/numba-0.35.0.tar.gz"

    version('0.51.1', sha256='1e765b1a41535684bf3b0465c1d0a24dcbbff6af325270c8f4dad924c0940160')
    version('0.50.1', sha256='89e81b51b880f9b18c82b7095beaccc6856fcf84ba29c4f0ced42e4e5748a3a7')
    version('0.48.0', sha256='9d21bc77e67006b5723052840c88cc59248e079a907cc68f1a1a264e1eaba017')
    version('0.40.1', sha256='52d046c13bcf0de79dbfb936874b7228f141b9b8e3447cc35855e9ad3e12aa33')
    version('0.35.0', sha256='11564937757605bee590c5758c73cfe9fd6d569726b56d970316a6228971ecc3')

    depends_on('python@3.6:', type=('build', 'run'), when='@0.48.0:')
    depends_on('python@3.3:3.7.9999', type=('build', 'run'), when='@0.40.1:0.47.999')
    depends_on('python@3.3:3.6.9999', type=('build', 'run'), when='@:0.35.0')
    depends_on('py-numpy@1.15:', type=('build', 'run'), when='@0.48.0:')
    depends_on('py-numpy@1.10:1.99', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))

    # Note: As of 1 Nov 2018, 0.25 was the latest version of py-llvmlite.
    # That's why it was chosen as an upper bound in the following depends_on
    # calls.  If newer versions maintain backwards compatibility, the calls
    # can be updated accordingly.
    depends_on('py-llvmlite@0.34.0:0.34.999', type=('build', 'run'), when='@0.51.1')
    depends_on('py-llvmlite@0.33.0:0.33.999', type=('build', 'run'), when='@0.50.1')
    depends_on('py-llvmlite@0.31.0:0.31.999', type=('build', 'run'), when='@0.48.0')
    depends_on('py-llvmlite@0.25.0:',         type=('build', 'run'), when='@0.40.1')
    depends_on('py-llvmlite@0.20:0.25',       type=('build', 'run'), when='@0.35.1')

    depends_on('py-argparse', type=('build', 'run'), when='^python@:2.6')
    depends_on('py-funcsigs', type=('build', 'run'), when='^python@:3.3.99')
    depends_on('py-singledispatch', type=('build', 'run'), when='^python@:3.3.99')

    # Version 6.0.0 of llvm had a hidden symbol which breaks numba at runtime.
    # See https://reviews.llvm.org/D44140
    conflicts('^llvm@6.0.0')
