# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlStatisticsPca(PerlPackage):
    """A simple Perl implementation of Principal Component Analysis."""

    homepage = "https://metacpan.org/pod/Statistics::PCA"
    url = "http://search.cpan.org/CPAN/authors/id/D/DS/DSTH/Statistics-PCA-0.0.1.tar.gz"

    version("0.0.1", sha256="f8adb10b00232123d103a5b49161ad46370f47fe0f752e5462a4dc15f9d46bc4")

    depends_on("perl-module-build", type="build")
    depends_on("perl-contextual-return", type=("build", "run"))
    depends_on("perl-text-simpletable", type=("build", "run"))
    depends_on("perl-math-matrixreal", type=("build", "run"))
