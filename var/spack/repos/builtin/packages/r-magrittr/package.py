# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class RMagrittr(RPackage):
    """A Forward-Pipe Operator for R

    Provides a mechanism for chaining commands with a new forward-pipe
    operator, %>%. This operator will forward a value, or the result of an
    expression, into the next function call/expression. There is flexible
    support for the type of right-hand side expressions. For more information,
    see package vignette."""

    homepage = "https://cloud.r-project.org/package=magrittr"
    url      = "https://cloud.r-project.org/src/contrib/magrittr_1.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/magrittr"

    version('2.0.1', sha256='75c265d51cc2b34beb27040edb09823c7b954d3990a7a931e40690b75d4aad5f')
    version('1.5', sha256='05c45943ada9443134caa0ab24db4a962b629f00b755ccf039a2a2a7b2c92ae8')
