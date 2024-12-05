# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileRemove(PerlPackage):
    """File::Remove - Remove files and directories"""

    homepage = "https://metacpan.org/pod/File::Remove"
    url = "https://cpan.metacpan.org/authors/id/S/SH/SHLOMIF/File-Remove-1.61.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.61", sha256="fd857f585908fc503461b9e48b3c8594e6535766bc14beb17c90ba58d5dc4975")

    depends_on("perl-module-build", type="build")
