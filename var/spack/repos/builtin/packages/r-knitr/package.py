# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RKnitr(RPackage):
    """Provides a general-purpose tool for dynamic report generation in R using
    Literate Programming techniques."""

    homepage = "https://cloud.r-project.org/package=knitr"
    url      = "https://cloud.r-project.org/src/contrib/knitr_1.14.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/knitr"

    version('1.28', sha256='05ee01da31d715bf24793efb3e4ef3bb3101ef1e1ab2d760c645fc5b9d40232a')
    version('1.24', sha256='e80c2043b445a7e576b62ae8510cce89322660fe388881d799a706d35cd27b89')
    version('1.23', sha256='063bfb3300fc9f3e7d223c346e19b93beced0e6784470b9bef2524868a206a99')
    version('1.17', sha256='9484a2b2c7b0c2aae24ab7f4eec6db48affbceb0e42bd3d69e34d953fe92f401')
    version('1.14', sha256='ba6d301482d020a911390d5eff181e1771f0e02ac3f3d9853a9724b1ec041aec')

    depends_on('r@2.14.1:', when='@:1.9', type=('build', 'run'))
    depends_on('r@3.0.2:', when='@1.10:1.14', type=('build', 'run'))
    depends_on('r@3.1.0:', when='@1.15:1.22', type=('build', 'run'))
    depends_on('r@3.2.3:', when='@1.23:', type=('build', 'run'))
    depends_on('r-evaluate@0.10:', type=('build', 'run'))
    depends_on('r-digest@:1.17', when='@:1.24', type=('build', 'run'))
    depends_on('r-formatr@:1.14', when='@:1.24', type=('build', 'run'))
    depends_on('r-highr', type=('build', 'run'))
    depends_on('r-stringr@0.6:', type=('build', 'run'))
    depends_on('r-markdown', type=('build', 'run'))
    depends_on('r-yaml@2.1.19:', type=('build', 'run'))
    depends_on('r-xfun', when='@1.23:', type=('build', 'run'))
