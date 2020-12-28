# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTidyselect(RPackage):
    """A backend for the selecting functions of the 'tidyverse'. It makes it
       easy to implement select-like functions in your own packages in a way
       that is consistent with other 'tidyverse' interfaces for selection."""

    homepage = "https://cloud.r-project.org/package=tidyselect"
    url      = "https://cloud.r-project.org/src/contrib/tidyselect_0.2.3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/tidyselect"

    version('0.2.5', sha256='5ce2e86230fa35cfc09aa71dcdd6e05e1554a5739c863ca354d241bfccb86c74')
    version('0.2.4', sha256='5cb30e56ad5c1ac59786969edc8d542a7a1735a129a474f585a141aefe6a2295')
    version('0.2.3', sha256='0c193abc8251a60e1d2a32a99c77651c336bc185e3c2a72e5f8781813d181c2c')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-glue@1.3.0:', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-rlang@0.2.2:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.0:', type=('build', 'run'))
