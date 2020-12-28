# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTidyverse(RPackage):
    """The 'tidyverse' is a set of packages that work in harmony because they
       share common data representations and 'API' design. This package is
       designed to make it easy to install and load multiple 'tidyverse'
       packages in a single step."""

    homepage = "http://tidyverse.tidyverse.org/"
    url      = "https://cloud.r-project.org/src/contrib/tidyverse_1.2.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tidyverse"

    version('1.2.1', sha256='ad67a27bb4e89417a15338fe1a40251a7b5dedba60e9b72637963d3de574c37b')

    depends_on('r-broom@0.4.2:', type=('build', 'run'))
    depends_on('r-cli@1.0.0:', type=('build', 'run'))
    depends_on('r-crayon@1.3.4:', type=('build', 'run'))
    depends_on('r-dplyr@0.7.4:', type=('build', 'run'))
    depends_on('r-dbplyr@1.1.0:', type=('build', 'run'))
    depends_on('r-forcats@0.2.0:', type=('build', 'run'))
    depends_on('r-ggplot2@2.2.1:', type=('build', 'run'))
    depends_on('r-haven@1.1.0:', type=('build', 'run'))
    depends_on('r-hms@0.3:', type=('build', 'run'))
    depends_on('r-httr@1.3.1:', type=('build', 'run'))
    depends_on('r-jsonlite@1.5:', type=('build', 'run'))
    depends_on('r-lubridate@1.7.1:', type=('build', 'run'))
    depends_on('r-magrittr@1.5:', type=('build', 'run'))
    depends_on('r-modelr@0.1.1:', type=('build', 'run'))
    depends_on('r-purrr@0.2.4:', type=('build', 'run'))
    depends_on('r-readr@1.1.1:', type=('build', 'run'))
    depends_on('r-readxl@1.0.0:', type=('build', 'run'))
    depends_on('r-reprex@0.1.1:', type=('build', 'run'))
    depends_on('r-rlang@0.1.4:', type=('build', 'run'))
    depends_on('r-rstudioapi@0.7:', type=('build', 'run'))
    depends_on('r-rvest@0.3.2:', type=('build', 'run'))
    depends_on('r-stringr@1.2.0:', type=('build', 'run'))
    depends_on('r-tibble@1.3.4:', type=('build', 'run'))
    depends_on('r-tidyr@0.7.2:', type=('build', 'run'))
    depends_on('r-xml2@1.1.1:', type=('build', 'run'))
