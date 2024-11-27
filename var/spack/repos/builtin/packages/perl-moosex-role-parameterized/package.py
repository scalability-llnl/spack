# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMoosexRoleParameterized(PerlPackage):
    """Moose roles with composition parameters"""

    homepage = "https://metacpan.org/pod/MooseX::Role::Parameterized"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/MooseX-Role-Parameterized-1.11.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("1.11", sha256="1cfe766c5d7f0ecab57f733dcca430a2a2acd6b995757141b940ade3692bec9e")

    depends_on("perl@5.8.1:", type=("build", "link", "run", "test"))
    depends_on("perl-cpan-meta-check@0.011:", type=("build", "test"))
    depends_on("perl-module-build-tiny@0.034:", type=("build"))
    depends_on("perl-module-runtime", type=("build", "run", "test"))
    depends_on("perl-moose@2.0300:", type=("build", "run", "test"))
    depends_on("perl-namespace-autoclean", type=("build", "run", "test"))
    depends_on("perl-namespace-clean@0.19:", type=("build", "run", "test"))
    depends_on("perl-test-fatal", type=("build", "test"))
    depends_on("perl-test-needs", type=("build", "test"))
