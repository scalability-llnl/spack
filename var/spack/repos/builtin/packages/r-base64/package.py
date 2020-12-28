# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBase64(RPackage):
    """Compatibility wrapper to replace the orphaned package by Romain
       Francois. New applications should use the 'openssl' or 'base64enc'
       package instead."""

    homepage = "https://cloud.r-project.org/package=base64"
    url      = "https://cloud.r-project.org/src/contrib/base64_2.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/base64"

    version('2.0', sha256='8e259c2b12446197d1152b83a81bab84ccb5a5b77021a9b5645dd4c63c804bd1')

    depends_on('r-openssl', type=('build', 'run'))
