# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMoPack(PythonPackage):
    """Packing methods used to encode and decode the data payloads of
    Met Office Unified Model 'fields'"""

    homepage = "https://github.com/SciTools/mo_pack"
    url      = "https://github.com/SciTools/mo_pack/archive/v0.2.0.tar.gz"

    version('0.2.0', sha256='4aa70e1f846b666670843bc2514435dedf7393203e88abaf74d48f8f2717a726')

    depends_on('libmo-unpack')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))

    def setup_build_environment(self, env):
        env.append_flags('LDFLAGS', self.spec['libmo-unpack'].libs.search_flags)
