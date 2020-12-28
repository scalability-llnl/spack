# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFunctools32(PythonPackage):
    """Backport of the functools module from Python 3.2.3 for use on 2.7 and
    PyPy."""

    homepage = "https://github.com/MiCHiLU/python-functools32"
    url      = "https://pypi.io/packages/source/f/functools32/functools32-3.2.3-2.tar.gz"

    version('3.2.3-2', sha256='f6253dfbe0538ad2e387bd8fdfd9293c925d63553f5813c4e587745416501e6d')
