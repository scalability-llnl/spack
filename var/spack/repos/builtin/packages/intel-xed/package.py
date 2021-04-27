# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.pkgkit import *


class IntelXed(Package):
    """The Intel X86 Encoder Decoder library for encoding and decoding x86
    machine instructions (64- and 32-bit).  Also includes libxed-ild,
    a lightweight library for decoding the length of an instruction."""

    homepage = "https://intelxed.github.io/"
    git      = "https://github.com/intelxed/xed.git"
    maintainers = ['mwkrentel']

    mbuild_git = 'https://github.com/intelxed/mbuild.git'

    # Current versions now have actual releases and tags.
    version('master', branch='master')
    version('12.0.1', tag='12.0.1')
    version('11.2.0', tag='11.2.0')

    # The old 2019.03.01 version (before there were tags).
    version('10.2019.03', commit='b7231de4c808db821d64f4018d15412640c34113')

    resource(name='mbuild', placement='mbuild', git=mbuild_git,
             branch='master', when='@master')

    resource(name='mbuild', placement='mbuild', git=mbuild_git,
             commit='3e8eb33aada4153c21c4261b35e5f51f6e2019e8', when='@:999')

    variant('debug', default=False, description='Enable debug symbols')
    variant('pic', default=False,
            description='Compile with position independent code.')

    # The current mfile uses python3 by name.
    depends_on('python@3.4:', type='build')

    patch('1201-segv.patch', when='@12.0.1')

    conflicts('target=ppc64:', msg='intel-xed only runs on x86')
    conflicts('target=ppc64le:', msg='intel-xed only runs on x86')
    conflicts('target=aarch64:', msg='intel-xed only runs on x86')

    mycflags = []

    # Save CFLAGS for use in install.
    def flag_handler(self, name, flags):
        if name == 'cflags':
            self.mycflags = flags

            if '+pic' in self.spec:
                flags.append(self.compiler.cc_pic_flag)

        return (flags, None, None)

    def install(self, spec, prefix):
        # XED needs PYTHONPATH to find the mbuild directory.
        mbuild_dir = join_path(self.stage.source_path, 'mbuild')
        python_path = os.getenv('PYTHONPATH', '')
        os.environ['PYTHONPATH'] = mbuild_dir + ':' + python_path

        mfile = Executable(join_path('.', 'mfile.py'))

        args = ['-j', str(make_jobs),
                '--cc=%s' % spack_cc,
                '--no-werror']

        if '+debug' in spec:
            args.append('--debug')

        # If an optimization flag (-O...) is specified in CFLAGS, use
        # that, else set default opt level.
        for flag in self.mycflags:
            if flag.startswith('-O'):
                break
        else:
            args.append('--opt=2')

        # Build and install static libxed.a.
        mfile('--clean')
        mfile(*args)

        mkdirp(prefix.include)
        mkdirp(prefix.lib)
        mkdirp(prefix.bin)

        install(join_path('obj', 'lib*.a'), prefix.lib)

        # Build and install shared libxed.so and examples (to get the CLI).
        mfile('--clean')
        mfile('examples', '--shared', *args)

        install(join_path('obj', 'lib*.so'), prefix.lib)

        # Starting with 11.x, the install files are moved or copied into
        # subdirs of obj/wkit.
        if spec.satisfies('@11.0:'):
            wkit = join_path('obj', 'wkit')
            install(join_path(wkit, 'bin', 'xed'), prefix.bin)
            install(join_path(wkit, 'include', 'xed', '*.h'), prefix.include)
        else:
            # Old 2019.03.01 paths.
            install(join_path('obj', 'examples', 'xed'), prefix.bin)
            install(join_path('include', 'public', 'xed', '*.h'),
                    prefix.include)
            install(join_path('obj', '*.h'), prefix.include)
