# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RXgboost(RPackage):
    """Extreme Gradient Boosting, which is an efficient implementation of
    gradient boosting framework. This package is its R interface. The package
    includes efficient linear model solver and tree learning algorithms. The
    package can automatically do parallel computation on a single machine which
    could be more than 10 times faster than existing gradient boosting
    packages. It supports various objective functions, including regression,
    classification and ranking. The package is made to be extensible, so that
    users are also allowed to define their own objectives easily."""

    homepage = "https://github.com/dmlc/xgboost"
    url      = "https://cloud.r-project.org/src/contrib/xgboost_0.6-4.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/xgboost"

    version('0.90.0.2', sha256='240584c1b4d54a95b4fef9074480752fae9a5b096e8f84747457d641decfc9bf')
    version('0.81.0.1', sha256='3e7ada32e66881ea5c90aeafdab948927014c76cfff60a8e3d7f9e1f8a9ed7ce')
    version('0.6-4', sha256='9fc51dd1b910c70930357f617d1ac7a74c5056e8847d4188175db27c09f9d1ed')
    version('0.4-4', sha256='b955fc3352fcdc4894178c82fd62fbaf5e099c9d794f1e9daa2dd7b3494b61ff')

    depends_on('r@2.10:', when='@:0.4-4', type=('build', 'run'))
    depends_on('r@2.15.1:', when='@0.6-0:0.6-2', type=('build', 'run'))
    depends_on('r@3.3.0:', when='@0.6-3:', type=('build', 'run'))
    depends_on('r-matrix@1.1-0:', type=('build', 'run'))
    depends_on('r-data-table@1.9.6:', type=('build', 'run'))
    depends_on('r-magrittr@1.5:', type=('build', 'run'))
    depends_on('r-stringi@0.5.2:', type=('build', 'run'))

    # This is not listed as required, but installation fails without it
    # ERROR: dependency 'stringr' is not available for package 'xgboost'
    depends_on('r-stringr', type=('build', 'run'))
