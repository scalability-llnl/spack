# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlSoapLite(PerlPackage):
    """Perl's Web Services Toolkit"""

    homepage = "https://metacpan.org/pod/SOAP::Lite"
    url = "http://search.cpan.org/CPAN/authors/id/P/PH/PHRED/SOAP-Lite-1.22.tar.gz"

    license("GPL-1.0-or-later OR Artistic-1.0-Perl")

    version("1.22", sha256="92f492f8722cb3002cd1dce11238cee5599bb5bd451a062966df45223d33693a")

    depends_on("perl-io-sessiondata", type=("build", "run"))
    depends_on("perl-lwp-protocol-https", type=("build", "run"))
    depends_on("perl-task-weaken", type=("build", "run"))
    depends_on("perl-xml-parser-lite", type=("build", "run"))
    depends_on("perl-xml-parser", type=("build", "run"))
    depends_on("perl-test-warn", type=("build", "run"))
    depends_on("perl-class-inspector", type=("build", "run"))
