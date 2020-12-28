# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttptools(PythonPackage):
    """httptools is a Python binding for the nodejs HTTP parser."""

    homepage = "https://github.com/MagicStack/httptools"
    url      = "https://pypi.io/packages/source/h/httptools/httptools-0.1.1.tar.gz"

    version('0.1.1', sha256='41b573cf33f64a8f8f3400d0a7faf48e1888582b6f6e02b82b9bd4f0bf7497ce')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
