# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlHtmlTemplate(PerlPackage):
    """Perl module to use HTML-like templating language"""

    homepage = "https://metacpan.org/pod/HTML::Template"
    url = "https://cpan.metacpan.org/authors/id/S/SA/SAMTREGAR/HTML-Template-2.97.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-1.0-Perl OR GPL-1.0-or-later")

    version("2.97", sha256="6547af61f3aa85793f8616190938d677d7995fb3b720c16258040bc935e2129f")

    depends_on("perl-cgi", type=("build", "run", "test"))
    depends_on("perl-test-pod", type=("build", "link"))
