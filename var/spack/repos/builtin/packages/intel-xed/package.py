# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class IntelXed(Package):
    """The Intel X86 Encoder Decoder library for encoding and decoding x86
    machine instructions (64- and 32-bit).  Also includes libxed-ild,
    a lightweight library for decoding the length of an instruction."""

    homepage = "https://intelxed.github.io/"
    git      = "https://github.com/intelxed/xed.git"

    # The version name and git commit hashes for the main xed repo and
    # the mbuild resource.  Xed doesn't have official releases, only
    # git commits.

    version_list = [('2019.03.01',
                     'b7231de4c808db821d64f4018d15412640c34113',
                     '176544e1fb54b6bfb40f596111368981d287e951'),
                    ('2018.02.14',
                     '44d06033b69aef2c20ab01bfb518c52cd71bb537',
                     'bb9123152a330c7fa1ff1a502950dc199c83e177')]

    version('develop', branch='master')
    resource(name='mbuild',
             git='https://github.com/intelxed/mbuild.git',
             branch='master', placement='mbuild',
             when='@develop')

    for (vers, xed_hash, mbuild_hash) in version_list:
        version(vers, commit=xed_hash)
        resource(name='mbuild',
                 git='https://github.com/intelxed/mbuild.git',
                 commit=mbuild_hash,
                 when='@{0}'.format(vers))

    variant('debug', default=False, description='Enable debug symbols')

    # python module 'platform.linux_distribution' was removed in python 3.8
    depends_on('python@2.7:3.7', type='build')

    conflicts('target=ppc64:', msg='intel-xed only runs on x86')
    conflicts('target=ppc64le:', msg='intel-xed only runs on x86')

    mycflags = []

    # Save CFLAGS for use in install.
    def flag_handler(self, name, flags):
        if name == 'cflags':
            self.mycflags = flags
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

        # Install the xed program
        install(join_path('obj', 'examples', 'xed'), prefix.bin)

        # Install header files.
        install(join_path('include', 'public', 'xed', '*.h'), prefix.include)
        install(join_path('obj', '*.h'), prefix.include)
