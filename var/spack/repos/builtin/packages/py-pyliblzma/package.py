# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyliblzma(PythonPackage):
    """Python bindings for liblzma"""

    homepage = "https://launchpad.net/pyliblzma"
    url      = "https://pypi.io/packages/source/p/pyliblzma/pyliblzma-0.5.3.tar.bz2"

    version('0.5.3', sha256='08d762f36d5e59fb9bb0e22e000c300b21f97e35b713321ee504cfb442667957')

    depends_on('py-setuptools', type='build')
    depends_on('lzma')
