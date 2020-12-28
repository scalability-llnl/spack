# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTestpath(PythonPackage):
    """Testpath is a collection of utilities for Python code working with
    files and commands."""

    homepage = "https://github.com/jupyter/testpath"
    url      = "https://pypi.io/packages/source/t/testpath/testpath-0.4.2.tar.gz"

    version('0.4.2', sha256='b694b3d9288dbd81685c5d2e7140b81365d46c29f5db4bc659de5aa6b98780f8')
