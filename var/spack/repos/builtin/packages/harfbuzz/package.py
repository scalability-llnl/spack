# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Harfbuzz(AutotoolsPackage):
    """The Harfbuzz package contains an OpenType text shaping engine."""
    homepage = "https://github.com/harfbuzz/harfbuzz"
    url      = "http://www.freedesktop.org/software/harfbuzz/release/harfbuzz-0.9.37.tar.bz2"
    git      = "https://github.com/harfbuzz/harfbuzz.git"

    version('2.6.8', sha256='6648a571a27f186e47094121f0095e1b809e918b3037c630c7f38ffad86e3035')
    version('2.3.1', sha256='f205699d5b91374008d6f8e36c59e419ae2d9a7bb8c5d9f34041b9a5abcae468')
    version('2.1.3', sha256='613264460bb6814c3894e3953225c5357402915853a652d40b4230ce5faf0bee')
    version('1.9.0', sha256='11eca62bf0ac549b8d6be55f4e130946399939cdfe7a562fdaee711190248b00')
    version('1.4.6', sha256='21a78b81cd20cbffdb04b59ac7edfb410e42141869f637ae1d6778e74928d293')
    version('0.9.37', sha256='255f3b3842dead16863d1d0c216643d97b80bfa087aaa8fc5926da24ac120207')

    variant('graphite2', default=False, description='enable support for graphite2 font engine')

    depends_on("pkgconfig", type="build")
    depends_on("glib")
    depends_on("icu4c")
    depends_on("freetype")
    depends_on("cairo+pdf+ft")
    depends_on("zlib")
    depends_on("graphite2", when='+graphite2')

    conflicts('%intel', when='@2.3.1:',
              msg='harfbuzz-2.3.1 does not build with the Intel compiler')

    def url_for_version(self, version):
        if version > Version('2.3.1'):
            url = "https://github.com/harfbuzz/harfbuzz/releases/download/{0}/harfbuzz-{0}.tar.xz"
        else:
            url = "http://www.freedesktop.org/software/harfbuzz/release/harfbuzz-{0}.tar.bz2"

        return url.format(version)

    # Function borrowed from superlu
    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == 'cxxflags':
            flags.append(self.compiler.cxx11_flag)
        if name == 'cflags':
            if '%pgi' not in self.spec and self.spec.satisfies('%gcc@:5.1'):
                flags.append('-std=gnu99')
        return (None, None, flags)

    def configure_args(self):
        args = []
        # disable building of gtk-doc files following #9771
        args.append('--disable-gtk-doc-html')
        true = which('true')
        args.append('GTKDOC_CHECK={0}'.format(true))
        args.append('GTKDOC_CHECK_PATH={0}'.format(true))
        args.append('GTKDOC_MKPDF={0}'.format(true))
        args.append('GTKDOC_REBASE={0}'.format(true))
        args.extend(self.with_or_without('graphite2'))

        return args

    def patch(self):
        change_sed_delimiter('@', ';', 'src/Makefile.in')
