# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPathtools(PerlPackage):
    """File::Spec - portably perform operations on file names."""

    homepage = "https://metacpan.org/pod/File::Spec"
    url = "https://cpan.metacpan.org/authors/id/X/XS/XSAWYERX/PathTools-3.75.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("3.75", sha256="a558503aa6b1f8c727c0073339081a77888606aa701ada1ad62dd9d8c3f945a2")
