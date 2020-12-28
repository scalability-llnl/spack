# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyToolz(PythonPackage):
    """A set of utility functions for iterators, functions, and dictionaries"""

    homepage = "http://github.com/pytoolz/toolz/"
    url      = "https://pypi.io/packages/source/t/toolz/toolz-0.9.0.tar.gz"

    version('0.9.0', sha256='929f0a7ea7f61c178bd951bdae93920515d3fbdbafc8e6caf82d752b9b3b31c9')

    depends_on('py-setuptools', type='build')
