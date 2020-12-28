# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RForeach(RPackage):
    """Support for the foreach looping construct. Foreach is an idiom that
    allows for iterating over elements in a collection, without the use of an
    explicit loop counter. This package in particular is intended to be used
    for its return value, rather than for its side effects. In that sense, it
    is similar to the standard lapply function, but doesn't require the
    evaluation of a function. Using foreach without side effects also
    facilitates executing the loop in parallel."""

    homepage = "https://cloud.r-project.org/package=foreach"
    url      = "https://cloud.r-project.org/src/contrib/foreach_1.4.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/foreach"

    version('1.4.7', sha256='95632c0b1182fc01490718d82fa3b2bce864f2a011ae53282431c7c2a3f5f160')
    version('1.4.3', sha256='1ef03f770f726a62e3753f2402eb26b226245958fa99d570d003fc9e47d35881')

    depends_on('r@2.5.0:', type=('build', 'run'))
    depends_on('r-codetools', type=('build', 'run'))
    depends_on('r-iterators', type=('build', 'run'))
