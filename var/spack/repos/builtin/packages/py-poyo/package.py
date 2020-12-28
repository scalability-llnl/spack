# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPoyo(PythonPackage):
    """A lightweight YAML Parser for Python"""

    homepage = "https://github.com/hackebrot/poyo"
    url      = "https://github.com/hackebrot/poyo/archive/0.4.1.tar.gz"

    version('0.4.1', sha256='9f069dc9c8ee359abc8ef9e7304cb1b1c23556d1f4ae64f4247c1e45de43c1f1')

    depends_on('py-setuptools', type='build')
