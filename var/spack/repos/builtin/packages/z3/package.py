# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Z3(MakefilePackage):
    """Z3 is a theorem prover from Microsoft Research.
    It is licensed under the MIT license."""

    homepage = "https://github.com/Z3Prover/z3/wiki"
    url      = "https://github.com/Z3Prover/z3/archive/z3-4.5.0.tar.gz"

    version('4.8.7', sha256='8c1c49a1eccf5d8b952dadadba3552b0eac67482b8a29eaad62aa7343a0732c3')
    version('4.5.0', sha256='aeae1d239c5e06ac183be7dd853775b84698db1265cb2258e5918a28372d4a0c')
    version('4.4.1', sha256='50967cca12c5c6e1612d0ccf8b6ebf5f99840a783d6cf5216336a2b59c37c0ce')
    version('4.4.0', sha256='65b72f9eb0af50949e504b47080fb3fc95f11c435633041d9a534473f3142cba')

    phases = ['bootstrap', 'build', 'install']

    variant('python', default=True, description='Enable python binding')
    depends_on('python+shared', type=('build', 'run'), when="+python")
    extends('python', when='+python')

    # Referenced: https://github.com/Z3Prover/z3/issues/1016
    patch('fix_1016_1.patch', when='@:4.4.1')
    patch('fix_1016_2.patch', when='@4.5.0')

    using_py26 = "^python@:2.6.99"
    patch('py26-1.patch', when=using_py26)
    patch('py26-2.patch', when=using_py26)
    patch('py26-3.patch', when=using_py26)
    depends_on('py-argparse', type=('build', 'run'), when=using_py26)
    depends_on('py-setuptools@:25.2.0', type=('build', 'run'), when=using_py26)

    build_directory = 'build'

    def configure_args(self, prefix):
        spec = self.spec

        args = []

        if spec.satisfies('+python'):
            args.append('--python')
            args.append(
                '--pypkgdir=%s' % join_path(
                    prefix.lib,
                    'python%s' % spec['python'].version.up_to(2),
                    'site-packages'))

        return args

    def bootstrap(self, spec, prefix):
        options = ['--prefix={0}'.format(prefix)] + self.configure_args(prefix)
        spec['python'].command('scripts/mk_make.py', *options)
