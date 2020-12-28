# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySoupsieve(PythonPackage):
    """A modern CSS selector implementation for Beautiful Soup."""

    homepage = "https://github.com/facelessuser/soupsieve"
    url      = "https://pypi.io/packages/source/s/soupsieve/soupsieve-1.9.3.tar.gz"

    version('1.9.3', sha256='8662843366b8d8779dec4e2f921bebec9afd856a5ff2e82cd419acc5054a1a92')

    depends_on('py-setuptools', type='build')
    depends_on('py-backports-functools-lru-cache', when='^python@:2', type=('build', 'run'))
