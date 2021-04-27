# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Gloo(CMakePackage):
    """Gloo is a collective communications library."""

    homepage = "https://github.com/facebookincubator/gloo"
    git      = "https://github.com/facebookincubator/gloo.git"

    version('master')
