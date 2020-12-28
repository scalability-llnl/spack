# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBabel(PythonPackage):
    """Babel is an integrated collection of utilities that assist in
    internationalizing and localizing Python applications, with an
    emphasis on web-based applications."""

    homepage = "http://babel.pocoo.org/en/latest/"
    url      = "https://pypi.io/packages/source/B/Babel/Babel-2.7.0.tar.gz"

    version('2.7.0', sha256='e86135ae101e31e2c8ec20a4e0c5220f4eed12487d5cf3f78be7e98d3a57fc28')
    version('2.6.0', sha256='8cba50f48c529ca3fa18cf81fa9403be176d374ac4d60738b839122dfaaa3d23')
    version('2.4.0', sha256='8c98f5e5f8f5f088571f2c6bd88d530e331cbbcb95a7311a0db69d3dca7ec563')
    version('2.3.4', sha256='c535c4403802f6eb38173cd4863e419e2274921a01a8aad8a5b497c131c62875')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-pytz@2015.7:', type=('build', 'run'))
