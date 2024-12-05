# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCatalystComponentInstancepercontext(PerlPackage):
    """Moose role to create only one instance of component per context"""

    homepage = "https://metacpan.org/pod/Catalyst::Component::InstancePerContext"
    url = "https://cpan.metacpan.org/authors/id/G/GR/GRODITI/Catalyst-Component-InstancePerContext-0.001001.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.001001", sha256="7f63f930e1e613f15955c9e6d73873675c50c0a3bc2a61a034733361ed26d271")

    depends_on("perl-catalyst-runtime", type=("build", "run", "test"))
    depends_on("perl-moose", type=("build", "run", "test"))
