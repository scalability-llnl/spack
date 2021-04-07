# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGast(PythonPackage):
    """Python AST that abstracts the underlying Python version"""

    homepage = "https://github.com/serge-sans-paille/gast"
    pypi = "gast/gast-0.3.2.tar.gz"

    version('0.4.0', sha256='40feb7b8b8434785585ab224d1568b857edb18297e5a3047f1ba012bc83b42c1')
    version('0.3.3', sha256='b881ef288a49aa81440d2c5eb8aeefd4c2bb8993d5f50edae7413a85bfdb3b57')
    version('0.3.2', sha256='5c7617f1f6c8b8b426819642b16b9016727ddaecd16af9a07753e537eba8a3a5')
    version('0.2.2', sha256='fe939df4583692f0512161ec1c880e0a10e71e6a232da045ab8edd3756fbadf0')
    version('0.2.0', sha256='7068908321ecd2774f145193c4b34a11305bd104b4551b09273dfd1d6a374930')

    depends_on('py-setuptools', type='build')
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
