# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Modules2tuple(GoPackage):
    """Generate GH_TUPLE/GL_TUPLE from modules.txt."""

    homepage = "https://github.com/hartzell/modules2tuple"
    url      = "https://github.com/hartzell/modules2tuple/archive/v0.11.3.tar.gz"

    # TODO: if/when the dust settles on GoPackage,
    # https://github.com/dmgk/modules2tuple/pull/8 should be wrapped
    # up and a real version added here.
    version('dev', sha256='c64388553fd6d6e991fe5e2563637bfe6a0084bc2fd86d0147521274b2491460',
            url='https://www.github.com/hartzell/modules2tuple/tarball/b5be39d09ad196a546c33b01c007d2796fc4e790')

    depends_on('go@1.13:', type='build')  # go.mod value overrides default

    executables = ['modules2tuple']
