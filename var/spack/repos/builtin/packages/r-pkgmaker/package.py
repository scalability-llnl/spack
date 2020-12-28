# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPkgmaker(RPackage):
    """This package provides some low-level utilities to use for package
    development. It currently provides managers for multiple package specific
    options and registries, vignette, unit test and bibtex related utilities.
    It serves as a base package for packages like NMF, RcppOctave, doRNG, and
    as an incubator package for other general purposes utilities, that will
    eventually be packaged separately. It is still under heavy development and
    changes in the interface(s) are more than likely to happen."""

    homepage = "https://renozao.github.io/pkgmaker"
    url      = "https://cloud.r-project.org/src/contrib/pkgmaker_0.27.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pkgmaker"

    version('0.27', sha256='17a289d8f596ba5637b07077b3bff22411a2c2263c0b7de59fe848666555ec6a')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-registry', type=('build', 'run'))
    depends_on('r-codetools', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-stringi', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-xtable', type=('build', 'run'))
    depends_on('r-withr', type=('build', 'run'))
    depends_on('r-bibtex@0.4:', type=('build', 'run'))
