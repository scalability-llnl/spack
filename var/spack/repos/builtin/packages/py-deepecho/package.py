# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDeepecho(PythonPackage):
    """DeepEcho is a Synthetic Data Generation Python library
    for mixed-type, multivariate time series."""

    homepage = "https://github.com/sdv-dev/DeepEcho"
    pypi     = "deepecho/deepecho-0.3.0.post1.tar.gz"

    version('0.3.0.post1', sha256='9f67373a435b5bcd84441c53eae87a2ba17a27574419a59191f92198f400b914')

    depends_on('python@3.6:3.9.999', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.18.0:1.19.999', type=('build', 'run'), when='^python@:3.6.999')
    depends_on('py-numpy@1.20.0:1.999', type=('build', 'run') , when='^python@3.7:')
    depends_on('py-pandas@1.1.3:1.999', type=('build', 'run'))
    depends_on('py-torch@1.8.0:1.999', type=('build', 'run'))
    depends_on('py-tqdm@4.15:4.999', type=('build', 'run'))
