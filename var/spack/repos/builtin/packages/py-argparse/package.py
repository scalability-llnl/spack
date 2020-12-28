# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArgparse(PythonPackage):
    """Python command-line parsing library."""

    homepage = "https://github.com/ThomasWaldmann/argparse/"
    url      = "https://pypi.io/packages/source/a/argparse/argparse-1.4.0.tar.gz"

    version('1.4.0', sha256='62b089a55be1d8949cd2bc7e0df0bddb9e028faefc8c32038cc84862aefdd6e4')

    depends_on('py-setuptools', type='build')
