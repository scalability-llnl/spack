# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySingledispatch(PythonPackage):
    """This library brings functools.singledispatch to Python 2.6-3.3."""

    homepage = "https://pypi.python.org/pypi/singledispatch"
    url      = "https://pypi.io/packages/source/s/singledispatch/singledispatch-3.4.0.3.tar.gz"

    version('3.4.0.3', sha256='5b06af87df13818d14f08a028e42f566640aef80805c3b50c5056b086e3c2b9c')

    depends_on('py-setuptools', type='build')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-ordereddict', when="^python@:2.6", type=('build', 'run'))
