# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyglet(PythonPackage):
    """pyglet is a cross-platform windowing and multimedia library for Python
    for developing games and other visually rich applications.
    """

    homepage = "https://github.com/pyglet/pygle://github.com/pyglet/pyglet"
    url      = "https://pypi.io/packages/source/p/pyglet/pyglet-1.4.2.tar.gz"

    version('1.4.2', sha256='fda25ae5e99057f05bd339ea7972196d2f44e6fe8fb210951ab01f6609cdbdb7')
    version('1.2.1', sha256='d1afb253d6de230e73698377566da333ef42e1c82190216aa7a0c1b729d6ff4d')

    depends_on('py-setuptools', type='build')
    depends_on('py-future', type=('build', 'run'))
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
