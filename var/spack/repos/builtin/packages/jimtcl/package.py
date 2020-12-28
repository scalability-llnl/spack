# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jimtcl(AutotoolsPackage):
    """A small-footprint implementation of the Tcl programming language."""

    homepage = "http://jim.tcl.tk/"
    url      = "https://github.com/msteveb/jimtcl/archive/0.79.tar.gz"

    version('0.79', sha256='ab8204cd03b946f5149e1273af9c86d8e73b146084a0fbeb1d4f41a75b0b3411')
    version('0.78', sha256='cf801795c9fd98bfff6882c14afdf96424ba86dead58c2a4e15978b176d3e12b')
    version('0.77', sha256='0874c50ab932c68940c29c48c014266a322c54ff357a0919386f32cc341eb3b2')
