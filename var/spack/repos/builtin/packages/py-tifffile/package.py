# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTifffile(PythonPackage):
    """Read and write image data from and to TIFF files."""

    homepage = "https://github.com/blink1073/tifffile"
    url      = "https://pypi.io/packages/source/t/tifffile/tifffile-0.12.1.tar.gz"

    version('2020.10.1', sha256='799feeccc91965b69e1288c51a1d1118faec7f40b2eb89ad2979591b85324830')
    version('0.12.1', sha256='802367effe86b0d1e64cb5c2ed886771f677fa63260b945e51a27acccdc08fa1')

    depends_on('python@3.7:', type=('build', 'run'), when='@2020.10.1:')
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.8.2:', type=('build', 'run'))
    depends_on('py-numpy@1.15.1:', type=('build', 'run'), when='@2020.10.1:')
