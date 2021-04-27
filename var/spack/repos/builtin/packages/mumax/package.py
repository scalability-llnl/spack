# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import shutil


class Mumax(MakefilePackage, CudaPackage):
    """GPU accelerated micromagnetic simulator."""

    homepage = "http://mumax.github.io"
    url      = "https://github.com/mumax/3/archive/v3.10.tar.gz"

    maintainers = ['glennpj']

    version('3.10',
            sha256='42c858661cec3896685ff4babea11e711f71fd6ea37d20c2bed7e4a918702caa',
            preferred=True)
    version('3.10beta',
            sha256='f20fbd90a4b531fe5a0d8acc3d4505a092a5e426f5f53218a22a87d445daf0e9',
            url='https://github.com/mumax/3/archive/3.10beta.tar.gz')

    variant('cuda', default=True,
            description='Use CUDA; must be true')
    variant('gnuplot', default=False,
            description='Use gnuplot for graphs')

    depends_on('cuda')
    depends_on('go@:1.15', type='build')
    depends_on('gnuplot', type='run', when='+gnuplot')

    conflicts('~cuda', msg='mumax requires cuda')

    patch('https://github.com/mumax/3/commit/2cf5c9a6985c9eb16a124c6bd96aed75b4a30c24.patch',
          sha256='a43b2ca6c9f9edfb1fd6d916a599f85a57c8bb3f9ee38148b1988fd82feec8ad',
          when='@3.10beta')

    @property
    def cuda_arch(self):
        cuda_arch = ' '.join(self.spec.variants['cuda_arch'].value)
        if cuda_arch == 'none':
            raise InstallError(
                'Must select at least one value for cuda_arch'
            )
        return cuda_arch

    @property
    def gopath(self):
        return self.stage.path

    @property
    def mumax_gopath_dir(self):
        return join_path(self.gopath, 'src/github.com/mumax/3')

    def do_stage(self, mirror_only=False):
        super(Mumax, self).do_stage(mirror_only)
        if not os.path.exists(self.mumax_gopath_dir):
            # Need to move source to $GOPATH and then symlink the original
            # stage directory
            shutil.move(self.stage.source_path, self.mumax_gopath_dir)
            force_symlink(self.mumax_gopath_dir, self.stage.source_path)

    # filter out targets that do not exist
    def edit(self, spec, prefix):
        filter_file(r'(^all: cudakernels) hooks$', r'\1', 'Makefile')

    @when('@3.10beta')
    def edit(self, spec, prefix):
        filter_file(r'(^ln -sf .*)', r'#\1', 'make.bash')
        filter_file(r'(^\(cd test)', r'#\1', 'make.bash')
        filter_file(r'(for cc in ).*(; do)', r'\1{0}\2'.format(self.cuda_arch),
                    'cuda/make.bash')

    def setup_build_environment(self, env):
        env.prepend_path('GOPATH', self.gopath)
        env.set('CUDA_CC', self.cuda_arch)

    def install(self, spec, prefix):
        make()
        with working_dir(self.gopath):
            install_tree('bin', prefix.bin)
