# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFilesysNotifySimple(PerlPackage):
    """Simple and dumb file system watcher"""

    homepage = "https://metacpan.org/pod/Filesys::Notify::Simple"
    url = "https://cpan.metacpan.org/authors/id/M/MI/MIYAGAWA/Filesys-Notify-Simple-0.14.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.14", sha256="1fda712d4ba5e1868159ed35f6f8efbfae9d435d6376f5606d533bcb080555a4")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-test-sharedfork", type=("build", "test"))
