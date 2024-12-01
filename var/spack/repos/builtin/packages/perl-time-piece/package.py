# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTimePiece(PerlPackage):
    """Object Oriented time objects"""

    homepage = "https://metacpan.org/pod/Time::Piece"
    url = "http://search.cpan.org/CPAN/authors/id/E/ES/ESAYM/Time-Piece-1.3203.tar.gz"

    version("1.3401", sha256="4b55b7bb0eab45cf239a54dfead277dfa06121a43e63b3fce0853aecfdb04c27")
    version("1.3203", sha256="6971faf6476e4f715a5b5336f0a97317f36e7880fcca6c4db7c3e38e764a6f41")
