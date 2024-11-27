# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PerlRoleTiny(PerlPackage):
    """Role::Tiny - Roles: a nouvelle cuisine portion size slice of Moose"""

    homepage = "https://metacpan.org/pod/Role::Tiny"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/Role-Tiny-2.002004.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("2.002004", sha256="d7bdee9e138a4f83aa52d0a981625644bda87ff16642dfa845dcb44d9a242b45")

    depends_on("perl-exporter-tiny", type=("build", "run"))
