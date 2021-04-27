# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Bumpversion(PythonPackage):
    """Version-bump your software with a single command."""

    pypi = "bumpversion/bumpversion-0.5.0.tar.gz"

    version('0.5.3', sha256='6744c873dd7aafc24453d8b6a1a0d6d109faf63cd0cd19cb78fd46e74932c77e')
    version('0.5.0', sha256='030832b9b46848e1c1ac6678dba8242a021e35e908b65565800c9650291117dc')

    depends_on('py-setuptools', type='build')
