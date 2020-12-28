# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileHomedir(PerlPackage):
    """Find your home and other directories on any platform"""

    homepage = "https://metacpan.org/pod/File::HomeDir"
    url      = "https://cpan.metacpan.org/authors/id/R/RE/REHSACK/File-HomeDir-1.004.tar.gz"

    version('1.004', sha256='45f67e2bb5e60a7970d080e8f02079732e5a8dfc0c7c3cbdb29abfb3f9f791ad')

    depends_on('perl-file-which', type=('build', 'run'))
