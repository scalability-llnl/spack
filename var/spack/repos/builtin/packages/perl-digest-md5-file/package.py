# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDigestMd5File(PerlPackage):
    """Digest::MD5::File - Perl extension for getting MD5 sums for files and urls."""

    homepage = "https://metacpan.org/pod/Digest::MD5::File"
    url = "https://cpan.metacpan.org/authors/id/D/DM/DMUEY/Digest-MD5-File-0.08.tar.gz"

    version("0.08", sha256="adb43a54e32627b4f7e57c9640e6eb06d0bb79d8ea54cd0bd79ed35688fb1218")

    depends_on("perl-extutils-makemaker", type="build")
    depends_on("perl-libwww-perl", type=("build", "run"))
