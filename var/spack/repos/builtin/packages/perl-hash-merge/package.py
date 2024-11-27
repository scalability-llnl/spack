# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHashMerge(PerlPackage):
    """Hash::Merge merges two arbitrarily deep hashes into a single hash."""

    homepage = "https://metacpan.org/pod/Hash::Merge"
    url = "https://cpan.metacpan.org/authors/id/R/RE/REHSACK/Hash-Merge-0.300.tar.gz"

    version("0.300", sha256="402fd52191d51415bb7163b7673fb4a108e3156493d7df931b8db4b2af757c40")

    depends_on("perl-scalar-list-utils", type=("build", "run"))
    depends_on("perl-clone-choose", type=("build", "run"))
