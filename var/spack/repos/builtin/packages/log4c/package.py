# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Log4c(AutotoolsPackage):
    """Library for writing log messages from C programs"""

    homepage = "http://log4c.sourceforge.net/"
    url      = "https://downloads.sourceforge.net/project/log4c/log4c/1.2.4/log4c-1.2.4.tar.gz"

    version('1.2.4', sha256='5991020192f52cc40fa852fbf6bbf5bd5db5d5d00aa9905c67f6f0eadeed48ea')

    depends_on('expat@1.95.1:')
