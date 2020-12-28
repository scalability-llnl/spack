# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RJanitor(RPackage):
    """The main janitor functions can: perfectly format data.frame column
       names; provide quick one- and two-variable tabulations (i.e., frequency
       tables and crosstabs); and isolate duplicate records. Other janitor
       functions nicely format the tabulation results. These
       tabulate-and-report functions approximate popular features of SPSS and
       Microsoft Excel. This package follows the principles of the "tidyverse"
       and works well with the pipe function %>%. janitor was built with
       beginning-to-intermediate R users in mind and is optimized for
       user-friendliness. Advanced R users can already do everything covered
       here, but with janitor they can do it faster and save their thinking
       for the fun stuff."""

    homepage = "https://github.com/sfirke/janitor"
    url      = "https://cloud.r-project.org/src/contrib/janitor_0.3.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/janitor"

    version('1.2.0', sha256='5e15a2292c65c5ddd6160289dec2604b05a813651a2be0d7854ace4548a32b8c')
    version('1.1.1', sha256='404b41f56e571fab4c95ef62e79cb4f3bb34d5bb6e4ea737e748ff269536176b')
    version('0.3.0', sha256='5e4d8ef895ed9c7b8fa91aeb93e25c009366b4c5faaf3d02265f64b33d4a45f4')

    depends_on('r@3.1.2:', type=('build', 'run'))
    depends_on('r-dplyr@0.7.0:', type=('build', 'run'))
    depends_on('r-tidyr@0.7.0:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-snakecase@0.9.2:', when='@1.1.0:', type=('build', 'run'))
    depends_on('r-purrr', when='@1.1.0:', type=('build', 'run'))
    depends_on('r-rlang', when='@1.1.0:', type=('build', 'run'))
