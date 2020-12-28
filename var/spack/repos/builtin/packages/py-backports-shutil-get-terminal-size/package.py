# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBackportsShutilGetTerminalSize(PythonPackage):
    """A backport of the get_terminal_size function
    from Python 3.3's shutil."""

    homepage = "https://pypi.python.org/pypi/backports.shutil_get_terminal_size"
    url      = "https://pypi.io/packages/source/b/backports.shutil_get_terminal_size/backports.shutil_get_terminal_size-1.0.0.tar.gz"

    py_namespace = 'backports'

    version('1.0.0', sha256='713e7a8228ae80341c70586d1cc0a8caa5207346927e23d09dcbcaf18eadec80')

    # newer setuptools version mess with "namespace" packages in an
    # incompatible way cf. https://github.com/pypa/setuptools/issues/900
    depends_on('py-setuptools@:30.999.999,41:', type='build')
    depends_on('python@:3.2')
