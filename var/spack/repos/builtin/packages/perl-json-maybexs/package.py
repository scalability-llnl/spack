# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PerlJsonMaybexs(PerlPackage):
    """Use Cpanel::JSON::XS with a fallback to JSON::XS and JSON::PP"""

    homepage = "https://metacpan.org/pod/JSON::MaybeXS"
    url = "https://cpan.metacpan.org/authors/id/E/ET/ETHER/JSON-MaybeXS-1.004005.tar.gz"

    maintainers("EbiArnie")

    version("1.004005", sha256="f5b6bc19f579e66b7299f8748b8ac3e171936dc4e7fcb72a8a257a9bd482a331")

    depends_on("perl@5.6.0:", type=("build", "link", "run", "test"))
    depends_on("perl-cpanel-json-xs@2.3310:", type=("build", "run", "test"))
    depends_on("perl-test-needs@0.002006:", type=("build", "test"))
