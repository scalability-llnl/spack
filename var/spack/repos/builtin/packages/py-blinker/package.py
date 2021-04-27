# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class PyBlinker(PythonPackage):
    """Fast, simple object-to-object and broadcast signaling"""

    homepage = "https://pythonhosted.org/blinker/"
    pypi = "blinker/blinker-1.4.tar.gz"

    version('1.4', sha256='471aee25f3992bd325afa3772f1063dbdbbca947a041b8b89466dc00d606f8b6')

    depends_on('py-setuptools', type='build')
