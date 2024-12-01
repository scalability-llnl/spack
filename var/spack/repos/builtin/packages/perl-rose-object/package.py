# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlRoseObject(PerlPackage):
    """A simple object base class."""

    homepage = "https://metacpan.org/pod/Rose::Object"
    url = "https://cpan.metacpan.org/authors/id/J/JS/JSIRACUSA/Rose-Object-0.860.tar.gz"

    maintainers("EbiArnie")

    version("0.860", sha256="f3ff294097b1a4b02a4bae6dc3544ded744a08972e831c1d2741083403197f47")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
