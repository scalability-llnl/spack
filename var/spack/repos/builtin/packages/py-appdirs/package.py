# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAppdirs(PythonPackage):
    """A small Python module for determining appropriate platform-specific
    dirs, e.g. a "user data dir"."""

    homepage = "https://github.com/ActiveState/appdirs"
    url      = "https://pypi.io/packages/source/a/appdirs/appdirs-1.4.3.tar.gz"

    version('1.4.3', sha256='9e5896d1372858f8dd3344faf4e5014d21849c756c8d5701f78f8a103b372d92')
    version('1.4.0', sha256='8fc245efb4387a4e3e0ac8ebcc704582df7d72ff6a42a53f5600bbb18fdaadc5')

    patch('setuptools-import.patch', when='@:1.4.0')
    depends_on('py-setuptools', type='build')
