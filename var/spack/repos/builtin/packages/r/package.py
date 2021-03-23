# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack import *


class R(AutotoolsPackage):
    """R is 'GNU S', a freely available language and environment for
    statistical computing and graphics which provides a wide variety of
    statistical and graphical techniques: linear and nonlinear modelling,
    statistical tests, time series analysis, classification, clustering, etc.
    Please consult the R project homepage for further information."""

    homepage = "https://www.r-project.org"
    url = "https://cloud.r-project.org/src/base/R-3/R-3.4.3.tar.gz"

    extendable = True

    maintainers = ['glennpj']

    version('4.0.4', sha256='523f27d69744a08c8f0bd5e1e6c3d89a4db29ed983388ba70963a3cd3a4a802e')
    version('4.0.3', sha256='09983a8a78d5fb6bc45d27b1c55f9ba5265f78fa54a55c13ae691f87c5bb9e0d')
    version('4.0.2', sha256='d3bceab364da0876625e4097808b42512395fdf41292f4915ab1fd257c1bbe75')
    version('4.0.1', sha256='95fe24a4d8d8f8f888460c8f5fe4311cec656e7a1722d233218bc03861bc6f32')
    version('4.0.0', sha256='06beb0291b569978484eb0dcb5d2339665ec745737bdfb4e873e7a5a75492940')
    version('3.6.3', sha256='89302990d8e8add536e12125ec591d6951022cf8475861b3690bc8bf1cefaa8f')
    version('3.6.2', sha256='bd65a45cddfb88f37370fbcee4ac8dd3f1aebeebe47c2f968fd9770ba2bbc954')
    version('3.6.1', sha256='5baa9ebd3e71acecdcc3da31d9042fb174d55a42829f8315f2457080978b1389')
    version('3.6.0', sha256='36fcac3e452666158e62459c6fc810adc247c7109ed71c5b6c3ad5fc2bf57509')
    version('3.5.3', sha256='2bfa37b7bd709f003d6b8a172ddfb6d03ddd2d672d6096439523039f7a8e678c')
    version('3.5.2', sha256='e53d8c3cf20f2b8d7a9c1631b6f6a22874506fb392034758b3bb341c586c5b62')
    version('3.5.1', sha256='0463bff5eea0f3d93fa071f79c18d0993878fd4f2e18ae6cf22c1639d11457ed')
    version('3.5.0', sha256='fd1725535e21797d3d9fea8963d99be0ba4c3aecadcf081b43e261458b416870')
    version('3.4.4', sha256='b3e97d2fab7256d1c655c4075934725ba1cd7cb9237240a11bb22ccdad960337')
    version('3.4.3', sha256='7a3cb831de5b4151e1f890113ed207527b7d4b16df9ec6b35e0964170007f426')
    version('3.4.2', sha256='971e30c2436cf645f58552905105d75788bd9733bddbcb7c4fbff4c1a6d80c64')
    version('3.4.1', sha256='02b1135d15ea969a3582caeb95594a05e830a6debcdb5b85ed2d5836a6a3fc78')
    version('3.4.0', sha256='288e9ed42457c47720780433b3d5c3c20983048b789291cc6a7baa11f9428b91')
    version('3.3.3', sha256='5ab768053a275084618fb669b4fbaadcc39158998a87e8465323829590bcfc6c')
    version('3.3.2', sha256='d294ad21e9f574fb4828ebb3a94b8cb34f4f304a41687a994be00dd41a4e514c')
    version('3.3.1', sha256='3dc59ae5831f5380f83c169bac2103ad052efe0ecec4ffa74bde4d85a0fda9e2')
    version('3.3.0', sha256='9256b154b1a5993d844bee7b1955cd49c99ad72cef03cce3cd1bdca1310311e4')
    version('3.2.5', sha256='60745672dce5ddc201806fa59f6d4e0ba6554d8ed78d0f9f0d79a629978f80b5')
    version('3.2.3', sha256='b93b7d878138279234160f007cb9b7f81b8a72c012a15566e9ec5395cfd9b6c1')
    version('3.2.2', sha256='9c9152e74134b68b0f3a1c7083764adc1cb56fd8336bec003fd0ca550cd2461d')
    version('3.2.1', sha256='d59dbc3f04f4604a5cf0fb210b8ea703ef2438b3ee65fd5ab536ec5234f4c982')
    version('3.2.0', sha256='f5ae953f18ba6f3d55b46556bbbf73441350f9fd22625402b723a2b81ff64f35')
    version('3.1.3', sha256='07e98323935baa38079204bfb9414a029704bb9c0ca5ab317020ae521a377312')
    version('3.1.2', sha256='bcd150afcae0e02f6efb5f35a6ab72432be82e849ec52ce0bb89d8c342a8fa7a')

    variant('external-lapack', default=False,
            description='Links to externally installed BLAS/LAPACK')
    variant('X', default=False,
            description='Enable X11 support (TCLTK, PNG, JPEG, TIFF, CAIRO)')
    variant('memory_profiling', default=False,
            description='Enable memory profiling')
    variant('rmath', default=False,
            description='Build standalone Rmath library')

    depends_on('blas', when='+external-lapack')
    depends_on('lapack', when='+external-lapack')
    depends_on('bzip2')
    depends_on('curl')
    depends_on('icu4c')
    depends_on('java')
    depends_on('ncurses')
    depends_on('pcre', when='@:3.6.3')
    depends_on('pcre2', when='@4:')
    depends_on('readline')
    depends_on('xz')
    depends_on('zlib@1.2.5:')
    depends_on('cairo+X+gobject+pdf', when='+X')
    depends_on('pango+X', when='+X')
    depends_on('harfbuzz+graphite2', when='+X')
    depends_on('jpeg', when='+X')
    depends_on('libpng', when='+X')
    depends_on('libtiff', when='+X')
    depends_on('libx11', when='+X')
    depends_on('libxmu', when='+X')
    depends_on('libxt', when='+X')
    depends_on('tk', when='+X')

    patch('zlib.patch', when='@:3.3.2')

    # R cannot be built with '-O2' optimization
    # with Fujitsu Compiler @4.1.0 now.
    # Until the Fujitsu compiler resolves this problem,
    # temporary fix to lower the optimization level.
    patch('change_optflags_tmp.patch', when='%fj@4.1.0')

    # R custom URL version
    def url_for_version(self, version):
        """Handle R's customed URL versions"""
        url = 'https://cloud.r-project.org/src/base'
        return url + '/R-%s/R-%s.tar.gz' % (version.up_to(1), version)

    filter_compiler_wrappers(
        'Makeconf', relative_root=os.path.join('rlib', 'R', 'etc')
    )

    @property
    def etcdir(self):
        return join_path(prefix, 'rlib', 'R', 'etc')

    @run_after('build')
    def build_rmath(self):
        if '+rmath' in self.spec:
            with working_dir('src/nmath/standalone'):
                make()

    @run_after('install')
    def install_rmath(self):
        if '+rmath' in self.spec:
            with working_dir('src/nmath/standalone'):
                make('install')

    def configure_args(self):
        spec   = self.spec
        prefix = self.prefix

        config_args = [
            '--libdir={0}'.format(join_path(prefix, 'rlib')),
            '--enable-R-shlib',
            '--enable-BLAS-shlib',
            '--enable-R-framework=no',
            '--without-recommended-packages',
            'LDFLAGS=-L{0} -Wl,-rpath,{0}'.format(join_path(prefix, 'rlib',
                                                            'R', 'lib')),
        ]

        if '+external-lapack' in spec:
            if '^mkl' in spec and 'gfortran' in self.compiler.fc:
                mkl_re = re.compile(r'(mkl_)intel(_i?lp64\b)')
                config_args.extend([
                    mkl_re.sub(r'\g<1>gf\g<2>',
                               '--with-blas={0}'.format(
                                   spec['blas'].libs.ld_flags)),
                    '--with-lapack'
                ])
            else:
                config_args.extend([
                    '--with-blas={0}'.format(spec['blas'].libs.ld_flags),
                    '--with-lapack'
                ])

        if '+X' in spec:
            config_args.append('--with-cairo')
            config_args.append('--with-jpeglib')
            config_args.append('--with-libpng')
            config_args.append('--with-libtiff')
            config_args.append('--with-tcltk')
            config_args.append('--with-x')

            tcl_config_path = join_path(
                spec['tcl'].libs.directories[0], 'tclConfig.sh')
            config_args.append('--with-tcl-config={0}'.format(tcl_config_path))

            tk_config_path = join_path(
                spec['tk'].libs.directories[0], 'tkConfig.sh')
            config_args.append('--with-tk-config={0}'.format(tk_config_path))
        else:
            config_args.append('--without-cairo')
            config_args.append('--without-jpeglib')
            config_args.append('--without-libpng')
            config_args.append('--without-libtiff')
            config_args.append('--without-tcltk')
            config_args.append('--without-x')

        if '+memory_profiling' in spec:
            config_args.append('--enable-memory-profiling')

        # Set FPICFLAGS for compilers except 'gcc'.
        if self.compiler.name != 'gcc':
            config_args.append('FPICFLAGS={0}'.format(
                self.compiler.cc_pic_flag))

        return config_args

    @run_after('install')
    def copy_makeconf(self):
        # Make a copy of Makeconf because it will be needed to properly build R
        # dependencies in Spack.
        src_makeconf = join_path(self.etcdir, 'Makeconf')
        dst_makeconf = join_path(self.etcdir, 'Makeconf.spack')
        install(src_makeconf, dst_makeconf)

    # ========================================================================
    # Set up environment to make install easy for R extensions.
    # ========================================================================

    @property
    def r_lib_dir(self):
        return join_path('rlib', 'R', 'library')

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Set R_LIBS to include the library dir for the
        # extension and any other R extensions it depends on.
        r_libs_path = []
        for d in dependent_spec.traverse(
                deptype=('build', 'run'), deptype_query='run'):
            if d.package.extends(self.spec):
                r_libs_path.append(join_path(d.prefix, self.r_lib_dir))

        r_libs_path = ':'.join(r_libs_path)
        env.set('R_LIBS', r_libs_path)
        env.set('R_MAKEVARS_SITE',
                join_path(self.etcdir, 'Makeconf.spack'))

        # Use the number of make_jobs set in spack. The make program will
        # determine how many jobs can actually be started.
        env.set('MAKEFLAGS', '-j{0}'.format(make_jobs))

    def setup_dependent_run_environment(self, env, dependent_spec):
        # For run time environment set only the path for dependent_spec and
        # prepend it to R_LIBS
        if dependent_spec.package.extends(self.spec):
            env.prepend_path('R_LIBS', join_path(
                dependent_spec.prefix, self.r_lib_dir))

    def setup_run_environment(self, env):
        env.prepend_path('LIBRARY_PATH',
                         join_path(self.prefix, 'rlib', 'R', 'lib'))
        env.prepend_path('LD_LIBRARY_PATH',
                         join_path(self.prefix, 'rlib', 'R', 'lib'))
        env.prepend_path('CPATH',
                         join_path(self.prefix, 'rlib', 'R', 'include'))

    def setup_dependent_package(self, module, dependent_spec):
        """Called before R modules' install() methods. In most cases,
        extensions will only need to have one line:
            R('CMD', 'INSTALL', '--library={0}'.format(self.module.r_lib_dir),
              self.stage.source_path)"""

        # R extension builds can have a global R executable function
        module.R = Executable(join_path(self.spec.prefix.bin, 'R'))

        # Add variable for library directry
        module.r_lib_dir = join_path(dependent_spec.prefix, self.r_lib_dir)

        # Make the site packages directory for extensions, if it does not exist
        # already.
        if dependent_spec.package.is_extension:
            mkdirp(module.r_lib_dir)
