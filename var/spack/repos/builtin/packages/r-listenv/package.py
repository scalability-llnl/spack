# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RListenv(RPackage):
    """List environments are environments that have list-like properties. For
    instance, the elements of a list environment are ordered and can be
    accessed and iterated over using index subsetting."""

    homepage = "https://github.com/HenrikBengtsson/listenv"
    url      = "https://cloud.r-project.org/src/contrib/listenv_0.7.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/listenv"

    version('0.7.0', sha256='6126020b111870baea08b36afa82777cd578e88c17db5435cd137f11b3964555')

    depends_on('r@3.1.2:', type=('build', 'run'))
