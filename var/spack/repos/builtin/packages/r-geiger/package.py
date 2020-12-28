# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGeiger(RPackage):
    """Methods for fitting macroevolutionary models to phylogenetic trees."""

    homepage = "https://cloud.r-project.org/package=geiger"
    url      = "https://cloud.r-project.org/src/contrib/geiger_2.0.6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/geiger"

    version('2.0.6.2', sha256='9153047b608d652821251206d1450bb3f517c8884379f498a695315574ae001d')
    version('2.0.6.1', sha256='2a95e20a3a90c096343b014344dd97e699e954da99c151c17fc6c245c77dba0b')
    version('2.0.6', sha256='e13b2c526378eaf9356b00bbe21b3c2c956327f8062fed638ccc1f49591c3eff')

    depends_on('r@2.15.0:', type=('build', 'run'))
    depends_on('r-ape@3.0-6:', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
    depends_on('r-subplex', type=('build', 'run'))
    depends_on('r-desolve@1.7:', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-rcpp@0.11.0:', type=('build', 'run'))
    depends_on('r-coda', type=('build', 'run'))
    depends_on('r-ncbit', type=('build', 'run'))
    depends_on('r-colorspace', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
