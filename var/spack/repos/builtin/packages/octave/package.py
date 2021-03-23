# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path
import shutil
import sys
import tempfile

import spack.util.environment


class Octave(AutotoolsPackage, GNUMirrorPackage):
    """GNU Octave is a high-level language, primarily intended for numerical
    computations.

    It provides a convenient command line interface for solving linear and
    nonlinear problems numerically, and for performing other numerical
    experiments using a language that is mostly compatible with Matlab.
    It may also be used as a batch-oriented language.
    """

    homepage = "https://www.gnu.org/software/octave/"
    gnu_mirror_path = "octave/octave-4.0.0.tar.gz"
    maintainers = ['mtmiller']

    extendable = True

    version('6.2.0', sha256='457d1fda8634a839e2fd7cfc55b98bd56f36b6ae73d31bb9df43dde3012caa7c')
    version('6.1.0', sha256='6ff34e401658622c44094ecb67e497672e4337ca2d36c0702d0403ecc60b0a57')
    version('5.2.0', sha256='2fea62b3c78d6f38e9451da8a4d26023840725977dffee5250d3d180f56595e1')
    version('5.1.0', sha256='e36b1124cac27c7caa51cc57de408c31676d5f0096349b4d50b57bfe1bcd7495')
    version('4.4.1', sha256='09fbd0f212f4ef21e53f1d9c41cf30ce3d7f9450fb44911601e21ed64c67ae97')
    version('4.4.0', sha256='72f846379fcec7e813d46adcbacd069d72c4f4d8f6003bcd92c3513aafcd6e96')
    version('4.2.2', sha256='77b84395d8e7728a1ab223058fe5e92dc38c03bc13f7358e6533aab36f76726e')
    version('4.2.1', sha256='80c28f6398576b50faca0e602defb9598d6f7308b0903724442c2a35a605333b')
    version('4.2.0', sha256='443ba73782f3531c94bcf016f2f0362a58e186ddb8269af7dcce973562795567')
    version('4.0.2', sha256='39cd8fd36c218fc00adace28d74a6c7c9c6faab7113a5ba3c4372324c755bdc1')
    version('4.0.0', sha256='4c7ee0957f5dd877e3feb9dfe07ad5f39b311f9373932f0d2a289dc97cca3280')

    # patches
    # see https://savannah.gnu.org/bugs/?50234
    patch('patch_4.2.1_inline.diff', when='@4.2.1')

    # Variants
    variant('readline',   default=True)
    variant('arpack',     default=False)
    variant('curl',       default=False)
    variant('fftw',       default=False)
    variant('fltk',       default=False)
    variant('fontconfig', default=False)
    variant('freetype',   default=False)
    variant('glpk',       default=False)
    variant('gl2ps',      default=False)
    variant('gnuplot',    default=False)
    variant('magick',     default=False)
    variant('hdf5',       default=False)
    variant('jdk',        default=False)
    variant('llvm',       default=False)
    variant('opengl',     default=False)
    variant('qhull',      default=False)
    variant('qrupdate',   default=False)
    variant('qscintilla', default=False)
    variant('qt',         default=False)
    variant('suitesparse', default=False)
    variant('zlib',       default=False)

    # Required dependencies
    depends_on('blas')
    depends_on('lapack')
    # Octave does not configure with sed from darwin:
    depends_on('sed', when=sys.platform == 'darwin', type='build')
    depends_on('pcre')
    depends_on('pkgconfig', type='build')

    # Strongly recommended dependencies
    depends_on('readline',     when='+readline')

    # Optional dependencies
    depends_on('arpack-ng',    when='+arpack')
    depends_on('curl',         when='+curl')
    depends_on('fftw',         when='+fftw')
    depends_on('fltk',         when='+fltk')
    depends_on('fontconfig',   when='+fontconfig')
    depends_on('freetype',     when='+freetype')
    depends_on('glpk',         when='+glpk')
    depends_on('gl2ps',        when='+gl2ps')
    depends_on('gnuplot',      when='+gnuplot')
    depends_on('imagemagick',  when='+magick')
    depends_on('hdf5',         when='+hdf5')
    depends_on('java',         when='+jdk')        # TODO: requires Java 6 ?
    depends_on('llvm',         when='+llvm')
    depends_on('gl',           when='+opengl')
    depends_on('gl',           when='+fltk')
    depends_on('qhull',        when='+qhull')
    depends_on('qrupdate',     when='+qrupdate')
    depends_on('qscintilla',   when='+qscintilla')
    depends_on('qt+opengl',    when='+qt')
    depends_on('suite-sparse', when='+suitesparse')
    depends_on('zlib',         when='+zlib')

    def patch(self):
        # Filter mkoctfile.in.cc to use underlying compilers and not
        # Spack compiler wrappers. We are patching the template file
        # and not mkoctfile.cc since the latter is generated as part
        # of the build.
        mkoctfile_in = os.path.join(
            self.stage.source_path, 'src', 'mkoctfile.in.cc'
        )
        quote = lambda s: '"' + s + '"'
        entries_to_patch = {
            r'%OCTAVE_CONF_MKOCTFILE_CC%': quote(self.compiler.cc),
            r'%OCTAVE_CONF_MKOCTFILE_CXX%': quote(self.compiler.cxx),
            r'%OCTAVE_CONF_MKOCTFILE_F77%': quote(self.compiler.f77),
            r'%OCTAVE_CONF_MKOCTFILE_DL_LD%': quote(self.compiler.cxx),
            r'%OCTAVE_CONF_MKOCTFILE_LD_CXX%': quote(self.compiler.cxx)
        }

        for pattern, subst in entries_to_patch.items():
            filter_file(pattern, subst, mkoctfile_in)

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_mkoctfile_works_outside_of_build_env(self):
        # Check that mkoctfile is properly configured and can compile
        # Octave extensions outside of the build env
        mkoctfile = Executable(os.path.join(self.prefix, 'bin', 'mkoctfile'))
        helloworld_cc = os.path.join(
            os.path.dirname(__file__), 'helloworld.cc'
        )
        tmp_dir = tempfile.mkdtemp()
        shutil.copy(helloworld_cc, tmp_dir)

        # We need to unset these variables since we are still within
        # Spack's build environment when running tests
        vars_to_unset = ['CC', 'CXX', 'F77', 'FC']

        with spack.util.environment.preserve_environment(*vars_to_unset):
            # Delete temporarily the environment variables that point
            # to Spack compiler wrappers
            for v in vars_to_unset:
                del os.environ[v]
            # Check that mkoctfile outputs the expected value for CC
            cc = mkoctfile('-p', 'CC', output=str)
            msg = "mkoctfile didn't output the expected CC compiler"
            assert self.compiler.cc in cc, msg

            # Try to compile an Octave extension
            shutil.copy(helloworld_cc, tmp_dir)
            with working_dir(tmp_dir):
                mkoctfile('helloworld.cc')

    def configure_args(self):
        # See
        # https://github.com/macports/macports-ports/blob/master/math/octave/
        # https://github.com/Homebrew/homebrew-science/blob/master/octave.rb

        spec = self.spec
        config_args = []

        # Required dependencies
        config_args.extend([
            "--with-blas=%s" % spec['blas'].libs.ld_flags,
            "--with-lapack=%s" % spec['lapack'].libs.ld_flags
        ])

        # Strongly recommended dependencies
        if '+readline' in spec:
            config_args.append('--enable-readline')
        else:
            config_args.append('--disable-readline')

        # Optional dependencies
        if '+arpack' in spec:
            sa = spec['arpack-ng']
            config_args.extend([
                "--with-arpack-includedir=%s" % sa.prefix.include,
                "--with-arpack-libdir=%s"     % sa.prefix.lib
            ])
        else:
            config_args.append("--without-arpack")

        if '+curl' in spec:
            config_args.extend([
                "--with-curl-includedir=%s" % spec['curl'].prefix.include,
                "--with-curl-libdir=%s"     % spec['curl'].prefix.lib
            ])
        else:
            config_args.append("--without-curl")

        if '+fftw' in spec:
            config_args.extend([
                "--with-fftw3-includedir=%s"  % spec['fftw'].prefix.include,
                "--with-fftw3-libdir=%s"      % spec['fftw'].prefix.lib,
                "--with-fftw3f-includedir=%s" % spec['fftw'].prefix.include,
                "--with-fftw3f-libdir=%s"     % spec['fftw'].prefix.lib
            ])
        else:
            config_args.extend([
                "--without-fftw3",
                "--without-fftw3f"
            ])

        if '+fltk' in spec:
            config_args.extend([
                "--with-fltk-prefix=%s"      % spec['fltk'].prefix,
                "--with-fltk-exec-prefix=%s" % spec['fltk'].prefix
            ])
        else:
            config_args.append("--without-fltk")

        if '+glpk' in spec:
            config_args.extend([
                "--with-glpk-includedir=%s" % spec['glpk'].prefix.include,
                "--with-glpk-libdir=%s"     % spec['glpk'].prefix.lib
            ])
        else:
            config_args.append("--without-glpk")

        if '+magick' in spec:
            config_args.append("--with-magick=%s"
                               % spec['imagemagick'].prefix.lib)
        else:
            config_args.append("--without-magick")

        if '+hdf5' in spec:
            config_args.extend([
                "--with-hdf5-includedir=%s" % spec['hdf5'].prefix.include,
                "--with-hdf5-libdir=%s"     % spec['hdf5'].prefix.lib
            ])
        else:
            config_args.append("--without-hdf5")

        if '+jdk' in spec:
            config_args.extend([
                "--with-java-homedir=%s"    % spec['java'].home,
                "--with-java-includedir=%s" % spec['java'].home.include,
                "--with-java-libdir=%s"     % spec['java'].libs.directories[0]
            ])
        else:
            config_args.append("--disable-java")

        if '~opengl' and '~fltk' in spec:
            config_args.extend([
                "--without-opengl",
                "--without-framework-opengl"
            ])
        # TODO:  opengl dependency and package is missing?

        if '+qhull' in spec:
            config_args.extend([
                "--with-qhull-includedir=%s" % spec['qhull'].prefix.include,
                "--with-qhull-libdir=%s"     % spec['qhull'].prefix.lib
            ])
        else:
            config_args.append("--without-qhull")

        if '+qrupdate' in spec:
            config_args.extend([
                "--with-qrupdate-includedir=%s"
                % spec['qrupdate'].prefix.include,
                "--with-qrupdate-libdir=%s"     % spec['qrupdate'].prefix.lib
            ])
        else:
            config_args.append("--without-qrupdate")

        if '+zlib' in spec:
            config_args.extend([
                "--with-z-includedir=%s" % spec['zlib'].prefix.include,
                "--with-z-libdir=%s"     % spec['zlib'].prefix.lib
            ])
        else:
            config_args.append("--without-z")

        # If 64-bit BLAS is used:
        if (spec.satisfies('^openblas+ilp64') or
            spec.satisfies('^intel-mkl+ilp64') or
            spec.satisfies('^intel-parallel-studio+mkl+ilp64')):
            config_args.append('F77_INTEGER_8_FLAG=-fdefault-integer-8')

        # Use gfortran calling-convention %fj
        if spec.satisfies('%fj'):
            config_args.append('--enable-fortran-calling-convention=gfortran')

        return config_args

    # ========================================================================
    # Set up environment to make install easy for Octave extensions.
    # ========================================================================

    def setup_dependent_package(self, module, dependent_spec):
        """Called before Octave modules' install() methods.

        In most cases, extensions will only need to have one line:
            octave('--eval', 'pkg install %s' % self.stage.archive_file)
        """
        # Octave extension builds can have a global Octave executable function
        module.octave = Executable(join_path(self.spec.prefix.bin, 'octave'))
