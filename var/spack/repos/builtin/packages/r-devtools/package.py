# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDevtools(RPackage):
    """Tools to Make Developing R Packages Easier.

    Collection of package development tools."""

    cran = "devtools"

    version('2.4.3', sha256='e42159a9bca0b219170e76c282862e27ca283649d6cbf6a868175d8982e06b4f')
    version('2.3.2', sha256='e5086106baef6bb925445dfdddb3cd5ff4f8fff96353365b135aba5618d1986d')
    version('2.3.0', sha256='4fc375c171335c67bd71df4e0b1b3dff2ae3aa17b3e0566b790ba0808b39dcd0')
    version('2.1.0', sha256='c1f75346a90adf0669b5508fe68cc78bd3b114c1303fa7d22bf90991edd9230d')
    version('2.0.2', sha256='99a2fa957068254b8ecdb3fc2d50e2950230910ea31c314fc0e7d934e4bd1709')
    version('1.12.0', sha256='8a3e2ca3988dffe29341e45a160bb588995eae43485d6a811a9ae4836d37afd4')
    version('1.11.1', sha256='51c876f9ddbfdf611f6ea0b06c0b46da8cefcb8cc98d60e06d576b61f0a06346')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r-usethis@1.5.0:', type=('build', 'run'), when='@2.0.0:')
    depends_on('r-usethis@1.6.0:', type=('build', 'run'), when='@2.3.0:')
    depends_on('r-usethis@1.6.3:', type=('build', 'run'), when='@2.3.2:')
    depends_on('r-usethis@2.0.1:', type=('build', 'run'), when='@2.4.3:')
    depends_on('r-callr', type=('build', 'run'), when='@2.0.0:')
    depends_on('r-callr@3.4.3:', type=('build', 'run'), when='@2.3.0:')
    depends_on('r-callr@3.4.4:', type=('build', 'run'), when='@2.3.2:')
    depends_on('r-callr@3.4.4:', type=('build', 'run'), when='@2.3.2:')
    depends_on('r-callr@3.6.0:', type=('build', 'run'), when='@2.4.3:')
    depends_on('r-cli', type=('build', 'run'), when='@2.0.0:')
    depends_on('r-cli@2.0.2:', type=('build', 'run'), when='@2.3.0:')
    depends_on('r-cli@3.0.0:', type=('build', 'run'), when='@2.4.3:')
    depends_on('r-covr@3.5.0:', type=('build', 'run'), when='@2.3.0:')
    depends_on('r-covr@3.5.1:', type=('build', 'run'), when='@2.3.2:')
    depends_on('r-desc@1.2.0:', type=('build', 'run'), when='@2.3.0:')
    depends_on('r-desc@1.3.0:', type=('build', 'run'), when='@2.4.3:')
    depends_on('r-ellipsis@0.3.0:', type=('build', 'run'), when='@2.3.0:')
    depends_on('r-ellipsis@0.3.1:', type=('build', 'run'), when='@2.3.2:')
    depends_on('r-fs@1.5.0:', type=('build', 'run'), when='@2.4.3:')
    depends_on('r-httr@0.4:', type=('build', 'run'))
    depends_on('r-httr@1.4.1:', type=('build', 'run'), when='@2.3.0:')
    depends_on('r-httr@1.4.2:', type=('build', 'run'), when='@2.3.2:')
    depends_on('r-lifecycle@1.0.0:', type=('build', 'run'), when='@2.4.3:')
    depends_on('r-memoise@1.0.0:', type=('build', 'run'))
    depends_on('r-memoise@1.1.0:', type=('build', 'run'), when='@2.3.0:')
    depends_on('r-memoise@2.0.0:', type=('build', 'run'), when='@2.4.3:')
    depends_on('r-pkgbuild@1.0.3:', type=('build', 'run'), when='@2.0.0:')
    depends_on('r-pkgbuild@1.0.6:', type=('build', 'run'), when='@2.3.0:')
    depends_on('r-pkgbuild@1.1.0:', type=('build', 'run'), when='@2.3.2:')
    depends_on('r-pkgbuild@1.2.0:', type=('build', 'run'), when='@2.4.3:')
    depends_on('r-pkgload@1.0.2:', type=('build', 'run'), when='@2.0.0:')
    depends_on('r-pkgload@1.1.0:', type=('build', 'run'), when='@2.0.2:')
    depends_on('r-pkgload@1.2.1:', type=('build', 'run'), when='@2.4.3:')
    depends_on('r-rcmdcheck@1.3.3:', type=('build', 'run'), when='@2.0.0:')
    depends_on('r-remotes@2.1.0:', type=('build', 'run'), when='@2.0.0:')
    depends_on('r-remotes@2.1.1:', type=('build', 'run'), when='@2.3.0:')
    depends_on('r-remotes@2.2.0:', type=('build', 'run'), when='@2.3.2:')
    depends_on('r-remotes@2.3.0:', type=('build', 'run'), when='@2.4.3:')
    depends_on('r-rlang@0.4.5:', type=('build', 'run'), when='@2.3.0:')
    depends_on('r-rlang@0.4.7:', type=('build', 'run'), when='@2.3.2:')
    depends_on('r-rlang@0.4.10:', type=('build', 'run'), when='@2.4.3:')
    depends_on('r-roxygen2@6.1.1:', type=('build', 'run'), when='@2.0.0:')
    depends_on('r-roxygen2@7.1.0:', type=('build', 'run'), when='@2.3.0:')
    depends_on('r-roxygen2@7.1.1:', type=('build', 'run'), when='@2.3.2:')
    depends_on('r-rstudioapi@0.7.0:', type=('build', 'run'))
    depends_on('r-rstudioapi@0.11:', type=('build', 'run'), when='@2.3.0:')
    depends_on('r-rstudioapi@0.13:', type=('build', 'run'), when='@2.4.3:')
    depends_on('r-rversions@2.0.1:', type=('build', 'run'), when='@2.3.0:')
    depends_on('r-rversions@2.0.2:', type=('build', 'run'), when='@2.3.2:')
    depends_on('r-sessioninfo@1.1.1:', type=('build', 'run'), when='@2.0.0:')
    depends_on('r-testthat@2.1.1:', type=('build', 'run'), when='@2.0.0:')
    depends_on('r-testthat@2.3.2:', type=('build', 'run'), when='@2.3.0:')
    depends_on('r-testthat@3.0.2:', type=('build', 'run'), when='@2.4.3:')
    depends_on('r-withr', type=('build', 'run'))
    depends_on('r-withr@2.1.2:', type=('build', 'run'), when='@2.3.0:')
    depends_on('r-withr@2.2.0:', type=('build', 'run'), when='@2.3.2:')
    depends_on('r-withr@2.4.1:', type=('build', 'run'), when='@2.4.3:')

    depends_on('r-crayon@1.3.4:', type=('build', 'run'), when='@2.3.0')
    depends_on('r-digest', type=('build', 'run'), when='@:2.3.0')
    depends_on('r-digest@0.6.25:', type=('build', 'run'), when='@2.3.0')
    depends_on('r-glue@1.4.0:', type=('build', 'run'), when='@2.3.0')
    depends_on('r-git2r@0.23.0:', type=('build', 'run'), when='@:2.3.0')
    depends_on('r-git2r@0.26.1:', type=('build', 'run'), when='@2.3.0')
    depends_on('r-whisker', type=('build', 'run'), when='@:1.12.0')
    depends_on('r-dt@0.13:', type=('build', 'run'), when='@:2.3.0')
    depends_on('r-dt@0.15:', type=('build', 'run'), when='@2.3.2')
    depends_on('r-jsonlite', type=('build', 'run'), when='@:2.3.2')
    depends_on('r-jsonlite@1.6.1:', type=('build', 'run'), when='@2.3.0')
    depends_on('r-jsonlite@1.7.1:', type=('build', 'run'), when='@2.3.2')
