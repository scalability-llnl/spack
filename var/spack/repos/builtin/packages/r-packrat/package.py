# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPackrat(RPackage):
    """Manage the R packages your project depends on in an isolated, portable,
    and reproducible way."""

    homepage = "https://github.com/rstudio/packrat/"
    url      = "https://cloud.r-project.org/src/contrib/packrat_0.4.7-1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/packrat"

    version('0.5.0', sha256='d6a09290fbe037a6c740921c5dcd70b500e5b36e4713eae4010adf0c456bc5f7')
    version('0.4.9-3', sha256='87299938a751defc54eb00a029aecd3522d6349d900aaa8b3e1aa6bf31e98234')
    version('0.4.8-1', sha256='a283caf4fda419e6571ae9ca6210a59002a030721feb8a50c0d0787fd6f672f3')
    version('0.4.7-1', sha256='6e5067edd41a4086bb828617d3378210a3dbc995e223b02af811549519f3223a')

    depends_on('r@3.0.0:', type=('build', 'run'))
