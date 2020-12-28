# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPil(PythonPackage):
    """The Python Imaging Library (PIL) adds image processing capabilities
    to your Python interpreter. This library supports many file formats,
    and provides powerful image processing and graphics capabilities."""

    homepage = "http://www.pythonware.com/products/pil/"
    url      = "http://effbot.org/media/downloads/Imaging-1.1.7.tar.gz"

    version('1.1.7', sha256='895bc7c2498c8e1f9b99938f1a40dc86b3f149741f105cf7c7bd2e0725405211')

    provides('pil')
    provides('pil@1.1.7', when='@1.1.7')

    # py-pil currently only works with Python2.
    # If you are using Python 3, try using py-pillow instead.
    depends_on('python@1.5.2:2.8', type=('build', 'run'))
