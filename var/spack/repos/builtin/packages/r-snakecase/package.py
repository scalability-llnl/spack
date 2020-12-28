# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSnakecase(RPackage):
    """A consistent, flexible and easy to use tool to parse and convert strings
    into cases like snake or camel among others."""

    homepage = "https://github.com/Tazinho/snakecase"
    url      = "https://cloud.r-project.org/src/contrib/snakecase_0.11.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/snakecase"

    version('0.11.0', sha256='998420a58391ac85785e60bcdf6fd6927c82758ad2859a9a73a0e57299e8c1cf')

    depends_on('r@3.2:', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-stringi', type=('build', 'run'))
