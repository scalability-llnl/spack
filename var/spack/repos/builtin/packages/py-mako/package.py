# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMako(PythonPackage):
    """A super-fast templating language that borrows the best
       ideas from the existing templating languages."""

    homepage = "https://pypi.python.org/pypi/mako"
    url = "https://pypi.io/packages/source/M/Mako/Mako-1.0.1.tar.gz"

    version('1.0.4', sha256='fed99dbe4d0ddb27a33ee4910d8708aca9ef1fe854e668387a9ab9a90cbf9059')
    version('1.0.1', sha256='45f0869febea59dab7efd256fb451c377cbb7947bef386ff0bb44627c31a8d1c')

    depends_on('py-setuptools', type='build')
    depends_on('py-markupsafe@0.9.2:', type=('build', 'run'))
