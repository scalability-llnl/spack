# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlFileFindRule(PerlPackage):
    """File::Find::Rule is a friendlier interface to File::Find. It allows you to
    build rules which specify the desired files and directories."""

    homepage = "https://metacpan.org/pod/File::Find::Rule"
    url = "https://cpan.metacpan.org/authors/id/R/RC/RCLAMP/File-Find-Rule-0.34.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.34", sha256="7e6f16cc33eb1f29ff25bee51d513f4b8a84947bbfa18edb2d3cc40a2d64cafe")

    depends_on("perl-extutils-makemaker", type="build")
    depends_on("perl-number-compare", type=("build", "run"))
    depends_on("perl-text-glob", type=("build", "run"))
