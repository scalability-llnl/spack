# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIntervaltree(PythonPackage):
    """Editable interval tree data structure for Python 2 and 3."""

    homepage = "https://github.com/chaimleib/intervaltree"
    url      = "https://github.com/chaimleib/intervaltree/archive/3.0.2.tar.gz"

    version('3.0.2', sha256='e8ab75b66077f2e5fb85ac56cb6df834689edb048d38601d53d8867cce3b77d1')

    depends_on('py-sortedcontainers@2:2.999', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
