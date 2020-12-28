# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMzid(RPackage):
    """An mzIdentML parser for R.

       A parser for mzIdentML files implemented using the XML package. The
       parser tries to be general and able to handle all types of mzIdentML
       files with the drawback of having less 'pretty' output than a vendor
       specific parser. Please contact the maintainer with any problems and
       supply an mzIdentML file so the problems can be fixed quickly."""

    homepage = "https://bioconductor.org/packages/mzID"
    git      = "https://git.bioconductor.org/packages/mzID.git"

    version('1.22.0', commit='382d9cf11f0cba996911a9d79e193d28f3ac6042')
    version('1.20.1', commit='819582646944440ddd9ed3724ae964841573e54c')
    version('1.18.0', commit='7d8924ae95585eb8cf472d21619a7603d291d652')
    version('1.16.0', commit='fc203832a4cbbbe20f6dd826c6bf2128f2c271c4')
    version('1.14.0', commit='1c53aa6523ae61d3ebb13381381fc119d6cc6115')

    depends_on('r-xml', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-iterators', type=('build', 'run'))
    depends_on('r-protgenerics', type=('build', 'run'))
