# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTextGlob(PerlPackage):
    """Text::Glob implements glob(3) style matching that can be used to match
    against text rather than fetching names from a filesystem."""

    homepage = "https://metacpan.org/pod/Text::Glob"
    url = "https://cpan.metacpan.org/authors/id/R/RC/RCLAMP/Text-Glob-0.11.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.11", sha256="069ccd49d3f0a2dedb115f4bdc9fbac07a83592840953d1fcdfc39eb9d305287")

    depends_on("perl-extutils-makemaker", type="build")
