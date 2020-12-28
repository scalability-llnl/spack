# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Scons(PythonPackage):
    """SCons is a software construction tool"""

    homepage = "http://scons.org"
    url      = "https://pypi.io/packages/source/s/scons/scons-3.1.1.tar.gz"

    version('3.1.2', sha256='8aaa483c303efeb678e6f7c776c8444a482f8ddc3ad891f8b6cdd35264da9a1f')
    version('3.1.1', sha256='fd44f8f2a4562e7e5bc8c63c82b01e469e8115805a3e9c2923ee54cdcd6678b3')
    version('3.1.0', sha256='94e0d0684772d3e6d9368785296716e0ed6ce757270b3ed814e5aa72d3163890')
    version('3.0.5', sha256='e95eaae17d9e490cf12cd37f091a6cbee8a628b5c8dbd3cab1f348f602f46462')
    version('3.0.4', sha256='72c0b56db84f40d3558f351918a0ab98cb4345e8696e879d3e271f4df4a5913c')
    version('3.0.1', sha256='24475e38d39c19683bc88054524df018fe6949d70fbd4c69e298d39a0269f173')
    version('2.5.1', sha256='c8de85fc02ed1a687b1f2ac791eaa0c1707b4382a204f17d782b5b111b9fdf07')
    version('2.5.0', sha256='01f1b3d6023516a8e1b5e77799e5a82a23b32953b1102d339059ffeca8600493')

    # Python 3 support was added in SCons 3.0.0
    depends_on('python@:2', when='@:2', type=('build', 'run'))
    depends_on('py-setuptools', when='@3.0.2:', type=('build', 'run'))

    patch('fjcompiler.patch', when='%fj')

    # Prevent passing --single-version-externally-managed to
    # setup.py, which it does not support.
    @when('@3.0.2:')
    def install_args(self, spec, prefix):
        return ['--prefix={0}'.format(prefix), '--root=/']

    def setup_run_environment(self, env):
        env.prepend_path('PYTHONPATH', self.prefix.lib.scons)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.prepend_path('PYTHONPATH', self.prefix.lib.scons)

    def setup_dependent_run_environment(self, env, dependent_spec):
        env.prepend_path('PYTHONPATH', self.prefix.lib.scons)
