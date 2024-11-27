# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFilePushd(PerlPackage):
    """Change directory temporarily for a limited scope"""

    homepage = "https://metacpan.org/pod/File::pushd"
    url = "http://search.cpan.org/CPAN/authors/id/D/DA/DAGOLDEN/File-pushd-1.014.tar.gz"

    license("Apache-2.0")

    version("1.016", sha256="d73a7f09442983b098260df3df7a832a5f660773a313ca273fa8b56665f97cdc")
    version("1.014", sha256="b5ab37ffe3acbec53efb7c77b4423a2c79afa30a48298e751b9ebee3fdc6340b")
