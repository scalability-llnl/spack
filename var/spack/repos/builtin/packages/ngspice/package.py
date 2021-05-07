# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Ngspice(AutotoolsPackage):
    """ngspice is the open source spice simulator for electric and
    electronic circuits."""

    homepage = "http://ngspice.sourceforge.net/"
    url      = "https://sourceforge.net/projects/ngspice/files/ngspice-33.tar.gz"
    git      = "git://git.code.sf.net/p/ngspice/ngspice"

    maintainers = ['aweits', 'cessenat']

    # Master version by default adds the experimental adms feature
    version('master', branch='master')
    version('34', sha256='2263fffc6694754972af7072ef01cfe62ac790800dad651bc290bfcae79bd7b5')
    version('33', sha256='b99db66cc1c57c44e9af1ef6ccb1dcbc8ae1df3e35acf570af578f606f8541f1')
    version('32', sha256='3cd90c4e94516d87c5b4d02a3a6405b1136b25d05c871d4fee1fd7c4c0d03ef2')
    version('31', sha256='845f3b0c962e47ded051dfbc134c3c1e4ac925c9f0ce1cb3df64eb9b9da5c282')
    version('30', sha256='08fe0e2f3768059411328a33e736df441d7e6e7304f8dad0ed5f28e15d936097')
    version('29', sha256='8d6d0ffbc15f248eb6ec3bde3b9d1397fbc95cb677e1c6a14ff46065c7f95c4a')
    version('27', sha256='0c08c7d57a2e21cf164496f3237f66f139e0c78e38345fbe295217afaf150695')

    # kicad needs build=lib, i.e. --with--ngshared
    variant(
        'build', default='lib',
        description='Build type: lib=ngshared, bin otherwise',
        values=('lib', 'bin'),
        multi=False,
    )

    variant('X', default=False, description='Use the X Window System')
    variant(
        'debug', default='auto',
        description='Enable debugging features: '
        'auto is yes for build=lib, no for build=bin',
        values=('auto', 'yes', 'no'),
        multi=False,
    )
    variant('xspice', default=False, description='Enable XSPICE enhancements')
    variant('cider', default=False, description='Enable CIDER enhancements')
    variant('openmp', default=False, description='Compile with multi-threading support')
    variant('readline', default=True, description='Build readline support (for bin)')
    variant('fft', default=True, description='Use external fftw lib')

    depends_on('fftw-api@3:~mpi~openmp', when='+fft~openmp')
    depends_on('fftw-api@3:~mpi+openmp', when='+fft+openmp')
    depends_on('readline', when='+readline build=bin')

    # Needed for autoreconf:
    depends_on('bison', type='build', when='@master')
    depends_on('flex', type='build', when='@master')

    # INSTALL indicates dependency on these but they are underlying
    # depends_on('freetype', when='+X build=bin')
    # depends_on('libxrender', when='+X build=bin')
    # depends_on('fontconfig', when='+X build=bin')
    # depends_on('libxft', when='+X build=bin')
    # depends_on('libxext', when='+X build=bin')
    # depends_on('libxmu', when='+X build=bin')
    depends_on('libxaw', when='+X build=bin')
    depends_on('libx11', when='+X build=bin')

    # Need autotools when building on master:
    depends_on("autoconf", type='build', when='@master')
    depends_on("automake", type='build', when='@master')
    depends_on("libtool", type='build', when='@master')

    depends_on("adms", when='@master')

    conflicts('%gcc@:4.9.9', when='@32:',
              msg='Failure to compile recent release with old gcc due to hicum2')
    conflicts('@28', msg='This release does not compile')

    @when('@master')
    def autoreconf(self, spec, prefix):
        Executable('./autogen.sh')('--adms')

    def configure_args(self):
        spec = self.spec
        args = []
        if 'build=lib' in spec:
            args.append('--with-ngshared')
            # Legacy debug is activated in auto debug mode with build=lib
            if 'debug=no' in spec:
                args.append('--disable-debug')
            args.append('--without-x')
        else:
            if 'debug=auto' in spec or 'debug=no' in spec:
                args.append('--disable-debug')
            if '+readline' in spec:
                args.append('--with-readline=yes')
            if '+X' in spec:
                args.append('--with-x')
                x = spec['libx11']
                args.extend([
                    '--x-includes=%s' % x.prefix.include,
                    '--x-libraries=%s' % x.prefix.lib,
                ])
            else:
                args.append('--without-x')
        if '+xspice' in spec:
            args.append('--enable-xspice')
        if '+cider' in spec:
            args.append('--enable-cider')

        if '+openmp' in spec:
            args.append('--enable-openmp')
        if '~fft' in spec:
            args.append('--with-fftw3=no')
        if 'darwin' in spec.architecture:
            args.append('--enable-pss')
        if '@master' in spec:
            args.append('--enable-adms')

        # Do not hide compilation line (easier to debug compilation)
        args.append('--disable-silent-rules')

        return args

    def flag_handler(self, name, flags):
        if self.spec.satisfies('%nvhpc') and name == 'cflags':
            flags.append('-Wall -Wextra -Wmissing-prototypes -Wstrict-prototypes')
            flags.append('-Wnested-externs -Wredundant-decls')
            if 'debug=yes' in self.spec:
                flags.append('-g')
        return (None, None, flags)
