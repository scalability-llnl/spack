# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Tk(AutotoolsPackage, SourceforgePackage):
    """Tk is a graphical user interface toolkit that takes developing
       desktop applications to a higher level than conventional
       approaches. Tk is the standard GUI not only for Tcl, but for
       many other dynamic languages, and can produce rich, native
       applications that run unchanged across Windows, Mac OS X, Linux
       and more."""
    homepage = "http://www.tcl.tk"
    sourceforge_mirror_path = "tcl/tk8.6.5-src.tar.gz"

    version('8.6.10', sha256='63df418a859d0a463347f95ded5cd88a3dd3aaa1ceecaeee362194bc30f3e386')
    version('8.6.8',  sha256='49e7bca08dde95195a27f594f7c850b088be357a7c7096e44e1158c7a5fd7b33')
    version('8.6.6',  sha256='d62c371a71b4744ed830e3c21d27968c31dba74dd2c45f36b9b071e6d88eb19d')
    version('8.6.5',  sha256='fbbd93541b4cd467841208643b4014c4543a54c3597586727f0ab128220d7946')
    version('8.6.3',  sha256='ba15d56ac27d8c0a7b1a983915a47e0f635199b9473cf6e10fbce1fc73fd8333')
    version('8.5.19', sha256='407af1de167477d598bd6166d84459a3bdccc2fb349360706154e646a9620ffa')

    variant('xft', default=True,
            description='Enable X FreeType')
    variant('xss', default=True,
            description='Enable X Screen Saver')

    extends('tcl')

    depends_on('tcl@8.6:', when='@8.6:')
    depends_on('libx11')
    depends_on('libxft', when='+xft')
    depends_on('libxscrnsaver', when='+xss')

    configure_directory = 'unix'

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            make('install')

            # Some applications like Expect require private Tk headers.
            make('install-private-headers')

            # Copy source to install tree
            installed_src = join_path(
                self.spec.prefix, 'share', self.name, 'src')
            stage_src = os.path.realpath(self.stage.source_path)
            install_tree(stage_src, installed_src)

            # Replace stage dir -> installed src dir in tkConfig
            filter_file(
                stage_src, installed_src,
                join_path(self.spec['tk'].libs.directories[0], 'tkConfig.sh'))

    @property
    def libs(self):
        return find_libraries(['libtk{0}'.format(self.version.up_to(2))],
                              root=self.prefix, recursive=True)

    def setup_run_environment(self, env):
        # When using Tkinter from within spack provided python+tkinter, python
        # will not be able to find Tcl/Tk unless TK_LIBRARY is set.
        env.set('TK_LIBRARY', self.spec['tk'].libs.directories[0])

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('TK_LIBRARY', self.spec['tk'].libs.directories[0])

    def configure_args(self):
        spec = self.spec
        config_args = [
            '--with-tcl={0}'.format(spec['tcl'].libs.directories[0]),
            '--x-includes={0}'.format(spec['libx11'].headers.directories[0]),
            '--x-libraries={0}'.format(spec['libx11'].libs.directories[0])
        ]
        config_args += self.enable_or_disable('xft')
        config_args += self.enable_or_disable('xss')

        return config_args

    @run_after('install')
    def symlink_wish(self):
        with working_dir(self.prefix.bin):
            symlink('wish{0}'.format(self.version.up_to(2)), 'wish')
