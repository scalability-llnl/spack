# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RJomo(RPackage):
    """Similarly to Schafer's package 'pan', 'jomo' is a package for multilevel
    joint modelling multiple imputation (Carpenter and Kenward, 2013)
    <doi:10.1002/9781119942283>. Novel aspects of 'jomo' are the possibility of
    handling binary and categorical data through latent normal variables, the
    option to use cluster-specific covariance matrices and to impute compatibly
    with the substantive model.
    """

    homepage = "https://cloud.r-project.org/package=jomo"
    url      = "https://cloud.r-project.org/src/contrib/jomo_2.6-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/jomo"

    version('2.6-9', sha256='b90f47071e62b8863b00b1ae710a56ae6efbfe2baeb9963f8a91a10d6183cc9b')
    version('2.6-7', sha256='6e83dab51103511038a3e9a3c762e00cc45ae7080c0a0f64e37bcea8c488db53')
    version('2.6-2', sha256='67496d6d69ddbe9a796789fd8b3ac32cada09a81cf5a8e7b925a21e085e2d87f')

    depends_on('r-lme4', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-mass', when='@2.6-7:', type=('build', 'run'))
    depends_on('r-ordinal', when='@2.6-7:', type=('build', 'run'))
