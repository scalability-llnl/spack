# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPythonUtils(PythonPackage):
    """Python Utils is a collection of small Python functions and classes
    which make common patterns shorter and easier."""

    homepage = "https://github.com/WoLpH/python-utils"
    url      = "https://pypi.io/packages/source/p/python-utils/python-utils-2.4.0.tar.gz"

    version('2.4.0', sha256='f21fc09ff58ea5ebd1fd2e8ef7f63e39d456336900f26bdc9334a03a3f7d8089')
    version('2.3.0', sha256='34aaf26b39b0b86628008f2ae0ac001b30e7986a8d303b61e1357dfcdad4f6d3')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
