# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RBroom(RPackage):
    """Convert Statistical Objects into Tidy Tibbles

    Summarizes key information about statistical objects in tidy tibbles. This
    makes it easy to report results, create plots and consistently work with
    large numbers of models at once. Broom provides three verbs that each
    provide different types of information about a model. tidy() summarizes
    information about model components such as coefficients of a regression.
    glance() reports information about an entire model, such as goodness of fit
    measures like AIC and BIC. augment() adds information about individual
    observations to a dataset, such as fitted values or influence measures."""

    homepage = "http://github.com/tidyverse/broom"
    url      = "https://cloud.r-project.org/src/contrib/broom_0.4.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/broom"

    version('0.7.3', sha256='de5650e46ca6884876b63bc401d22bef9eace671147774466406d43324aebc2f')
    version('0.5.2', sha256='16af7b446b24bc14461efbda9bea1521cf738c778c5e48fcc7bad45660a4ac62')
    version('0.5.1', sha256='da9e6bf7cb8f960b83309cf107743976cc32b54524675f6471982abe3d1aae2e')
    version('0.4.2', sha256='9f409413623cf25e7110452e6215353af5114f7044d73af182bd6c10971c5a44')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-backports', when='@0.5.0:', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-dplyr@1.0.0:', when='@0.7.3:', type=('build', 'run'))
    depends_on('r-ellipsis', when='@0.7.3:', type=('build', 'run'))
    depends_on('r-generics@0.0.2:', when='@0.5.1:', type=('build', 'run'))
    depends_on('r-glue', when='@0.7.3:', type=('build', 'run'))
    depends_on('r-purrr', when='@0.5.0:', type=('build', 'run'))
    depends_on('r-rlang', when='@0.7.3:', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-tibble', when='@0.5.0:', type=('build', 'run'))
    depends_on('r-tibble@3.0.0:', when='@0.7.3:', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-tidyr@1.0.0:', when='@0.7.3:', type=('build', 'run'))
    depends_on('r-plyr', when='@:0.4.2', type=('build', 'run'))
    depends_on('r-psych', when='@:0.4.2', type=('build', 'run'))
    depends_on('r-reshape2', when='@:0.5.2', type=('build', 'run'))
    depends_on('r-nlme', when='@:0.5.2', type=('build', 'run'))
