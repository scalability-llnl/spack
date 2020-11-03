# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyYapf(PythonPackage):
    """ Yet Another Python Formatter """
    homepage = "https://github.com/google/yapf"
    # base https://pypi.python.org/pypi/cffi
    url      = "https://github.com/google/yapf/archive/v0.2.1.tar.gz"

    version('0.30.0', sha256='9f561af26f8d27c3a334d3d2ee8947b8826a86691087e447ce483512d834682c')
    version('0.2.1', sha256='13158055acd8e3c2f3a577528051a1c5057237f699150211a86fb405c4ea3936')

    depends_on('py-setuptools', type='build')
