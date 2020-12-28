# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJson5(PythonPackage):
    """The JSON5 Data Interchange Format (JSON5) is a superset of JSON that aims
       to alleviate some of the limitations of JSON by expanding its syntax to
       include some productions from ECMAScript 5.1."""

    homepage = "https://github.com/dpranke/pyjson5"
    url      = "https://pypi.io/packages/source/j/json5/json5-0.9.4.tar.gz"

    version('0.9.4', sha256='2ebfad1cd502dca6aecab5b5c36a21c732c3461ddbc412fb0e9a52b07ddfe586')

    depends_on('py-setuptools', type=('build', 'run'))
