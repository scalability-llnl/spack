# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGss(RPackage):
    """A comprehensive package for structural multivariate function
    estimation using smoothing splines."""

    homepage = "https://cloud.r-project.org/package=gss"
    url      = "https://cloud.r-project.org/src/contrib/gss_2.1-7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/gss"

    version('2.1-10', sha256='26c47ecae6a9b7854a1b531c09f869cf8b813462bd8093e3618e1091ace61ee2')
    version('2.1-7', sha256='0405bb5e4c4d60b466335e5da07be4f9570045a24aed09e7bc0640e1a00f3adb')

    depends_on('r@2.14.0:', type=('build', 'run'))
