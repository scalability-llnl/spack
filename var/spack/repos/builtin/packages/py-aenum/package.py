# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAenum(PythonPackage):
    """Advanced Enumerations (compatible with Python's stdlib Enum),
    NamedTuples, and NamedConstants."""

    homepage = "https://bitbucket.org/stoneleaf/aenum"
    url      = "https://pypi.io/packages/source/a/aenum/aenum-2.1.2.tar.gz"

    version('2.1.2', sha256='a3208e4b28db3a7b232ff69b934aef2ea1bf27286d9978e1e597d46f490e4687')

    depends_on('py-setuptools', type='build')
