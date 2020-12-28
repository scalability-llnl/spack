# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWebkitServer(PythonPackage):
    """a Webkit-based, headless web client"""

    homepage = "https://github.com/niklasb/webkit-server"
    url      = "https://pypi.io/packages/source/w/webkit-server/webkit-server-1.0.tar.gz"
    git      = "https://github.com/niklasb/webkit-server.git"

    version('develop', branch='master')
    version('1.0', sha256='836dac18c823bf7737461a2d938c66c7b3601c858897e6c92c7ba0e33574a2bc')
