# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCloneChoose(PerlPackage):
    """Checks several different modules which provides a clone() function
    and selects an appropriate one."""

    homepage = "https://metacpan.org/pod/Clone::Choose"
    url = "https://cpan.metacpan.org/authors/id/H/HE/HERMES/Clone-Choose-0.010.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.010", sha256="5623481f58cee8edb96cd202aad0df5622d427e5f748b253851dfd62e5123632")
