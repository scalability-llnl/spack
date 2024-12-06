# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlIpcSystemSimple(PerlPackage):
    """Run commands simply, with detailed diagnostics"""

    homepage = "https://metacpan.org/pod/IPC::System::Simple"
    url = "https://cpan.metacpan.org/authors/id/J/JK/JKEENAN/IPC-System-Simple-1.30.tar.gz"

    maintainers("EbiArnie")

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.30", sha256="22e6f5222b505ee513058fdca35ab7a1eab80539b98e5ca4a923a70a8ae9ba9e")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
