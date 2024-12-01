# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlMoosexEmulateClassAccessorFast(PerlPackage):
    """Emulate Class::Accessor::Fast behavior using Moose attributes"""

    homepage = "https://metacpan.org/pod/MooseX::Emulate::Class::Accessor::Fast"
    url = "https://cpan.metacpan.org/authors/id/H/HA/HAARG/MooseX-Emulate-Class-Accessor-Fast-0.009032.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.009032", sha256="82eeb7ef1f0d25418ae406ea26912b241428d4b2ab9510d5e9deb3f72c187994")

    depends_on("perl-moose@0.84:", type=("build", "run", "test"))
    depends_on("perl-namespace-clean", type=("build", "run", "test"))
    depends_on("perl-test-exception", type=("build", "test"))
