# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlGraphviz(PerlPackage):
    """Interface to AT&T's GraphViz. Deprecated. See GraphViz2"""

    homepage = "https://metacpan.org/pod/GraphViz"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETJ/GraphViz-2.26.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("2.26", sha256="9a5d2520b3262bf30475272dd764a445f8e7f931bef88be0e3d3bff445da7328")

    depends_on("graphviz", type=("build", "run", "test"))
    depends_on("perl-file-which@1.09:", type=("build", "run", "test"))
    depends_on("perl-ipc-run@0.6:", type=("build", "run", "test"))
    depends_on("perl-libwww-perl", type=("build", "run", "test"))
    depends_on("perl-parse-recdescent@1.965001:", type=("build", "run", "test"))
    depends_on("perl-xml-twig@3.52:", type=("build", "run", "test"))
    depends_on("perl-xml-xpath@1.13:", type=("build", "run", "test"))
