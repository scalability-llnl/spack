# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBmtk(PythonPackage):
    """The Brain Modeling Toolkit"""

    homepage = "https://github.com/AllenInstitute/bmtk"
    pypi = "bmtk/bmtk-1.0.5.tar.gz"

    version('1.0.5', sha256='e0cb47b334467a6d124cfb99bbc67cc88f39f0291f4c39929f50d153130642a4')

    depends_on('py-setuptools', type='build')

    depends_on('py-jsonschema',   type=('run'))
    depends_on('py-pandas',       type=('run'))
    depends_on('py-numpy',        type=('run'))
    depends_on('py-six',          type=('run'))
    depends_on('py-h5py',         type=('run'))
    depends_on('py-matplotlib',   type=('run'))
    depends_on('py-scipy',        type=('run'))
    depends_on('py-scikit-image', type=('run'))
    depends_on('py-sympy',        type=('run'))
