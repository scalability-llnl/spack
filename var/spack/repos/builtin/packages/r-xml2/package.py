# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RXml2(RPackage):
    """Work with XML files using a simple, consistent interface. Built on top
       of the 'libxml2' C library."""

    homepage = "https://cloud.r-project.org/package=xml2"
    url      = "https://cloud.r-project.org/src/contrib/xml2_1.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/xml2"

    version('1.3.2', sha256='df22f9e7e3189d8c9b8804eaf0105324fdac983cffe743552f6d76613600a4cf')
    version('1.2.2', sha256='3050f147c4335be2925a576557bbda36bd52a5bba3110d47b740a2dd811a78f4')
    version('1.2.1', sha256='5615bbc94607efc3bc192551992b349091df802ae34b855cfa817733f2690605')
    version('1.1.1', sha256='00f3e3b66b76760c19da5f6dddc98e6f30de36a96b211e59e1a3f4ff58763116')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.12:', when='@:1.2', type=('build', 'run'))
    depends_on('r-bh', when='@:1.1.1', type=('build', 'run'))
    depends_on('libxml2')
