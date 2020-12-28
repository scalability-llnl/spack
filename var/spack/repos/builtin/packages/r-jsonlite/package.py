# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RJsonlite(RPackage):
    """A fast JSON parser and generator optimized for statistical data and the
    web. Started out as a fork of 'RJSONIO', but has been completely rewritten
    in recent versions. The package offers flexible, robust, high performance
    tools for working with JSON in R and is particularly powerful for building
    pipelines and interacting with a web API. The implementation is based on
    the mapping described in the vignette (Ooms, 2014). In addition to
    converting JSON data from/to R objects, 'jsonlite' contains functions to
    stream, validate, and prettify JSON data. The unit tests included with the
    package verify that all edge cases are encoded and decoded consistently for
    use with dynamic data in systems and applications."""

    homepage = "https://github.com/jeroenooms/jsonlite"
    url      = "https://cloud.r-project.org/src/contrib/jsonlite_1.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/jsonlite"

    version('1.6.1', sha256='74921dd249857a23afabc1ad1485a63a48828e57f240f0619deb04c60f883377')
    version('1.6', sha256='88c5b425229966b7409145a6cabc72db9ed04f8c37ee95901af0146bb285db53')
    version('1.5', sha256='6490371082a387cb1834048ad8cdecacb8b6b6643751b50298c741490c798e02')
    version('1.2', sha256='cb6b4660468d2db84ed09c7b8fefd169fcfc13e1e6b4e7ce64dce2713f34264d')
    version('1.0', sha256='d756dd6367e3fc515c855bb0b34a3a81955f8aeb494db029a893f3cdfcff962d')
    version('0.9.21', sha256='079349342ea6eb92bd5fa8f6a7c08d9e3652c3d41010b64afbc3297671eb3791')
