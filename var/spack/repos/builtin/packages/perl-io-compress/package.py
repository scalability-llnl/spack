# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlIoCompress(PerlPackage):
    """A perl library for uncompressing gzip, zip, bzip2
    or lzop file/buffer."""

    homepage = "http://search.cpan.org/~pmqs/IO-Compress-2.070/lib/IO/Uncompress/AnyUncompress.pm"
    url      = "http://search.cpan.org/CPAN/authors/id/P/PM/PMQS/IO-Compress-2.081.tar.gz"

    version('2.081', sha256='5211c775544dc8c511af08edfb1c0c22734daa2789149c2a88d68e17b43546d9')

    depends_on('perl-compress-raw-zlib', type='run')
    depends_on('perl-compress-raw-bzip2', type='run')
