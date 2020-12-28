# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMpld3(PythonPackage):
    """An interactive D3js-based viewer which brings matplotlib graphics
    to the browser."""

    homepage = "http://mpld3.github.com/"
    url      = "https://pypi.io/packages/source/m/mpld3/mpld3-0.3.tar.gz"

    version('0.3', sha256='4d455884a211bf99b37ecc760759435c7bb6a5955de47d8daf4967e301878ab7')

    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-matplotlib@1.3:', type=('build', 'run'))
    depends_on('py-jinja2@2.7:', type=('build', 'run'))
