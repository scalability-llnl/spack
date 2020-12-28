# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBroom(RPackage):
    """Convert statistical analysis objects from R into tidy data frames, so
       that they can more easily be combined, reshaped and otherwise processed
       with tools like 'dplyr', 'tidyr' and 'ggplot2'. The package provides
       three S3 generics: tidy, which summarizes a model's statistical
       findings such as coefficients of a regression; augment, which adds
       columns to the original data such as predictions, residuals and cluster
       assignments; and glance, which provides a one-row summary of
       model-level statistics."""

    homepage = "http://github.com/tidyverse/broom"
    url      = "https://cloud.r-project.org/src/contrib/broom_0.4.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/broom"

    version('0.5.2', sha256='16af7b446b24bc14461efbda9bea1521cf738c778c5e48fcc7bad45660a4ac62')
    version('0.5.1', sha256='da9e6bf7cb8f960b83309cf107743976cc32b54524675f6471982abe3d1aae2e')
    version('0.4.2', sha256='9f409413623cf25e7110452e6215353af5114f7044d73af182bd6c10971c5a44')

    depends_on('r@3.1:', type=('build', 'run'))
    depends_on('r-plyr', when='@:0.4.2', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'))
    depends_on('r-tidyr', type=('build', 'run'))
    depends_on('r-psych', when='@:0.4.2', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-nlme', type=('build', 'run'))
    depends_on('r-backports', when='@0.5.0:', type=('build', 'run'))
    depends_on('r-generics@0.0.2:', when='@0.5.1:', type=('build', 'run'))
    depends_on('r-purrr', when='@0.5.0:', type=('build', 'run'))
    depends_on('r-tibble', when='@0.5.0:', type=('build', 'run'))
