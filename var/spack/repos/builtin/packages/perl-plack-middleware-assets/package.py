# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlPlackMiddlewareAssets(PerlPackage):
    """Concatenate and minify JavaScript and CSS files"""

    homepage = "https://metacpan.org/pod/Plack::Middleware::Assets"
    url = "https://cpan.metacpan.org/authors/id/P/PE/PERLER/Plack-Middleware-Assets-1.0.0.tar.gz"

    maintainers("EbiArnie")

    license("BSD")

    version("1.0.0", sha256="fb43c9fb7e395efcb75baeed9dc1a4546d6d7ad387761238b0568673ace0ce84")

    depends_on("perl-css-minifier-xs", type=("build", "run", "test"))
    depends_on("perl-http-date", type=("build", "run", "test"))
    depends_on("perl-javascript-minifier-xs", type=("build", "run", "test"))
    depends_on("perl-plack", type=("build", "run", "test"))
