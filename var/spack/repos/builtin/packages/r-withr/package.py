# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RWithr(RPackage):
    """A set of functions to run code 'with' safely and temporarily modified
    global state. Many of these functions were originally a part of the
    'devtools' package, this provides a simple package with limited
    dependencies to provide access to these functions."""

    homepage = "http://github.com/jimhester/withr"
    url      = "https://cloud.r-project.org/src/contrib/withr_1.0.2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/withr"

    version('2.2.0', sha256='4c21e51cf48f8c281ddd5f5ec358ac446df3c982104fd00bfe62d9259d73b582')
    version('2.1.2', sha256='41366f777d8adb83d0bdbac1392a1ab118b36217ca648d3bb9db763aa7ff4686')
    version('1.0.2', sha256='2391545020adc4256ee7c2e31c30ff6f688f0b6032e355e1ce8f468cab455f10')
    version('1.0.1', sha256='7e245fdd17d290ff9e7c237159804dd06e1c6a3efe7855ed641eb0765a1e727d')

    depends_on('r@3.0.2:', type=('build', 'run'))
    depends_on('r@3.2:', when='@2.2:', type=('build', 'run'))
