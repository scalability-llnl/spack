# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPacificaDownloader(PythonPackage):
    """Python Pacifica Download Library"""

    homepage = "https://github.com/pacifica/pacifica-python-downloader/"
    pypi     = "pacifica-downloader/pacifica-downloader-0.4.1.tar.gz"

    version('0.4.1', sha256='11da2032a07ca7bb06fed38dc8d7c4c57267ff98c5fd925271083e18dd85d9f4')

    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-requests', type=('build', 'run'))
