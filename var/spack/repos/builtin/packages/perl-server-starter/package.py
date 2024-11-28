# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlServerStarter(PerlPackage):
    """A superdaemon for hot-deploying server programs"""

    homepage = "https://metacpan.org/pod/Server::Starter"
    url = "https://cpan.metacpan.org/authors/id/K/KA/KAZUHO/Server-Starter-0.35.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.35", sha256="676dc0d6cff4648538332c63c32fb88ad09ed868213ea9e62e3f19fad41b9c40")

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
    depends_on("perl-test-requires", type=("build", "test"))
    depends_on("perl-test-sharedfork", type=("build", "test"))
    depends_on("perl-test-tcp@2.08:", type=("build", "test"))
