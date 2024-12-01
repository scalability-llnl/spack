# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlTemplateToolkit(PerlPackage):
    """Template - Front-end module to the Template Toolkit."""

    homepage = "https://metacpan.org/pod/Template"
    url = "https://cpan.metacpan.org/authors/id/A/AB/ABW/Template-Toolkit-3.101.tar.gz"

    maintainers("ChristopherChristofi")

    version("3.101", sha256="d2a32dd6c21e4b37c6a93df8087ca9e880cfae613a3e5efaea307b0bdcaedb58")

    depends_on("perl-extutils-makemaker", type=("build"))
    depends_on("perl-appconfig@1.56:")
    depends_on("perl-pathtools@0.8:")
    depends_on("perl-file-temp@0.12:")
    depends_on("perl-test-leaktrace", type=("build", "test"))

    def configure_args(self):
        args = ["TT_QUIET=y", "TT_ACCEPT=y"]
        return args
