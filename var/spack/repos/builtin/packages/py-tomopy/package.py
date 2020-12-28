# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTomopy(PythonPackage):
    """TomoPy is an open-source Python package for tomographic data
       processing and image reconstruction."""

    homepage = "http://tomopy.readthedocs.io/en/latest/index.html"
    url      = "https://github.com/tomopy/tomopy/archive/1.0.0.tar.gz"

    version('1.0.0', sha256='ee45f7a062e5a66d6f18a904d2e204e48d85a1ce1464156f9e2f6353057dfe4c')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-h5py', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-scikit-image', type=('build', 'run'))
    depends_on('py-pywavelets', type=('build', 'run'))
    depends_on('py-pyfftw', type=('build', 'run'))
    depends_on('py-dxchange', type=('build', 'run'))
