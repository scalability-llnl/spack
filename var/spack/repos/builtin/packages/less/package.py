# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Less(AutotoolsPackage):
    """The less utility is a text file browser that resembles more, but
    has more capabilities.  Less allows you to move backwards in the
    file aswell as forwards."""

    homepage = "http://www.greenwoodsoftware.com/less/"
    url      = "http://www.greenwoodsoftware.com/less/less-551.zip"

    version('551', sha256='2630db16ef188e88b513b3cc24daa9a798c45643cc7da06e549c9c00cfd84244')
    version('530', sha256='8c1652ba88a726314aa2616d1c896ca8fe9a30253a5a67bc21d444e79a6c6bc3')
