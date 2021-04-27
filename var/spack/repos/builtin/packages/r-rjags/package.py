# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RRjags(RPackage):
    """Bayesian Graphical Models using MCMC

    Interface to the JAGS MCMC library."""

    homepage = "https://cloud.r-project.org/package=rjags"
    url      = "https://cloud.r-project.org/src/contrib/rjags_4-8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/rjags/"

    version('4-10', sha256='bd3e0bdf50b23b63061a0caa2428be585ccbf0b3f5d28eaa690e714e508d0ada')
    version('4-8', sha256='1529827ab11493fb5f05552e239d700ae2f818995d86d3c9e4c92523f594b59f')
    version('4-6', sha256='cf24bb1e7c8445bafb49097089ad33e5bd5d8efbccf16fc7e32ad230f05f89ad')

    depends_on('r@2.14.0:', type=('build', 'run'))
    depends_on('r-coda@0.13:', type=('build', 'run'))
    depends_on('jags@4.0.0:4.999.999', type=('link'))

    def configure_args(self):
        args = ['--with-jags-lib=%s' % self.spec['jags'].prefix.lib,
                '--with-jags-include=%s' % self.spec['jags'].prefix.include,
                '--with-jags-modules=%s/JAGS/modules-4'
                % self.spec['jags'].prefix.lib]
        return args
