# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCatalystActionRest(PerlPackage):
    """Automated REST Method Dispatching"""

    homepage = "https://metacpan.org/pod/Catalyst::Action::REST"
    url = "https://cpan.metacpan.org/authors/id/J/JJ/JJNAPIORK/Catalyst-Action-REST-1.21.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.21", sha256="ccf81bba5200d3a0ad6901f923af173a3d4416618aea08a6938baaffdef4cb20")

    depends_on("perl-catalyst-runtime@5.80030:", type=("build", "run", "test"))
    depends_on("perl-class-inspector@1.13:", type=("build", "run", "test"))
    depends_on("perl-json-maybexs", type=("build", "run", "test"))
    depends_on("perl-libwww-perl", type=("build", "test"))
    depends_on("perl-module-pluggable", type=("build", "run", "test"))
    depends_on("perl-moose@1.03:", type=("build", "run", "test"))
    depends_on("perl-mro-compat@0.10:", type=("build", "run", "test"))
    depends_on("perl-namespace-autoclean", type=("build", "run", "test"))
    depends_on("perl-params-validate@0.76:", type=("build", "run", "test"))
    depends_on("perl-test-requires", type=("build", "test"))
    depends_on("perl-uri-find", type=("build", "run", "test"))
