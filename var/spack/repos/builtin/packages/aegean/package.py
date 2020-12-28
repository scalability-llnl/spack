# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Aegean(MakefilePackage):
    """The AEGeAn Toolkit is designed for the Analysis and Evaluation of
       Genome Annotations. The toolkit includes a variety of analysis programs
       as well as a C library whose API provides access to AEGeAn's core
       functions and data structures."""

    homepage = "http://brendelgroup.github.io/AEGeAn/"
    url      = "https://github.com/BrendelGroup/AEGeAn/archive/v0.15.2.tar.gz"

    version('0.15.2', sha256='734c9dd23ab3415c3966083bfde5fb72c81e6ace84e08ee3fe0d4c338331d975')

    depends_on('genometools')

    def edit(self, spec, prefix):
        makefile = FileFilter('Makefile')
        if spec.target.family == 'aarch64':
            makefile.filter('-m64', '')

        makefile.filter('/usr/local', prefix)
