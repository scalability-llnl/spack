# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSubExporterProgressive(PerlPackage):
    """Progressive Sub::Exporter"""

    homepage = "https://metacpan.org/pod/Sub::Exporter::Progressive"
    url = (
        "http://search.cpan.org/CPAN/authors/id/F/FR/FREW/Sub-Exporter-Progressive-0.001013.tar.gz"
    )

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("0.001013", sha256="d535b7954d64da1ac1305b1fadf98202769e3599376854b2ced90c382beac056")
