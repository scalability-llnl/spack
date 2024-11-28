# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlLogDispatch(PerlPackage):
    """Dispatches messages to one or more outputs"""

    homepage = "https://metacpan.org/pod/Log::Dispatch"
    url = "https://cpan.metacpan.org/authors/id/D/DR/DROLSKY/Log-Dispatch-2.71.tar.gz"

    maintainers("EbiArnie")

    license("Artistic-2.0")

    version("2.71", sha256="9d60d9648c35ce2754731eb4deb7f05809ece1bd633b74d74795aed9ec732570")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-devel-globaldestruction", type=("build", "run", "test"))
    depends_on("perl-dist-checkconflicts@0.02:", type=("build", "run", "test"))
    depends_on("perl-ipc-run3", type=("build", "test"))
    depends_on("perl-module-runtime", type=("build", "run", "test"))
    depends_on("perl-namespace-autoclean", type=("build", "run", "test"))
    depends_on("perl-params-validationcompiler", type=("build", "run", "test"))
    depends_on("perl-specio@0.32:", type=("build", "run", "test"))
    depends_on("perl-test-fatal", type=("build", "test"))
    depends_on("perl-test-needs", type=("build", "test"))
    depends_on("perl-try-tiny", type=("build", "run", "test"))
