# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RParamhelpers(RPackage):
    """Functions for parameter descriptions and operations in black-box
       optimization, tuning and machine learning. Parameters can be described
       (type, constraints, defaults, etc.), combined to parameter sets and can
       in general be programmed on. A useful OptPath object (archive) to log
       function evaluations is also provided."""

    homepage = "https://github.com/berndbischl/ParamHelpers"
    url      = "https://cloud.r-project.org/src/contrib/ParamHelpers_1.10.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/ParamHelpers"

    version('1.12', sha256='b54db9e6608ba530345c380c757a60cb2b78ab08992a890b1a41914ce7abcc14')
    version('1.11', sha256='1614f4c0842cf822befc01228ab7263417f3423dd6a1dc24347b14f8491637a0')
    version('1.10', sha256='80629ba62e93b0b706bf2e451578b94fbb9c5b95ff109ecfb5b011bfe0a0fa5b')

    depends_on('r-bbmisc@1.10:', type=('build', 'run'))
    depends_on('r-checkmate@1.8.2:', type=('build', 'run'))
    depends_on('r-backports', when='@1.11:', type=('build', 'run'))
    depends_on('r-fastmatch', when='@1.11:', type=('build', 'run'))
