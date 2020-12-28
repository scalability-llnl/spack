# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMunch(PythonPackage):
    """A Munch is a Python dictionary that provides attribute-style
       access (a la JavaScript objects). """

    homepage = "https://github.com/Infinidat/munch"
    url      = "https://github.com/Infinidat/munch/archive/2.2.0.tar.gz"

    version('2.2.0', sha256='f354ea638e5e582c52d3e47eb54199d3eade94ee3552d64453ddfcbe953973f0')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
