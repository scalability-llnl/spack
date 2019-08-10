# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFutileOptions(RPackage):
    """A scoped options management framework"""

    homepage = "https://cran.rstudio.com/web/packages/futile.options/index.html"
    url      = "https://cran.rstudio.com/src/contrib/futile.options_1.0.0.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/futile.options"

    version('1.0.1', sha256='7a9cc974e09598077b242a1069f7fbf4fa7f85ffe25067f6c4c32314ef532570')
    version('1.0.0', '8fd845774bbce56f41f7c43c3b4c13ba')
