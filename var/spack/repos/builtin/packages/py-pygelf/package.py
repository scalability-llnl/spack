# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygelf(PythonPackage):
    """Python logging handlers with GELF (Graylog Extended Log Format)
    support."""

    homepage = "https://github.com/keeprocking/pygelf"
    url      = "https://pypi.io/packages/source/p/pygelf/pygelf-0.3.6.tar.gz"

    # notify when the package is updated.
    maintainers = ['victorusu', 'vkarak']

    version('0.3.6', sha256='3e5bc59e3b5a754556a76ff2c69fcf2003218ad7b5ff8417482fa1f6a7eba5f9')

    depends_on('python', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
