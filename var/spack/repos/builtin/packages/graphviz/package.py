# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.operating_systems.mac_os import macos_version

import os
import sys


MACOS_VERSION = macos_version() if sys.platform == 'darwin' else None


class Graphviz(AutotoolsPackage):
    """Graph Visualization Software"""

    homepage = 'http://www.graphviz.org'
    git      = 'https://gitlab.com/graphviz/graphviz.git'

    # This commit hash is tag='stable_release_2.44.1'
    version('2.44.1', commit='771bc4dbff3e6f358fa75cdc7774a413ccacad51')
    # This commit hash is tag='stable_release_2.42.2'
    version('2.42.2', commit='da4c2ec6f24ca1b6d1752c6b5bc4389e55682147')
    # This commit hash is tag='stable_release_2.40.1'
    version('2.40.1', commit='67cd2e5121379a38e0801cc05cce5033f8a2a609')

    conflicts('%gcc@:5.9',
              when='@2.40.1+qt ^qt@5:',
              msg='graphviz-2.40.1 needs gcc-6 or greater to compile with QT5 '
              'suppport')

    # Language bindings
    language_bindings = ['java']

    # Additional language bindings are nominally supported by GraphViz via SWIG
    # but are untested and need the proper dependencies added:
    # language_bindings += ['sharp', 'go', 'guile', 'io', 'lua', 'ocaml',
    #                       'perl', 'php', 'python', 'r', 'ruby', 'tcl']

    for lang in language_bindings:
        variant(lang, default=False,
                description='Enable for optional {0} language '
                'bindings'.format(lang))

    # Feature variants
    variant('expat', default=False,
            description='Build with Expat support (enables HTML-like labels)')
    variant('gts', default=False,
            description='Build with GNU Triangulated Surface Library')
    variant('ghostscript', default=False,
            description='Build with Ghostscript support')
    variant('gtkplus', default=False,
            description='Build with GTK+ support')
    variant('libgd', default=False,
            description='Build with libgd support (more output formats)')
    variant('pangocairo', default=False,
            description='Build with pango+cairo support (more output formats)')
    variant('poppler', default=False,
            description='Build with poppler support (pdf formats)')
    variant('qt', default=False,
            description='Build with Qt support')
    variant('quartz', default=(MACOS_VERSION is not None),
            description='Build with Quartz and PDF support')
    variant('x', default=False,
            description='Use the X Window System')

    patch('http://www.linuxfromscratch.org/patches/blfs/9.0/graphviz-2.40.1-qt5-1.patch',
          sha256='bd532df325df811713e311d17aaeac3f5d6075ea4fd0eae8d989391e6afba930',
          when='@:2.40+qt^qt@5:')
    patch('https://raw.githubusercontent.com/easybuilders/easybuild-easyconfigs/master/easybuild/easyconfigs/g/Graphviz/Graphviz-2.38.0_icc_sfio.patch',
          sha256='393a0a772315a89dcc970b5efd4765d22dba83493d7956303673eb89c45b949f',
          level=0,
          when='@:2.40%intel')
    patch('https://raw.githubusercontent.com/easybuilders/easybuild-easyconfigs/master/easybuild/easyconfigs/g/Graphviz/Graphviz-2.40.1_icc_vmalloc.patch',
          sha256='813e6529e79161a18b0f24a969b7de22f8417b2e942239e658b5402884541bc2',
          when='@:2.40%intel')
    patch('ps2pdf.patch')
    patch('implicit.patch', level=0, when='@:2.44.0')

    if not MACOS_VERSION:
        conflicts('+quartz',
                  msg="Graphviz can only be build with Quartz on macOS.")
    elif MACOS_VERSION >= Version('10.9'):
        # Doesn't detect newer mac os systems as being new
        patch('fix-quartz-darwin.patch')

    # Language dependencies
    depends_on('java', when='+java')
    for lang in language_bindings:
        depends_on('swig', when=('+' + lang))

    # Feature dependencies
    depends_on('expat', when='+expat')
    depends_on('libgd', when='+libgd')
    depends_on('fontconfig', when='+libgd')
    depends_on('freetype', when='+libgd')
    depends_on('ghostscript', when='+ghostscript')
    depends_on('gtkplus', when='+gtkplus')
    depends_on('gts', when='+gts')
    depends_on('cairo+pdf+png+svg', when='+pangocairo')
    depends_on('fontconfig', when='+pangocairo')
    depends_on('freetype', when='+pangocairo')
    depends_on('glib', when='+pangocairo')
    depends_on('libpng', when='+pangocairo')
    depends_on('pango', when='+pangocairo')
    depends_on('poppler+glib', when='+poppler')
    depends_on('zlib')
    depends_on('qt', when='+qt')
    depends_on('libx11', when="+x")

    # Build dependencies
    depends_on('pkgconfig', type='build')
    # The following are needed when building from git
    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('bison', type='build')
    depends_on('flex', type='build')
    depends_on('libtool', type='build')
    # required to build docs
    depends_on('groff', type='build')
    depends_on('ghostscript', type='build')

    parallel = False

    def autoreconf(self, spec, prefix):
        # We need to generate 'configure' when checking out sources from git
        # If configure exists nothing needs to be done
        if os.path.exists(self.configure_abs_path):
            return
        # Else bootstrap (disabling auto-configure with NOCONFIG)
        bash = which('bash')
        bash('./autogen.sh', 'NOCONFIG')

    def setup_build_environment(self, env):
        if '+quartz' in self.spec:
            env.set('OBJC', self.compiler.cc)

    @when('%clang platform=darwin')
    def patch(self):
        # When using Clang, replace GCC's libstdc++ with LLVM's libc++
        mkdirs = ['cmd/dot', 'cmd/edgepaint', 'cmd/mingle', 'plugin/gdiplus']
        filter_file(r'-lstdc\+\+', '-lc++', 'configure.ac',
                    *(d + '/Makefile.am' for d in mkdirs))

    @when('%apple-clang')
    def patch(self):
        # When using Clang, replace GCC's libstdc++ with LLVM's libc++
        mkdirs = ['cmd/dot', 'cmd/edgepaint', 'cmd/mingle', 'plugin/gdiplus']
        filter_file(r'-lstdc\+\+', '-lc++', 'configure.ac',
                    *(d + '/Makefile.am' for d in mkdirs))

    def configure_args(self):
        spec = self.spec
        args = ['--disable-silent-rules']

        use_swig = False
        for lang in self.language_bindings:
            if '+' + lang in spec:
                use_swig = True
                args.append('--enable-' + lang)

        args.append('--{0}-swig'.format('enable' if use_swig else 'disable'))

        for var in ["expat", "gts", "ghostscript", "libgd", "pangocairo",
                    "poppler", "qt", "quartz", "x"]:
            args += self.with_or_without(var)

        args.append('--{0}-gtk'.format(
            "with" if "+gtkplus" in spec else "without"))

        return args
