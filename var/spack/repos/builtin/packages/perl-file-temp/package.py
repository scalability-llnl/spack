# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileTemp(PerlPackage):
    """File::Temp - return name and handle of a temporary file safely."""

    homepage = "https://metacpan.org/pod/File::Temp"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/File-Temp-0.2311.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.2311", sha256="2290d61bf5c39882fc3311da9ce1c7f42dbdf825ae169e552c59fe4598b36f4a")
