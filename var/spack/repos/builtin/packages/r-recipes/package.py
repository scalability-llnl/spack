# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRecipes(RPackage):
    """Preprocessing Tools to Create Design Matrices

    An extensible framework to create and preprocess design matrices.
    Recipes consist of one or more data manipulation and analysis "steps".
    Statistical parameters for the steps can be estimated from an initial data
    set and then applied to other data sets. The resulting design matrices can
    then be used as inputs into statistical or machine learning models."""

    homepage = "https://github.com/tidymodels/recipes"
    url      = "https://cloud.r-project.org/src/contrib/recipes_0.1.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/recipes"

    version('0.1.15', sha256='808ad2f4d68ae03aa27332437f037597e9c1bebd65ed4ebfab1d243ea6022e76')
    version('0.1.6', sha256='51e0db72de171d58d13ad8ffcf1dea402ab8f82100d161722041b6fd014cbfd9')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-generics', type=('build', 'run'))
    depends_on('r-generics@0.1.0:', when='@0.1.15:', type=('build', 'run'))
    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-gower', type=('build', 'run'))
    depends_on('r-ipred', type=('build', 'run'))
    depends_on('r-lifecycle', when='@0.1.15:', type=('build', 'run'))
    depends_on('r-lubridate', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-purrr@0.2.3:', type=('build', 'run'))
    depends_on('r-rlang@0.4.0:', type=('build', 'run'))
    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-tidyr@1.0.0:', when='@0.1.15:', type=('build', 'run'))
    depends_on('r-tidyselect@0.2.5:', type=('build', 'run'))
    depends_on('r-tidyselect@1.1.0:', when='@0.1.15:', type=('build', 'run'))
    depends_on('r-timedate', type=('build', 'run'))
    depends_on('r-withr', type=('build', 'run'))
