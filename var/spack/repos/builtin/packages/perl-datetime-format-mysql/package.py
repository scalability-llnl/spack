# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDatetimeFormatMysql(PerlPackage):
    """Parse and format MySQL dates and times"""

    homepage = "https://metacpan.org/pod/DateTime::Format::MySQL"
    url = "https://cpan.metacpan.org/authors/id/X/XM/XMIKEW/DateTime-Format-MySQL-0.08.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.08", sha256="19cb70e98584655e354d2d6a8e71cc5ca902dddc3ac44416712f9163d122b9e8")

    depends_on("perl-datetime", type=("build", "run", "test"))
    depends_on("perl-datetime-format-builder@0.6:", type=("build", "run", "test"))
