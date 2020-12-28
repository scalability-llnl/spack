# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyEcos(PythonPackage):
    """This is the Python package for ECOS: Embedded Cone Solver."""

    homepage = "https://github.com/embotech/ecos"
    url      = "https://www.pypi.io/packages/source/e/ecos/ecos-2.0.7.post1.tar.gz"

    version('2.0.7.post1', sha256='83e90f42b3f32e2a93f255c3cfad2da78dbd859119e93844c45d2fca20bdc758')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy@1.6:', type=('build', 'run'))
    depends_on('py-scipy@0.9:', type=('build', 'run'))
