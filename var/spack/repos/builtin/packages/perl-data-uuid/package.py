# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlDataUuid(PerlPackage):
    """Globally/Universally Unique Identifiers (GUIDs/UUIDs)"""

    homepage = "https://metacpan.org/pod/Data::UUID"
    url = "https://cpan.metacpan.org/authors/id/R/RJ/RJBS/Data-UUID-1.226.tar.gz"

    maintainers("EbiArnie")

    license("BSD")

    version("1.226", sha256="093d57ffa0d411a94bafafae495697db26f5c9d0277198fe3f7cf2be22996453")
