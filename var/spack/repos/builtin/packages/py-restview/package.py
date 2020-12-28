# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRestview(PythonPackage):
    """A viewer for ReStructuredText documents that renders them on the fly."""

    homepage = "https://mg.pov.lt/restview/"
    url = "https://pypi.io/packages/source/r/restview/restview-2.6.1.tar.gz"

    version('2.6.1', sha256='14d261ee0edf30e0ebc1eb320428ef4898e97422b00337863556966b851fb5af')

    depends_on('python@2.7:2.8,3.3:3.5')
    depends_on('py-setuptools', type='build')
    depends_on('py-docutils@0.13.1:', type=('build', 'run'))
    depends_on('py-readme-renderer', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
