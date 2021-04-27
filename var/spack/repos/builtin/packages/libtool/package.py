# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re


class Libtool(AutotoolsPackage, GNUMirrorPackage):
    """libtool -- library building part of autotools."""

    homepage = 'https://www.gnu.org/software/libtool/'
    gnu_mirror_path = "libtool/libtool-2.4.2.tar.gz"

    version('develop', git='https://git.savannah.gnu.org/git/libtool.git',
            branch='master', submodules=True)
    version('2.4.6', sha256='e3bd4d5d3d025a36c21dd6af7ea818a2afcd4dfc1ea5a17b39d7854bcd0c06e3')
    version('2.4.2', sha256='b38de44862a987293cd3d8dfae1c409d514b6c4e794ebc93648febf9afc38918')

    depends_on('m4@1.4.6:', type='build')
    depends_on('autoconf', type='build', when='@2.4.2,develop')
    depends_on('automake', type='build', when='@2.4.2,develop')
    depends_on('help2man', type='build', when='@2.4.2,develop')
    depends_on('xz', type='build', when='@develop')
    depends_on('texinfo', type='build', when='@develop')

    # Fix parsing of compiler output when collecting predeps and postdeps
    # http://lists.gnu.org/archive/html/bug-libtool/2016-03/msg00003.html
    patch('flag_space.patch', when='@develop')

    build_directory = 'spack-build'

    tags = ['build-tools']

    executables = ['^g?libtool(ize)?$']

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--version', output=str, error=str)
        match = re.search(r'\(GNU libtool\)\s+(\S+)', output)
        return match.group(1) if match else None

    @when('@2.4.2,develop')
    def autoreconf(self, spec, prefix):
        Executable('./bootstrap')()

    @property
    def libs(self):
        return find_libraries(
            ['libltdl'], root=self.prefix, recursive=True, shared=True
        )

    def _make_executable(self, name):
        return Executable(join_path(self.prefix.bin, name))

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies('%nvhpc@:20.11'):
            filter_file('-fno-builtin', '-Mnobuiltin', 'configure')
            filter_file('-fno-builtin', '-Mnobuiltin', 'libltdl/configure')

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.append_path('ACLOCAL_PATH', self.prefix.share.aclocal)

    def setup_dependent_package(self, module, dependent_spec):
        # Automake is very likely to be a build dependency, so we add
        # the tools it provides to the dependent module. Some build
        # systems differentiate between BSD libtool (e.g., Darwin) and
        # GNU libtool, so also add 'glibtool' and 'glibtoolize' to the
        # list of executables. See Homebrew:
        # https://github.com/Homebrew/homebrew-core/blob/master/Formula/libtool.rb
        executables = ['libtoolize', 'libtool', 'glibtoolize', 'glibtool']
        for name in executables:
            setattr(module, name, self._make_executable(name))

    @run_after('install')
    def post_install(self):
        # Some platforms name GNU libtool and GNU libtoolize
        # 'glibtool' and 'glibtoolize', respectively, to differentiate
        # them from BSD libtool and BSD libtoolize. On these BSD
        # platforms, build systems sometimes expect to use the assumed
        # GNU commands glibtool and glibtoolize instead of the BSD
        # variant; this happens frequently, for instance, on Darwin
        symlink(join_path(self.prefix.bin, 'libtool'),
                join_path(self.prefix.bin, 'glibtool'))
        symlink(join_path(self.prefix.bin, 'libtoolize'),
                join_path(self.prefix.bin, 'glibtoolize'))
