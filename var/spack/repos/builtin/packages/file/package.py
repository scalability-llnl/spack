# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class File(AutotoolsPackage):
    """The file command is "a file type guesser", that is, a command-line
    tool that tells you in words what kind of data a file contains"""

    homepage = "http://www.darwinsys.com/file/"
    url      = "https://astron.com/pub/file/file-5.37.tar.gz"

    version('5.37', sha256='e9c13967f7dd339a3c241b7710ba093560b9a33013491318e88e6b8b57bae07f')
