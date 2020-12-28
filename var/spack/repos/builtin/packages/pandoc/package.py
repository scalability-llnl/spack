# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


class Pandoc(Package):
    """If you need to convert files from one markup format into another, pandoc
    is your swiss-army knife."""

    homepage = "https://pandoc.org"

    # The following installs the binaries for pandoc and pandoc-citeproc. The
    # reason for installing binaries is that pandoc is a Haskell package and
    # the Haskell framework is not yet in Spack. See #1408 for a discussion of
    # the challenges with Haskell. Until the Haskell framework is in Spack this
    # package will meet the needs of packages that have a dependency on pandoc.

    if platform.system() == "Linux":
        url = "https://github.com/jgm/pandoc/releases/download/2.7.3/pandoc-2.7.3-linux.tar.gz"
        version('2.7.3', sha256='eb775fd42ec50329004d00f0c9b13076e707cdd44745517c8ce2581fb8abdb75')
    elif platform.system() == "Darwin":
        url = "https://github.com/jgm/pandoc/releases/download/2.7.3/pandoc-2.7.3-macOS.zip"
        version('2.7.3', sha256='fb93800c90f3fab05dbd418ee6180d086b619c9179b822ddfecb608874554ff0')

    variant('texlive', default=True, description='Use TeX Live to enable PDF output')

    depends_on('texlive', when='+texlive')

    def install(self, spec, prefix):
        install_tree('.', prefix)
