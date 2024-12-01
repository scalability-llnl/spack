# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlArchiveZip(PerlPackage):
    """Archive::Zip - Provide an interface to ZIP archive files."""

    homepage = "https://metacpan.org/pod/Archive::Zip"
    url = "https://cpan.metacpan.org/authors/id/P/PH/PHRED/Archive-Zip-1.68.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.68", sha256="984e185d785baf6129c6e75f8eb44411745ac00bf6122fb1c8e822a3861ec650")
