# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlLinguaEnInflect(PerlPackage):
    """Convert singular to plural. Select "a" or "an"."""

    homepage = "https://metacpan.org/pod/Lingua::EN::Inflect"
    url = "https://cpan.metacpan.org/authors/id/D/DC/DCONWAY/Lingua-EN-Inflect-1.905.tar.gz"

    maintainers("EbiArnie")

    version("1.905", sha256="05c29ec3482e572313a60da2181b0b30c5db7cf01f8ae7616ad67e1b66263296")
