# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMagrittr(RPackage):
    """Provides a mechanism for chaining commands with a new forward-pipe
    operator, %>%. This operator will forward a value, or the result of an
    expression, into the next function call/expression. There is flexible
    support for the type of right-hand side expressions. For more information,
    see package vignette."""

    homepage = "https://cloud.r-project.org/package=magrittr"
    url      = "https://cloud.r-project.org/src/contrib/magrittr_1.5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/magrittr"

    version('1.5', sha256='05c45943ada9443134caa0ab24db4a962b629f00b755ccf039a2a2a7b2c92ae8')
