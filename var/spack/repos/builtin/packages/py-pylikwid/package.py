# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class PyPylikwid(PythonPackage):
    """Python interface to the LIKWID tools library with calls for system
       topology, process/thread affinity, hardware performance monitoring
       and the manipulation of system features like frequencies and
       prefetchers."""

    homepage = "https://github.com/RRZE-HPC/pylikwid"
    url = "https://pypi.io/packages/source/p/pylikwid/pylikwid-0.4.0.tar.gz"
    git = "https://github.com/RRZE-HPC/pylikwid.git"

    maintainers = ['TomTheBear']

    version('0.4.0', sha256='f7894a6d7ebcea7da133ef639599a314f850f55cd6c5ffdd630bb879bd2aa0b8')

    variant('cuda',
            default=False,
            description='with Nvidia GPU profiling support')

    depends_on('likwid', when='~cuda')
    depends_on('likwid+cuda', when='+cuda')

    def setup_build_environment(self, env):
        env.set('LIKWID_PREFIX', self.spec['likwid'].prefix)
