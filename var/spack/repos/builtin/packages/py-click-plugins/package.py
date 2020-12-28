# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyClickPlugins(PythonPackage):
    """An extension module for py-click to register external CLI
       commands via setuptools entry-points."""

    homepage = "https://pypi.org/project/click-plugins/"
    url      = "https://pypi.io/packages/source/c/click-plugins/click-plugins-1.0.4.tar.gz"

    version('1.0.4', sha256='dfed74b5063546a137de99baaaf742b4de4337ad2b3e1df5ec7c8a256adc0847')

    depends_on('py-setuptools', type='build')
    depends_on('py-click@3.0:', type=('build', 'run'))
