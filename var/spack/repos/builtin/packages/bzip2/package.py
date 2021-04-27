# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack import *


class Bzip2(Package, SourcewarePackage):
    """bzip2 is a freely available, patent free high-quality data
    compressor. It typically compresses files to within 10% to 15%
    of the best available techniques (the PPM family of statistical
    compressors), whilst being around twice as fast at compression
    and six times faster at decompression."""

    homepage = "https://sourceware.org/bzip2/"
    sourceware_mirror_path = "bzip2/bzip2-1.0.8.tar.gz"

    executables = [r'^bzip2$']

    version('1.0.8', sha256='ab5a03176ee106d3f0fa90e381da478ddae405918153cca248e682cd0c4a2269')
    version('1.0.7', sha256='e768a87c5b1a79511499beb41500bcc4caf203726fff46a6f5f9ad27fe08ab2b')
    version('1.0.6', sha256='a2848f34fcd5d6cf47def00461fcb528a0484d8edef8208d6d2e2909dc61d9cd')

    variant('shared', default=True, description='Enables the build of shared libraries.')

    depends_on('diffutils', type='build')

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('--help', output=str, error=str)
        match = re.search(r'bzip2, a block-sorting file compressor.'
                          '  Version ([^,]+)', output)
        return match.group(1) if match else None

    # override default implementation
    @property
    def libs(self):
        shared = '+shared' in self.spec
        return find_libraries(
            'libbz2', root=self.prefix, shared=shared, recursive=True
        )

    def patch(self):
        # bzip2 comes with two separate Makefiles for static and dynamic builds
        # Tell both to use Spack's compiler wrapper instead of GCC
        filter_file(r'^CC=gcc', 'CC={0}'.format(spack_cc), 'Makefile')
        filter_file(
            r'^CC=gcc', 'CC={0}'.format(spack_cc), 'Makefile-libbz2_so'
        )

        # The Makefiles use GCC flags that are incompatible with PGI
        if self.spec.satisfies('%pgi') or self.spec.satisfies('%nvhpc@:20.11'):
            filter_file('-Wall -Winline', '-Minform=inform', 'Makefile')
            filter_file('-Wall -Winline', '-Minform=inform',
                        'Makefile-libbz2_so')

        # Patch the link line to use RPATHs on macOS
        if 'darwin' in self.spec.architecture:
            v = self.spec.version
            v1, v2, v3 = (v.up_to(i) for i in (1, 2, 3))

            kwargs = {'ignore_absent': False, 'backup': False, 'string': True}

            mf = FileFilter('Makefile-libbz2_so')
            mf.filter('$(CC) -shared -Wl,-soname -Wl,libbz2.so.{0} -o libbz2.so.{1} $(OBJS)'  # noqa
                      .format(v2, v3),
                      '$(CC) -dynamiclib -Wl,-install_name -Wl,@rpath/libbz2.{0}.dylib -current_version {1} -compatibility_version {2} -o libbz2.{3}.dylib $(OBJS)'  # noqa
                      .format(v1, v2, v3, v3),
                      **kwargs)

            mf.filter(
                '$(CC) $(CFLAGS) -o bzip2-shared bzip2.c libbz2.so.{0}'.format(v3),  # noqa
                '$(CC) $(CFLAGS) -o bzip2-shared bzip2.c libbz2.{0}.dylib'
                .format(v3), **kwargs)
            mf.filter(
                'rm -f libbz2.so.{0}'.format(v2),
                'rm -f libbz2.{0}.dylib'.format(v2), **kwargs)
            mf.filter(
                'ln -s libbz2.so.{0} libbz2.so.{1}'.format(v3, v2),
                'ln -s libbz2.{0}.dylib libbz2.{1}.dylib'.format(v3, v2),
                **kwargs)

    def install(self, spec, prefix):
        # Build the dynamic library first
        if '+shared' in spec:
            make('-f', 'Makefile-libbz2_so')

        # Build the static library and everything else
        make()
        make('install', 'PREFIX={0}'.format(prefix))

        if '+shared' in spec:
            install('bzip2-shared', join_path(prefix.bin, 'bzip2'))

            v1, v2, v3 = (self.spec.version.up_to(i) for i in (1, 2, 3))
            if 'darwin' in self.spec.architecture:
                lib = 'libbz2.dylib'
                lib1, lib2, lib3 = ('libbz2.{0}.dylib'.format(v)
                                    for v in (v1, v2, v3))
            else:
                lib = 'libbz2.so'
                lib1, lib2, lib3 = ('libbz2.so.{0}'.format(v)
                                    for v in (v1, v2, v3))

            install(lib3, join_path(prefix.lib, lib3))
            with working_dir(prefix.lib):
                for libname in (lib, lib1, lib2):
                    symlink(lib3, libname)

        with working_dir(prefix.bin):
            force_remove('bunzip2', 'bzcat')
            symlink('bzip2', 'bunzip2')
            symlink('bzip2', 'bzcat')
