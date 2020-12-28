# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTriebeard(RPackage):
    """triebeard: 'Radix' Trees in 'Rcpp'"""

    homepage = "https://github.com/Ironholds/triebeard/"
    url      = "https://cloud.r-project.org/src/contrib/triebeard_0.3.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/triebeard"

    version('0.3.0', sha256='bf1dd6209cea1aab24e21a85375ca473ad11c2eff400d65c6202c0fb4ef91ec3')

    depends_on('r-rcpp', type=('build', 'run'))
