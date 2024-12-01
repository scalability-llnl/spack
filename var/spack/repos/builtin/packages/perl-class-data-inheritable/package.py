# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlClassDataInheritable(PerlPackage):
    """For creating accessor/mutators to class data."""

    homepage = "https://metacpan.org/pod/Class::Data::Inheritable"
    url = "https://cpan.metacpan.org/authors/id/R/RS/RSHERER/Class-Data-Inheritable-0.09.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.09", sha256="44088d6e90712e187b8a5b050ca5b1c70efe2baa32ae123e9bd8f59f29f06e4d")
    version("0.08", sha256="9967feceea15227e442ec818723163eb6d73b8947e31f16ab806f6e2391af14a")

    def url_for_version(self, version):
        if self.spec.satisfies("@0.09:"):
            return f"https://cpan.metacpan.org/authors/id/R/RS/RSHERER/Class-Data-Inheritable-{version}.tar.gz"
        else:
            return f"https://cpan.metacpan.org/authors/id/T/TM/TMTM/Class-Data-Inheritable-{version}.tar.gz"
