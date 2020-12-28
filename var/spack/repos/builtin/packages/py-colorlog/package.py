# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyColorlog(PythonPackage):
    """A colored formatter for the python logging module"""

    homepage = "https://github.com/borntyping/python-colorlog"
    url      = "https://pypi.io/packages/source/c/colorlog/colorlog-4.0.2.tar.gz"

    version('4.0.2', sha256='3cf31b25cbc8f86ec01fef582ef3b840950dea414084ed19ab922c8b493f9b42')
    version('3.1.4', sha256='418db638c9577f37f0fae4914074f395847a728158a011be2a193ac491b9779d')

    depends_on('py-setuptools', type='build')
