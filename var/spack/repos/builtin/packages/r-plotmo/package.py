# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPlotmo(RPackage):
    """plotmo: Plot a Model's Residuals, Response, and Partial Dependence
    Plots.

    Plot model surfaces for a wide variety of models using partial dependence
    plots and other techniques. Also plot model residuals and other information
    on the model."""

    homepage = "http://www.milbo.users.sonic.net/"
    url      = "https://cloud.r-project.org/src/contrib/plotmo_3.5.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/plotmo"

    version('3.5.6', sha256='78f08dc897136d21fa8ade2acb6290351b569d29eb0592c7074c0be3cf2aa594')

    depends_on('r@3.4.0:', type=('build', 'run'))
    depends_on('r-formula@1.2-3:', type=('build', 'run'))
    depends_on('r-plotrix', type=('build', 'run'))
    depends_on('r-teachingdemos', type=('build', 'run'))
