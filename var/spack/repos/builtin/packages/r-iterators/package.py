# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIterators(RPackage):
    """Support for iterators, which allow a programmer to traverse through all
    the elements of a vector, list, or other collection of data."""

    homepage = "https://cloud.r-project.org/package=iterators"
    url      = "https://cloud.r-project.org/src/contrib/iterators_1.0.8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/iterators"

    version('1.0.12', sha256='96bf31d60ebd23aefae105d9b7790715e63327eec0deb2ddfb3d543994ea9f4b')
    version('1.0.9', sha256='de001e063805fdd124953b571ccb0ed2838c55e40cca2e9d283d8a90b0645e9b')
    version('1.0.8', sha256='ae4ea23385776eb0c06c992a3da6b0256a6c84558c1061034c5a1fbdd43d05b8')

    depends_on('r@2.5.0:', type=('build', 'run'))
