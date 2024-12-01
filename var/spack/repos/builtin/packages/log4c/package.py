# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Log4c(AutotoolsPackage):
    """Library for writing log messages from C programs"""

    homepage = "https://log4c.sourceforge.net/"
    url = "https://downloads.sourceforge.net/project/log4c/log4c/1.2.4/log4c-1.2.4.tar.gz"

    license("LGPL-2.1-or-later")

    version("1.2.4", sha256="5991020192f52cc40fa852fbf6bbf5bd5db5d5d00aa9905c67f6f0eadeed48ea")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("expat@1.95.1:")
