##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import glob
import os


class Binutils(AutotoolsPackage):
    """GNU binutils, which contain the linker, assembler, objdump and others"""

    homepage = "http://www.gnu.org/software/binutils/"
    url      = "https://ftpmirror.gnu.org/binutils/binutils-2.28.tar.bz2"

    version('2.31.1', 'ffcc382695bf947da6135e7436b8ed52d991cf270db897190f19d6f9838564d0')
    version('2.29.1', '9af59a2ca3488823e453bb356fe0f113')
    version('2.28', '9e8340c96626b469a603c15c9d843727')
    version('2.27', '2869c9bf3e60ee97c74ac2a6bf4e9d68')
    version('2.26', '64146a0faa3b411ba774f47d41de239f')
    version('2.25', 'd9f3303f802a5b6b0bb73a335ab89d66')
    version('2.24', 'e0f71a7b2ddab0f8612336ac81d9636b')
    version('2.23.2', '4f8fa651e35ef262edc01d60fb45702e')
    version('2.20.1', '2b9dc8f2b7dbd5ec5992c6e29de0b764')

    variant('plugins', default=False,
            description="enable plugins, needed for gold linker")
    variant('gold', default=True, description="build the gold linker")
    variant('libiberty', default=False, description='Also install libiberty.')

    patch('cr16.patch', when='@:2.29.1')
    patch('update_symbol-2.26.patch', when='@2.26')

    depends_on('zlib')

    depends_on('m4', type='build')
    depends_on('flex', type='build')
    depends_on('bison', type='build')
    depends_on('gettext')

    def configure_args(self):
        spec = self.spec

        configure_args = [
            '--with-system-zlib',
            '--disable-dependency-tracking',
            '--disable-werror',
            '--enable-interwork',
            '--enable-multilib',
            '--enable-shared',
            '--enable-64-bit-bfd',
            '--enable-targets=all',
            '--with-sysroot=/',
        ]

        if '+gold' in spec:
            configure_args.append('--enable-gold')

        if '+plugins' in spec:
            configure_args.append('--enable-plugins')

        if '+libiberty' in spec:
            configure_args.append('--enable-install-libiberty')

        # To avoid namespace collisions with Darwin/BSD system tools,
        # prefix executables with "g", e.g., gar, gnm; see Homebrew
        # https://github.com/Homebrew/homebrew-core/blob/master/Formula/binutils.rb
        if spec.satisfies('platform=darwin'):
            configure_args.append('--program-prefix=g')

        return configure_args

    def install(self, spec, prefix):
        super(Binutils, self).install(spec, prefix)

        for current_file in glob.glob(os.path.join(self.build_directory, 
            'bfd', '*.h')):
            install(current_file, prefix.include)
        for current_file in glob.glob(os.path.join(self.build_directory, 
            'include', '*.h')):
            install(current_file, prefix.include)
        for subdir in ['aout', 'cgen', 'coff', 'elf', 'gdb', 'mach-o', 'nlm', 
            'opcode', 'som', 'vms']:
            outputdir=os.path.join(prefix.include, subdir)
            mkdirp(outputdir)
            for current_file in glob.glob(os.path.join(self.build_directory, 
                'include', subdir, '*')):
                install(current_file, outputdir)
        bfd_file=os.path.join(prefix.include, 'bfd.h')
        filter_file("#if !defined PACKAGE && !defined PACKAGE_VERSION", 
        "#if 0", bfd_file)
