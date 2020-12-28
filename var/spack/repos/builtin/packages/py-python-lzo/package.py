# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonLzo(PythonPackage):
    """This module provides Python bindings for the LZO data compression
    library."""

    homepage = "https://github.com/jd-boyd/python-lzo"
    url      = "https://pypi.io/packages/source/p/python-lzo/python-lzo-1.12.tar.gz"

    version('1.12', sha256='97a8e46825e8f1abd84c2a3372bc09adae9745a5be5d3af2692cd850dac35345')

    depends_on('lzo')
