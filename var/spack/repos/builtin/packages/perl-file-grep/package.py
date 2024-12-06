# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileGrep(PerlPackage):
    """File::Grep - Find matches to a pattern in a series of files and related functions"""

    homepage = "https://metacpan.org/pod/File::Grep"
    url = "https://cpan.metacpan.org/authors/id/M/MN/MNEYLON/File-Grep-0.02.tar.gz"

    version("0.02", sha256="462e15274eb6278521407ea302d9eea7252cd44cab2382871f7de833d5f85632")

    depends_on("perl-extutils-makemaker", type="build")
