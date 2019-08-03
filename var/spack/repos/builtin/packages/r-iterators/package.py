# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RIterators(RPackage):
    """Support for iterators, which allow a programmer to traverse through all
    the elements of a vector, list, or other collection of data."""

    homepage = "https://cloud.r-project.org/web/packages/iterators/index.html"
    url      = "https://cloud.r-project.org/src/contrib/iterators_1.0.8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/iterators"

    version('1.0.9', sha256='de001e063805fdd124953b571ccb0ed2838c55e40cca2e9d283d8a90b0645e9b')
    version('1.0.8', '2ded7f82cddd8174f1ec98607946c6ee')
