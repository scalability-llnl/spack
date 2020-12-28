# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyImportlib(PythonPackage):
    """Packaging for importlib from Python 2.7"""

    homepage = "https://github.com/brettcannon/importlib"
    url      = "https://pypi.io/packages/source/i/importlib/importlib-1.0.4.zip"

    version('1.0.4', sha256='b6ee7066fea66e35f8d0acee24d98006de1a0a8a94a8ce6efe73a9a23c8d9826')
