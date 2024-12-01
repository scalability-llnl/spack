# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlCatalystPluginStaticSimple(PerlPackage):
    """Make serving static pages painless."""

    homepage = "https://metacpan.org/pod/Catalyst::Plugin::Static::Simple"
    url = "https://cpan.metacpan.org/authors/id/I/IL/ILMARI/Catalyst-Plugin-Static-Simple-0.37.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("0.37", sha256="5a4d85a3588cd4e83f1b002581412e7d71b7d57f66056e5d87a36f93d89c9e7c")

    depends_on("perl-catalyst-runtime@5.80008:", type=("build", "run", "test"))
    depends_on("perl-mime-types@2.03:", type=("build", "run", "test"))
    depends_on("perl-moose", type=("build", "run", "test"))
    depends_on("perl-namespace-autoclean", type=("build", "run", "test"))
