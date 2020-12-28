# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProgress(RPackage):
    """Configurable Progress bars, they may include percentage, elapsed time,
       and/or the estimated completion time. They work in terminals, in
       'Emacs' 'ESS', 'RStudio', 'Windows' 'Rgui' and the 'macOS' 'R.app'.
       The package also provides a 'C++' 'API', that works with or without
       'Rcpp'."""

    homepage = "https://cloud.r-project.org/package=progress"
    url      = "https://cloud.r-project.org/src/contrib/progress_1.1.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/progress"

    version('1.2.2', sha256='b4a4d8ed55db99394b036a29a0fb20b5dd2a91c211a1d651c52a1023cc58ff35')
    version('1.2.1', sha256='7401e86ff76bef4d26508b74ee8bd169a0377b2738d9ec79ebff0b7fd5c55326')
    version('1.1.2', sha256='a9f4abfd9579b80967cd681041643fe9dfcc4eb3beeba45391bb64e9209baabb')

    depends_on('r-r6', type=('build', 'run'))
    depends_on('r-prettyunits', type=('build', 'run'))
    depends_on('r-hms', when='@1.2.0:', type=('build', 'run'))
    depends_on('r-crayon', when='@1.2.0:', type=('build', 'run'))
