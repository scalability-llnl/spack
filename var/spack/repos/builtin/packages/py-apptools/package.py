# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyApptools(PythonPackage):
    """The apptools project includes a set of packages that Enthought has found
    useful in creating a number of applications. They implement functionality
    that is commonly needed by many applications."""

    homepage = "https://docs.enthought.com/apptools"
    url      = "https://pypi.io/packages/source/a/apptools/apptools-4.5.0.tar.gz"

    version('4.5.0', sha256='260ae0e2a86cb2df2fede631ab6ac8ece694a58a1def78cd015c890c57140582')

    depends_on('py-setuptools', type='build')
    depends_on('py-configobj', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-traitsui', type=('build', 'run'))
