# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlYamlLibyaml(PerlPackage):
    """Perl YAML Serialization using XS and libyaml"""

    homepage = "https://metacpan.org/pod/YAML::LibYAML"
    url = "http://search.cpan.org/CPAN/authors/id/T/TI/TINITA/YAML-LibYAML-0.67.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.89", sha256="155ab83675345c50add03311acf9dd915955707f909a2abd8b17d7792859b2ec")
    version("0.84", sha256="225bcb39be2d5e3d02df7888d5f99fd8712f048ba539b09232ca1481e70bfd05")
    version("0.67", sha256="e65a22abc912a46a10abddf3b88d806757f44f164ab3167c8f0ff6aa30648187")

    depends_on("c", type="build")  # generated
