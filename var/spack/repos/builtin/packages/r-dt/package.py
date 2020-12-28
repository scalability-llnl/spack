# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDt(RPackage):
    """Data objects in R can be rendered as HTML tables using the JavaScript
    library 'DataTables' (typically via R Markdown or Shiny). The 'DataTables'
    library has been included in this R package. The package name 'DT' is an
    abbreviation of 'DataTables'."""

    homepage = "http://rstudio.github.io/DT"
    url      = "https://cloud.r-project.org/src/contrib/DT_0.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/DT"

    version('0.13', sha256='79a073fe96980ce150d790ab76133c9e80bd463270c34d149c03934a622d63b5')
    version('0.8', sha256='90195054148806cf31c7db5c41f72d5389c75adc0b1183606a9babd2c6ae8e21')
    version('0.7', sha256='1de3f170deccd9e3aaefc057dd87c498e3b3f7f88eff645cf165ac34ffe3de2c')
    version('0.6', sha256='2ed68e9d161559171fa74b6105eee87b98acf755eae072b38ada60a83d427916')
    version('0.4', sha256='3daa96b819ca54e5fbc2c7d78cb3637982a2d44be58cea0683663b71cfc7fa19')
    version('0.3', sha256='ef42b24c9ea6cfa1ce089687bf858d773ac495dc80756d4475234e979bd437eb')
    version('0.2', sha256='a1b7f9e5c31a241fdf78ac582499f346e915ff948554980bbc2262c924b806bd')
    version('0.1', sha256='129bdafededbdcc3279d63b16f00c885b215f23cab2edfe33c9cbe177c8c4756')

    depends_on('r-htmltools@0.3.6:', type=('build', 'run'))
    depends_on('r-htmlwidgets@1.3:', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-crosstalk', type=('build', 'run'))
    depends_on('r-promises', when='@0.5:', type=('build', 'run'))
    depends_on('r-jsonlite@0.9.16:', when='@0.8:', type=('build', 'run'))
