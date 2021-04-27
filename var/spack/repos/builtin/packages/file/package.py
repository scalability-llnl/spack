# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class File(AutotoolsPackage):
    """The file command is "a file type guesser", that is, a command-line
    tool that tells you in words what kind of data a file contains"""

    homepage = "http://www.darwinsys.com/file/"
    url      = "https://astron.com/pub/file/file-5.37.tar.gz"

    version('5.40', sha256='167321f43c148a553f68a0ea7f579821ef3b11c27b8cbe158e4df897e4a5dd57')
    version('5.39', sha256='f05d286a76d9556243d0cb05814929c2ecf3a5ba07963f8f70bfaaa70517fad1')
    version('5.38', sha256='593c2ffc2ab349c5aea0f55fedfe4d681737b6b62376a9b3ad1e77b2cc19fa34')
    version('5.37', sha256='e9c13967f7dd339a3c241b7710ba093560b9a33013491318e88e6b8b57bae07f')
