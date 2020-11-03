# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.operating_systems.mac_os import macos_version
import llnl.util.tty as tty
import itertools
import os
import sys

MACOS_VERSION = macos_version() if sys.platform == 'darwin' else None


class Qt(Package):
    """Qt is a comprehensive cross-platform C++ application framework."""
    homepage = 'http://qt.io'
    # Alternative location 'http://download.qt.io/official_releases/qt/'
    url      = 'http://download.qt.io/archive/qt/5.7/5.7.0/single/qt-everywhere-opensource-src-5.7.0.tar.gz'
    list_url = 'http://download.qt.io/archive/qt/'
    list_depth = 3
    maintainers = ['sethrj']

    phases = ['configure', 'build', 'install']

    version('5.14.2', sha256='c6fcd53c744df89e7d3223c02838a33309bd1c291fcb6f9341505fe99f7f19fa')
    version('5.14.1', sha256='6f17f488f512b39c2feb57d83a5e0a13dcef32999bea2e2a8f832f54a29badb8')
    version('5.14.0', sha256='be9a77cd4e1f9d70b58621d0753be19ea498e6b0da0398753e5038426f76a8ba')
    version('5.13.1', sha256='adf00266dc38352a166a9739f1a24a1e36f1be9c04bf72e16e142a256436974e')
    version('5.12.7', sha256='873783a0302129d98a8f63de9afe4520fb5f8d5316be8ad7b760c59875cd8a8d')
    version('5.12.5', sha256='a2299e21db7767caf98242767bffb18a2a88a42fee2d6a393bedd234f8c91298')
    version('5.12.2', sha256='59b8cb4e728450b21224dcaaa40eb25bafc5196b6988f2225c394c6b7f881ff5')
    version('5.11.3', sha256='859417642713cee2493ee3646a7fee782c9f1db39e41d7bb1322bba0c5f0ff4d')
    version('5.11.2', sha256='c6104b840b6caee596fa9a35bc5f57f67ed5a99d6a36497b6fe66f990a53ca81')
    version('5.10.0', sha256='936d4cf5d577298f4f9fdb220e85b008ae321554a5fcd38072dc327a7296230e')
    version('5.9.1',  sha256='7b41a37d4fe5e120cdb7114862c0153f86c07abbec8db71500443d2ce0c89795')
    version('5.9.0',  sha256='f70b5c66161191489fc13c7b7eb69bf9df3881596b183e7f6d94305a39837517')
    version('5.8.0',  sha256='9dc5932307ae452855863f6405be1f7273d91173dcbe4257561676a599bd58d3')
    version('5.7.1',  sha256='c86684203be61ae7b33a6cf33c23ec377f246d697bd9fb737d16f0ad798f89b7')
    version('5.7.0',  sha256='4661905915d6265243e17fe59852930a229cf5b054ce5af5f48b34da9112ab5f')
    version('5.5.1',  sha256='c7fad41a009af1996b62ec494e438aedcb072b3234b2ad3eeea6e6b1f64be3b3')
    version('5.4.2',  sha256='cfc768c55f0a0cd232bed914a9022528f8f2e50cb010bf0e4f3f62db3dfa17bd')
    version('5.4.0',  sha256='1739633424bde3d89164ae6ff1c5c913be38b9997e451558ef873aac4bbc408a')
    version('5.3.2',  sha256='c8d3fd2ead30705c6673c5e4af6c6f3973346b4fb2bd6079c7be0943a5b0282d')
    version('5.2.1',  sha256='84e924181d4ad6db00239d87250cc89868484a14841f77fb85ab1f1dbdcd7da1')
    version('4.8.7',  sha256='e2882295097e47fe089f8ac741a95fef47e0a73a3f3cdf21b56990638f626ea0')
    version('4.8.6',  sha256='8b14dd91b52862e09b8e6a963507b74bc2580787d171feda197badfa7034032c')
    version('4.8.5',  sha256='eb728f8268831dc4373be6403b7dd5d5dde03c169ad6882f9a8cb560df6aa138')
    version('3.3.8b', sha256='1b7a1ff62ec5a9cb7a388e2ba28fda6f960b27f27999482ebeceeadb72ac9f6e')

    variant('debug',      default=False,
            description="Build debug version.")
    variant('gtk',        default=False,
            description="Build with gtkplus.")
    variant('webkit',     default=False,
            description="Build the Webkit extension")
    variant('examples',   default=False,
            description="Build examples.")
    variant('framework',   default=bool(MACOS_VERSION),
            description="Build as a macOS Framework package.")
    variant('tools',      default=True,
            description="Build tools, including Qt Designer.")
    variant('dbus',       default=False,
            description="Build with D-Bus support.")
    variant('phonon',     default=False,
            description="Build with phonon support.")
    variant('opengl',     default=False,
            description="Build with OpenGL support.")
    variant('sql',        default=True,
            description="Build with SQL support.")
    variant('shared',     default=True,
            description='Build shared libraries.')
    variant('ssl',    default=True,
            description="Build with OpenSSL support.")
    variant('freetype', default='spack', description='Freetype2 support',
            values=('spack', 'qt', 'none'), multi=False)

    # Patches for qt@3
    patch('qt3-accept.patch', when='@3')
    patch('qt3-headers.patch', when='@3')

    # Patches for qt@4
    patch('qt4-configure-gcc.patch', when='@4:4.8.6 %gcc')
    patch('qt4-87-configure-gcc.patch', when='@4.8.7 %gcc')
    patch('qt4-tools.patch', when='@4+tools')
    patch('qt4-mac.patch', when='@4.8.7 platform=darwin')
    # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=925811
    patch("qt4-qforeach.patch", when="@4 %gcc@9:")

    # Patches for qt@4:
    # https://github.com/spack/spack/issues/1517
    patch('qt4-pcre.patch', when='@4')
    patch('qt5-pcre.patch', when='@5:')
    # https://bugreports.qt.io/browse/QTBUG-74196
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=89585
    patch('qt4-asm-volatile.patch', when='@4')
    patch('qt5-asm-volatile.patch', when='@5.0.0:5.12.1')

    # Patches for qt@5
    # https://bugreports.qt.io/browse/QTBUG-74219
    patch('qt5-btn_trigger_happy.patch', when='@5.7:5.12')
    # https://bugreports.qt.io/browse/QTBUG-57656
    patch('qt5-8-framework.patch', when='@5.8.0 +framework')
    # https://bugreports.qt.io/browse/QTBUG-58038
    patch('qt5-8-freetype.patch', when='@5.8.0 freetype=spack')
    # https://codereview.qt-project.org/c/qt/qtbase/+/245425
    patch('https://github.com/qt/qtbase/commit/a52d7861edfb5956de38ba80015c4dd0b596259b.patch',
          sha256='c49b228c27e3ad46ec3af4bac0e9985af5b5b28760f238422d32e14f98e49b1e',
          working_dir='qtbase',
          when='@5.10:5.12.0 %gcc@9:')
    # https://github.com/Homebrew/homebrew-core/pull/5951
    patch('qt5-restore-pc-files.patch', when='@5.9:5.11 platform=darwin')
    # https://github.com/spack/spack/issues/14400
    patch('qt5-11-intel-overflow.patch', when='@5.11 %intel')
    patch('qt5-12-intel-overflow.patch', when='@5.12:5.14.0 %intel')
    # https://bugreports.qt.io/browse/QTBUG-78937
    patch('qt5-12-configure.patch', when='@5.12')

    # Build-only dependencies
    depends_on("pkgconfig", type='build')
    depends_on("flex", when='+webkit', type='build')
    depends_on("bison", when='+webkit', type='build')
    depends_on("python", when='@5.7.0:', type='build')

    # Dependencies, then variant- and version-specific dependencies
    depends_on("icu4c")
    depends_on("jpeg")
    depends_on("libmng")
    depends_on("libtiff")
    depends_on("libxml2")
    depends_on("zlib")
    depends_on("freetype", when='freetype=spack')
    depends_on("gperf", when='+webkit')
    depends_on("gtkplus", when='+gtk')
    depends_on("openssl", when='+ssl')
    depends_on("sqlite+column_metadata", when='+sql', type=('build', 'run'))

    depends_on("libpng@1.2.57", when='@3')
    depends_on("libsm", when='@3')
    depends_on("pcre+multibyte", when='@5.0:5.8')
    depends_on("inputproto", when='@:5.8')
    depends_on("openssl@:1.0.999", when='@4:5.9+ssl')

    depends_on("glib", when='@4:')
    depends_on("libpng", when='@4:')
    depends_on("dbus", when='@4:+dbus')
    depends_on("gl", when='@4:+opengl')

    depends_on("harfbuzz", when='@5:')
    depends_on("double-conversion", when='@5.7:')
    depends_on("pcre2+multibyte", when='@5.9:')

    # gcc@4 is not supported as of Qt@5.14
    # https://doc.qt.io/qt-5.14/supported-platforms.html
    conflicts('%gcc@:4.99', when='@5.14:')

    # Non-macOS dependencies and special macOS constraints
    if MACOS_VERSION is None:
        depends_on("fontconfig", when='freetype=spack')
        depends_on("libsm")
        depends_on("libx11")
        depends_on("libxcb")
        depends_on("libxkbcommon")
        depends_on("xcb-util-image")
        depends_on("xcb-util-keysyms")
        depends_on("xcb-util-renderutil")
        depends_on("xcb-util-wm")
        depends_on("libxext")
        depends_on("libxrender")
        conflicts('+framework',
                  msg="QT cannot be built as a framework except on macOS.")
    else:
        conflicts('platform=darwin', when='@4.8.6',
                  msg="QT 4 for macOS is only patched for 4.8.7")

    use_xcode = True

    # Mapping for compilers/systems in the QT 'mkspecs'
    compiler_mapping = {'intel': ('icc',),
                        'apple-clang': ('clang-libc++', 'clang'),
                        'clang': ('clang-libc++', 'clang'),
                        'gcc': ('g++',)}
    platform_mapping = {'darwin': 'macx'}

    def url_for_version(self, version):
        # URL keeps getting more complicated with every release
        url = self.list_url

        if version >= Version('4.0'):
            url += str(version.up_to(2)) + '/'
        else:
            url += str(version.up_to(1)) + '/'

        if version >= Version('4.8'):
            url += str(version) + '/'

        if version >= Version('5'):
            url += 'single/'

        url += 'qt-'

        if version >= Version('4.6'):
            url += 'everywhere-'
        elif version >= Version('2.1'):
            url += 'x11-'

        if version >= Version('5.10.0'):
            url += 'src-'
        elif version >= Version('4.0'):
            url += 'opensource-src-'
        elif version >= Version('3'):
            url += 'free-'

        # 5.9 only has xz format. From 5.2.1 -> 5.8.0 .gz or .xz were possible
        if version >= Version('5.9'):
            url += str(version) + '.tar.xz'
        else:
            url += str(version) + '.tar.gz'

        return url

    def setup_build_environment(self, env):
        env.set('MAKEFLAGS', '-j{0}'.format(make_jobs))

    def setup_run_environment(self, env):
        env.set('QTDIR', self.prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('QTDIR', self.prefix)

    def setup_dependent_package(self, module, dependent_spec):
        module.qmake = Executable(join_path(self.spec.prefix.bin, 'qmake'))

    def get_mkspec(self):
        """Determine the mkspecs root directory and QT platform.
        """
        spec = self.spec
        cname = spec.compiler.name
        pname = spec.architecture.platform

        # Transform spack compiler name to a list of possible QT compilers
        cnames = self.compiler_mapping.get(cname, [cname])
        # Transform platform name to match those in QT
        pname = self.platform_mapping.get(pname, pname)

        qtplat = None
        mkspec_dir = 'qtbase/mkspecs' if spec.satisfies('@5:') else 'mkspecs'
        for subdir, cname in itertools.product(('', 'unsupported/'), cnames):
            platdirname = "".join([subdir, pname, "-", cname])
            tty.debug("Checking for platform '{0}' in {1}".format(
                      platdirname, mkspec_dir))
            if os.path.exists(os.path.join(mkspec_dir, platdirname)):
                qtplat = platdirname
                break
        else:
            tty.warn("No matching QT platform was found in {0} "
                     "for platform '{1}' and compiler {2}".format(
                         mkspec_dir, pname, ",".join(cnames)))

        return (mkspec_dir, qtplat)

    @when('@4 platform=darwin')
    def patch(self):
        ogl = self.spec['opengl'] if '+opengl' in self.spec else None
        deployment_target = str(MACOS_VERSION.up_to(2))

        patches = {
            'MACOSX_DEPLOYMENT_TARGET': deployment_target,
            'PREFIX': self.prefix,
            'OPENGL_INCDIR': ogl.prefix.include if ogl else "",
            'OPENGL_LIBS': ogl.libs.ld_flags if ogl else "",
        }

        def repl(match):
            # Replace the original config variable value with the one chosen
            # here if it is mentioned in 'patches'; otherwise return the
            # original value.
            return patches.get(match.group(1), match.group(0))

        files_to_filter = [
            "configure",
            "mkspecs/common/mac.conf",
            "mkspecs/common/unix.conf",
            "mkspecs/common/gcc-base-macx.conf",
            "mkspecs/common/gcc-base.conf",
            "qmake/generators/unix/unixmake.cpp",
            "qmake/qmake.pri",
            "src/tools/bootstrap/bootstrap.pro"
        ]
        if '%clang' in self.spec or '%apple-clang' in self.spec:
            files_to_filter += [
                "mkspecs/unsupported/macx-clang-libc++/qmake.conf",
                "mkspecs/common/clang.conf"
            ]
        elif '%gcc' in self.spec:
            files_to_filter += [
                "mkspecs/common/g++-macx.conf",
                "mkspecs/darwin-g++/qmake.conf"
            ]

        # Filter inserted configure variables
        filter_file(r'@([a-zA-Z0-9_]+)@', repl, *files_to_filter)

        # Remove debug build
        files_to_filter = [
            "src/3rdparty/webkit/Source/WebKit.pri",
            "src/3rdparty/webkit/Source/WebKit/qt/declarative/declarative.pro",
            "src/imports/qimportbase.pri",
            "src/plugins/qpluginbase.pri",
            "src/qbase.pri",
            "tools/designer/src/components/lib/lib.pro",
            "tools/designer/src/lib/lib.pro",
            "tools/designer/src/plugins/activeqt/activeqt.pro",
            "tools/designer/src/plugins/plugins.pri",
            "tools/designer/src/uitools/uitools.pro",
        ]
        filter_file(r'(\+=.*)debug_and_release', r'\1', *files_to_filter)

    @when('@4: %gcc')  # *NOT* darwin/mac gcc
    def patch(self):
        (mkspec_dir, platform) = self.get_mkspec()

        def conf(name):
            return os.path.join(mkspec_dir, 'common', name + '.conf')

        # Fix qmake compilers in the default mkspec
        filter_file('^QMAKE_CC .*', 'QMAKE_CC = cc', conf('g++-base'))
        filter_file('^QMAKE_CXX .*', 'QMAKE_CXX = c++', conf('g++-base'))

        # Don't error out on undefined symbols
        filter_file('^QMAKE_LFLAGS_NOUNDEF .*', 'QMAKE_LFLAGS_NOUNDEF = ',
                    conf('g++-unix'))

        if self.spec.satisfies('@4'):
            # The gnu98 flag is necessary to build with GCC 6 and other modern
            # compilers (see http://stackoverflow.com/questions/10354371/);
            # be permissive because of the abundance of older code, and hide
            # all warnings because there are so many of them with newer
            # compilers
            with open(conf('gcc-base'), 'a') as f:
                f.write("QMAKE_CXXFLAGS += -std=gnu++98 -fpermissive -w\n")

    @when('@4: %intel')
    def patch(self):
        (mkspec_dir, platform) = self.get_mkspec()
        conf_file = os.path.join(mkspec_dir, platform, "qmake.conf")

        # Intel's `ar` equivalent might not be in the path: replace it with
        # explicit
        xiar = os.path.join(os.path.dirname(self.compiler.cc), 'xiar')
        filter_file(r'\bxiar\b', xiar, conf_file)

        if self.spec.satisfies('@4'):
            with open(conf_file, 'a') as f:
                f.write("QMAKE_CXXFLAGS += -std=gnu++98\n")

    @when('@4 %clang')
    def patch(self):
        (mkspec_dir, platform) = self.get_mkspec()
        conf_file = os.path.join(mkspec_dir, platform, "qmake.conf")

        with open(conf_file, 'a') as f:
            f.write("QMAKE_CXXFLAGS += -std=gnu++98\n")

    @property
    def common_config_args(self):
        # incomplete list is here http://doc.qt.io/qt-5/configure-options.html
        config_args = [
            '-prefix', self.prefix,
            '-v',
            '-opensource',
            '-{0}opengl'.format('' if '+opengl' in self.spec else 'no-'),
            '-{0}'.format('debug' if '+debug' in self.spec else 'release'),
            '-confirm-license',
            '-optimized-qmake',
            '-no-pch',
        ]

        if self.spec.variants['freetype'].value == 'spack':
            config_args.extend([
                '-system-freetype'
            ])
            config_args.extend(
                self.spec['freetype'].headers.include_flags.split()
            )
            if not MACOS_VERSION:
                config_args.append('-fontconfig')

        elif self.spec.variants['freetype'].value == 'qt':
            config_args.append('-qt-freetype')
        else:
            config_args.append('-no-freetype')

        if '+ssl' in self.spec:
            openssl = self.spec['openssl']
            config_args.extend([
                '-openssl-linked',
                openssl.libs.search_flags,
                openssl.headers.include_flags,
            ])
        else:
            config_args.append('-no-openssl')

        if '+sql' in self.spec:
            sqlite = self.spec['sqlite']
            config_args.extend([
                '-system-sqlite',
                '-R', sqlite.prefix.lib,
            ])
        else:
            comps = ['db2', 'ibase', 'oci', 'tds', 'mysql', 'odbc', 'psql',
                     'sqlite', 'sqlite2']
            config_args.extend("-no-sql-" + component for component in comps)

        if '+shared' in self.spec:
            config_args.append('-shared')
        else:
            config_args.append('-static')

        if self.spec.satisfies('@5:'):
            pcre = self.spec['pcre'] if self.spec.satisfies('@5.0:5.8') \
                else self.spec['pcre2']
            harfbuzz = self.spec['harfbuzz']
            config_args.extend([
                '-system-harfbuzz',
                harfbuzz.libs.search_flags,
                harfbuzz.headers.include_flags,
                '-system-pcre',
                pcre.libs.search_flags,
                pcre.headers.include_flags
            ])

        if self.spec.satisfies('@5.7:'):
            dc = self.spec['double-conversion']
            config_args.extend([
                '-system-doubleconversion',
                dc.libs.search_flags,
                dc.headers.include_flags
            ])

        if '@:5.7.1' in self.spec:
            config_args.append('-no-openvg')
        else:
            # FIXME: those could work for other versions
            png = self.spec['libpng']
            config_args.append('-system-libpng')
            if not png.external:
                config_args.extend([
                    png.libs.search_flags,
                    png.headers.include_flags
                ])

            jpeg = self.spec['jpeg']
            config_args.append('-system-libjpeg')
            if not jpeg.external:
                config_args.extend([
                    jpeg.libs.search_flags,
                    jpeg.headers.include_flags,
                ])
            zlib = self.spec['zlib']
            config_args.append('-system-zlib')
            if not zlib.external:
                config_args.extend([
                    zlib.libs.search_flags,
                    zlib.headers.include_flags
                ])

        if '@:5.7.0' in self.spec:
            config_args.extend([
                # NIS is deprecated in more recent glibc,
                # but qt-5.7.1 does not recognize this option
                '-no-nis',
            ])

        if '~examples' in self.spec:
            config_args.extend(['-nomake', 'examples'])

        if '~tools' in self.spec:
            config_args.extend(['-nomake', 'tools'])

        if '+dbus' in self.spec:
            dbus = self.spec['dbus'].prefix
            config_args.append('-dbus-linked')
            config_args.append('-I%s/dbus-1.0/include' % dbus.lib)
            config_args.append('-I%s/dbus-1.0' % dbus.include)
            config_args.append('-L%s' % dbus.lib)
        else:
            config_args.append('-no-dbus')

        if MACOS_VERSION:
            config_args.append('-{0}framework'.format(
                '' if '+framework' in self.spec else 'no-'))

        (_, qtplat) = self.get_mkspec()
        if qtplat is not None:
            config_args.extend(['-platform', qtplat])

        return config_args

    @when('@3')
    def configure(self, spec, prefix):
        # A user reported that this was necessary to link Qt3 on ubuntu.
        # However, if LD_LIBRARY_PATH is not set the qt build fails, check
        # and set LD_LIBRARY_PATH if not set, update if it is set.
        if os.environ.get('LD_LIBRARY_PATH'):
            os.environ['LD_LIBRARY_PATH'] += os.pathsep + os.getcwd() + '/lib'
        else:
            os.environ['LD_LIBRARY_PATH'] = os.pathsep + os.getcwd() + '/lib'

        configure('-prefix', prefix,
                  '-v',
                  '-thread',
                  '-shared',
                  '-release',
                  '-fast')

    @when('@4')
    def configure(self, spec, prefix):
        config_args = self.common_config_args

        config_args.extend([
            '-fast',
            '-no-declarative-debug',
            '-{0}gtkstyle'.format('' if '+gtk' in spec else 'no-'),
            '-{0}webkit'.format('' if '+webkit' in spec else 'no-'),
            '-{0}phonon'.format('' if '+phonon' in spec else 'no-'),
            '-arch', str(spec.target.family),
            '-xmlpatterns',
        ])

        # Disable phonon backend until gstreamer is setup as dependency
        if '+phonon' in self.spec:
            config_args.append('-no-phonon-backend')

        if '~examples' in self.spec:
            config_args.extend(['-nomake', 'demos'])

        if MACOS_VERSION:
            sdkpath = which('xcrun')('--show-sdk-path', output=str).strip()
            config_args.extend([
                '-cocoa',
                '-sdk', sdkpath])

        configure(*config_args)

    @when('@5')
    def configure(self, spec, prefix):
        config_args = self.common_config_args
        version = self.version

        config_args.extend([
            '-no-eglfs',
            '-no-directfb',
            '-{0}gtk{1}'.format(
                '' if '+gtk' in spec else 'no-',
                '' if version >= Version('5.7') else 'style')
        ])

        if MACOS_VERSION:
            config_args.extend([
                '-no-xcb-xlib',
                '-no-pulseaudio',
                '-no-alsa',
            ])
            if version < Version('5.12'):
                config_args.append('-no-xinput2')
        else:
            # Linux-only QT5 dependencies
            config_args.append('-system-xcb')

        if '~webkit' in spec:
            config_args.extend([
                '-skip',
                'webengine' if version >= Version('5.7') else 'qtwebkit',
            ])

        if spec.satisfies('@5.7'):
            config_args.extend(['-skip', 'virtualkeyboard'])

        if version >= Version('5.8'):
            # relies on a system installed wayland, i.e. no spack package yet
            # https://wayland.freedesktop.org/ubuntu16.04.html
            # https://wiki.qt.io/QtWayland
            config_args.extend(['-skip', 'wayland'])

        if version >= Version('5.10') and '~opengl' in spec:
            config_args.extend([
                '-skip', 'webglplugin',
                '-skip', 'qt3d',
            ])

        if version >= Version('5.14') and '~opengl' in spec:
            config_args.extend([
                '-skip', 'qtquick3d',
            ])

        configure(*config_args)

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make("install")
