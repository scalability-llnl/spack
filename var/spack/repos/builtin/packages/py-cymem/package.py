# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyCymem(PythonPackage):
    """Manage calls to calloc/free through Cython."""

    homepage = "https://github.com/explosion/cymem"
    url      = "https://pypi.io/packages/source/c/cymem/cymem-2.0.3.tar.gz"

    version('2.0.3', sha256='5083b2ab5fe13ced094a82e0df465e2dbbd9b1c013288888035e24fd6eb4ed01')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel@0.32.0:0.32.999', type='build')
