# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCorrectionlib(PythonPackage):
    """A generic correction library"""

    homepage = "https://github.com/cms-nanoAOD/correctionlib"
    pypi     = "correctionlib/correctionlib-2.0.0.tar.gz"

    version('2.0.0', sha256='e4d240cbdb2633a8955ddcd02d5b9bfb33d7e1a33554d6f7957f2dec56988a67')

    variant('convert', default=False,
            description='Includes select conversion routines for common types')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@42:', type='build')
    depends_on('py-setuptools-scm@3.4:+toml', type='build')
    depends_on('py-scikit-build', type='build')
    depends_on('py-cmake@3.11:', type='build')
    depends_on('ninja', type='build')
    depends_on('py-numpy@1.13.3:', type=('build', 'run'))
    depends_on('py-typing', type=('build', 'run'), when='^python@:3.4')
    depends_on('py-typing-extensions', type=('build', 'run'), when='^python@:3.7')
    depends_on('py-dataclasses', type=('build', 'run'), when='^python@:3.6')
    depends_on('py-pydantic@1.7.3:', type=('build', 'run'))
    depends_on('py-rich', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'), when='+convert')
    depends_on('py-uproot@4.0.4:', type=('build', 'run'), when='+convert')
    depends_on('py-requests', type=('build', 'run'), when='+convert')
