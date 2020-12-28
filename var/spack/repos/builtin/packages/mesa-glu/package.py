# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class MesaGlu(AutotoolsPackage):
    """This package provides the Mesa OpenGL Utility library."""

    homepage = "https://www.mesa3d.org"
    url      = "https://www.mesa3d.org/archive/glu/glu-9.0.0.tar.gz"

    version('9.0.1', sha256='f6f484cfcd51e489afe88031afdea1e173aa652697e4c19ddbcb8260579a10f7')
    version('9.0.0', sha256='4387476a1933f36fec1531178ea204057bbeb04cc2d8396c9ea32720a1f7e264')

    depends_on('gl@3:')

    provides('glu@1.3')

    @property
    def libs(self):
        for dir in ['lib64', 'lib']:
            libs = find_libraries('libGLU', join_path(self.prefix, dir),
                                  shared=True, recursive=False)
            if libs:
                return libs
