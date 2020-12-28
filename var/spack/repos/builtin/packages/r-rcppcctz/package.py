# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRcppcctz(RPackage):
    """'Rcpp' Access to the 'CCTZ' timezone library is provided. 'CCTZ' is a
       C++ library for translating between absolute and civil times using the
       rules of a time zone. The 'CCTZ' source code, released under the
       Apache 2.0 License, is included in this package. See
       <https://github.com/google/cctz> for more details."""

    homepage = "https://github.com/eddelbuettel/rcppcctz"
    url      = "https://cloud.r-project.org/src/contrib/RcppCCTZ_0.2.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RcppCCTZ"

    version('0.2.6', sha256='0e9a76055d29da24cd4c4069c78c1f44998f3461be60c7a6c3e7a35059fb79ae')
    version('0.2.4', sha256='98b6867d38abe03957fe803e88b6cc2d122b85a68ef07fa86f7e1009d6c00819')
    version('0.2.3', sha256='0fefcc98387b2c1a5907e5230babb46e2cc11b603424f458f515e445a3236031')

    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
