# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlBioDbHts(PerlPackage):
    """Bio::DB::HTS - This is a Perl interface to the HTS Library."""

    homepage = "https://metacpan.org/dist/Bio-DB-HTS"
    url = "https://cpan.metacpan.org/authors/id/A/AV/AVULLO/Bio-DB-HTS-3.01.tar.gz"

    version("3.01", sha256="12a6bc1f579513cac8b9167cce4e363655cc8eba26b7d9fe1170dfe95e044f42")

    depends_on("perl-module-build", type="build")
    depends_on("perl-bioperl")
    depends_on("htslib")
