# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RRmarkdown(RPackage):
    """Convert R Markdown documents into a variety of formats."""

    homepage = "http://rmarkdown.rstudio.com/"
    url      = "https://cloud.r-project.org/src/contrib/rmarkdown_1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rmarkdown"

    version('1.14', sha256='f636b1048c5be56e06aa0b2b4342ad5c8192734f1e9b27468fef62be672edc61')
    version('1.13', sha256='96fb6b08d27bbb8054145e0a55721f905341941d4f6691480a2a234e2d5a63ef')
    version('1.7', sha256='c3191db65b9ad41b6dbb77aff53487701032d306e92b208ef7515b747931fe63')
    version('1.0', sha256='ff1ecb74ebc444b9b0b7b547adc512daefe1ee08d06bc0e3ee4eb68e58d2ef30')

    depends_on('r@3.0:', type=('build', 'run'))
    depends_on('r-knitr@1.22:', type=('build', 'run'))
    depends_on('r-yaml@2.1.19:', type=('build', 'run'))
    depends_on('r-htmltools@0.3.5:', type=('build', 'run'))
    depends_on('r-evaluate@0.13:', type=('build', 'run'))
    depends_on('r-base64enc', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-rprojroot', when='@1.3:1.7', type=('build', 'run'))
    depends_on('r-mime', when='@1.8:', type=('build', 'run'))
    depends_on('r-stringr@1.2.0:', when='@1.6:', type=('build', 'run'))
    depends_on('r-catools', when='@:1.7', type=('build', 'run'))
    depends_on('r-tinytex@0.11:', when='@1.10:', type=('build', 'run'))
    depends_on('r-xfun', when='@1.13:', type=('build', 'run'))
    depends_on('pandoc@1.12.3:')
