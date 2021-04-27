# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRdpack(RPackage):
    """Update and Manipulate Rd Documentation Objects

    Functions for manipulation of R documentation objects, including
    functions reprompt() and ereprompt() for updating 'Rd' documentation for
    functions, methods and classes; 'Rd' macros for citations and import of
    references from 'bibtex' files for use in 'Rd' files and 'roxygen2'
    comments; 'Rd' macros for evaluating and inserting snippets of 'R' code and
    the results of its evaluation or creating graphics on the fly; and many
    functions for manipulation of references and Rd files."""

    homepage = "https://github.com/GeoBosh/Rdpack"
    url      = "https://cloud.r-project.org/src/contrib/Rdpack_0.11-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Rdpack"

    version('2.1', sha256='26e094fe3c077fb2a99e95c5bd94015a5f993a4a5f5d217829b4872ff004bfce')
    version('0.11-0', sha256='8fb449c80fbe931cdce51f728fb03a1978009ccce66fd6b9edacdc6ff4118d85')

    depends_on('r@2.15.0:', type=('build', 'run'))
    depends_on('r-gbrd', type=('build', 'run'))
    depends_on('r-rbibutils@1.3:', when='@2.1:', type=('build', 'run'))
    depends_on('r-bibtex@0.4.0:', when='@:0.11-0', type=('build', 'run'))
