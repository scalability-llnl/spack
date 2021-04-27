# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PySymfit(PythonPackage):
    """Symbolic Fitting; fitting as it should be."""

    homepage = "http://symfit.readthedocs.org"
    pypi = "symfit/symfit-0.3.5.tar.gz"

    version('0.3.5', sha256='24c66305895c590249da7e61f62f128ee1c0c43c0a8c8e33b8abd3e0931f0881')

    depends_on('py-setuptools@17.1:', type='build')
    depends_on('py-pbr@1.9:',         type='build')
    depends_on('py-numpy',            type='run')
    depends_on('py-scipy',            type='run')
    depends_on('py-sympy',            type='run')
    depends_on('py-funcsigs',         type='run', when='^python@:2.8')
