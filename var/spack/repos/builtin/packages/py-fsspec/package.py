# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFsspec(PythonPackage):
    """A specification for pythonic filesystems."""

    homepage = "https://github.com/intake/filesystem_spec"
    pypi = "fsspec/fsspec-0.4.4.tar.gz"

    version('0.8.0', sha256='176f3fc405471af0f1f1e14cffa3d53ab8906577973d068b976114433c010d9d')
    version('0.7.3', sha256='1b540552c93b47e83c568e87507d6e02993e6d1b30bc7285f2336c81c5014103')
    version('0.4.4', sha256='97697a46e8bf8be34461c2520d6fc4bfca0ed749b22bb2b7c21939fd450a7d63')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('python@3.6:', type=('build', 'run'), when='@0.6.3:')
    depends_on('py-setuptools', type='build')
