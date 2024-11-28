# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlLogDispatchFilerotate(PerlPackage):
    """Log to Files that Archive/Rotate Themselves"""

    homepage = "https://metacpan.org/pod/Log::Dispatch::FileRotate"
    url = "https://cpan.metacpan.org/authors/id/M/MS/MSCHOUT/Log-Dispatch-FileRotate-1.38.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.38", sha256="b55d6cede3f0a06426488fbfa554f4561320b014c1023893ced29508e5bce4ec")

    depends_on("perl@5.8.0:", type=("build", "link", "run", "test"))
    depends_on("perl-date-manip", type=("build", "run", "test"))
    depends_on("perl-log-dispatch@2.60:", type=("build", "run", "test"))
    depends_on("perl-sub-uplevel", type=("build", "run", "test"))
    depends_on("perl-path-tiny@0.018:", type=("build", "test"))
    depends_on("perl-test-warn", type=("build", "test"))
