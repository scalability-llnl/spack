# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEnum34(PythonPackage):
    """Python 3.4 Enum backported to 3.3, 3.2, 3.1, 2.7, 2.6, 2.5, and 2.4."""

    homepage = "https://bitbucket.org/stoneleaf/enum34/src"
    url      = "https://pypi.io/packages/source/e/enum34/enum34-1.1.6.tar.gz"

    version('1.1.6', sha256='8ad8c4783bf61ded74527bffb48ed9b54166685e4230386a9ed9b1279e2df5b1')

    # enum34 is a backport of the enum library from Python 3.4. It is not
    # intended to be used with Python 3.4+. In fact, it won't build at all
    # for Python 3.6+, as new constructs were added to the builtin enum
    # library that aren't present in enum34. See:
    # https://bitbucket.org/stoneleaf/enum34/issues/19
    depends_on('python@:3.5', type=('build', 'run'))
    depends_on('py-ordereddict', when='^python@:2.6', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
