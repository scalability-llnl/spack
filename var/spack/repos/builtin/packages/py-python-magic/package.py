# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyPythonMagic(PythonPackage):
    """A python wrapper for libmagic"""

    homepage = "https://github.com/ahupp/python-magic"
    pypi = "python-magic/python-magic-0.4.15.tar.gz"

    version('0.4.15', sha256='f3765c0f582d2dfc72c15f3b5a82aecfae9498bd29ca840d72f37d7bd38bfcd5')

    depends_on('py-setuptools', type='build')
