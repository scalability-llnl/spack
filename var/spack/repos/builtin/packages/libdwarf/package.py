# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import sys

from spack.package import *


# Only build certain parts of dwarf because the other ones break.
dwarf_dirs = ['libdwarf', 'dwarfdump2']


class Libdwarf(Package):
    """The DWARF Debugging Information Format is of interest to
       programmers working on compilers and debuggers (and any one
       interested in reading or writing DWARF information). It was
       developed by a committee (known as the PLSIG at the time)
       starting around 1991. Starting around 1991 SGI developed the
       libdwarf and dwarfdump tools for internal use and as part of
       SGI IRIX developer tools. Since that time dwarfdump and
       libdwarf have been shipped (as an executable and archive
       respectively, not source) with every release of the SGI
       MIPS/IRIX C compiler."""

    homepage = "http://www.prevanders.net/dwarf.html"
    url      = "http://www.prevanders.net/libdwarf-20160507.tar.gz"
    list_url = homepage

    version('20180129', sha256='8bd91b57064b0c14ade5a009d3a1ce819f1b6ec0e189fc876eb8f42a8720d8a6')
    version('20160507', sha256='12ae39376e3915bf8fa92555989f3ad5f2f4f332b590a628541ce68987b337af')
    version('20130729', sha256='b6455d8616baf2883e2af91f006d6cbd583128fdfff46e3d1fae460bc223bb7b')
    version('20130207', sha256='5cb81459f0a1f6a2a10ef4635faddc2fa5e1a9e36901018c017759e491e708b8')
    version('20130126', sha256='c23c847935f8612f4fcdcfa0b3311f1553dcbd95bb683d3d5e030440201192fe')
    depends_on("elfutils@0.163", when='@20160507', type='link')
    depends_on("elf", type='link')
    depends_on('zlib', type='link')

    parallel = False

    def patch(self):
        filter_file(r'^typedef struct Elf Elf;$', '', 'libdwarf/libdwarf.h.in')

    def install(self, spec, prefix):
        # dwarf build does not set arguments for ar properly
        make.add_default_arg('ARFLAGS=rcs')

        # Dwarf doesn't provide an install, so we have to do it.
        mkdirp(prefix.bin, prefix.include, prefix.lib, prefix.man.man1)

        with working_dir('libdwarf'):
            extra_config_args = []

            # this is to prevent picking up system /usr/include/libelf.h
            if spec.satisfies('^libelf'):
                libelf_inc_dir = join_path(spec['libelf'].prefix,
                                           'include/libelf')
                extra_config_args.append(
                    'CFLAGS=-I{0} -Wl,-L{1} -Wl,-lelf'.format(
                        libelf_inc_dir, spec['libelf'].prefix.lib))
            configure("--prefix=" + prefix, "--enable-shared",
                      *extra_config_args)
            filter_file(r'^dwfzlib\s*=\s*-lz',
                        'dwfzlib=-L{0} -lz'.format(
                            self.spec['zlib'].prefix.lib),
                        'Makefile')
            make()

            libdwarf_name = 'libdwarf.{0}'.format(dso_suffix)
            libdwarf1_name = 'libdwarf.{0}'.format(dso_suffix) + ".1"
            install('libdwarf.a',  prefix.lib)
            install('libdwarf.so', join_path(prefix.lib, libdwarf1_name))
            if spec.satisfies('@20160507:'):
                with working_dir(prefix.lib):
                    os.symlink(libdwarf1_name, libdwarf_name)
            install('libdwarf.h',  prefix.include)
            install('dwarf.h',     prefix.include)

            # It seems like fix_darwin_install_name can't be used
            # here directly; the install name of the library in
            # the stage directory must be fixed in order for dyld
            # to locate it on Darwin when spack builds dwarfdump
            if sys.platform == 'darwin':
                install_name_tool = which('install_name_tool')
                install_name_tool('-id',
                                  join_path('..', 'libdwarf',
                                            'libdwarf.so'),
                                  'libdwarf.so')

        if spec.satisfies('@20130126:20130729'):
            dwarfdump_dir = 'dwarfdump2'
        else:
            dwarfdump_dir = 'dwarfdump'
        with working_dir(dwarfdump_dir):
            configure("--prefix=" + prefix)
            filter_file(r'^dwfzlib\s*=\s*-lz',
                        'dwfzlib=-L{0} -lz'.format(
                            self.spec['zlib'].prefix.lib),
                        'Makefile')

            # This makefile has strings of copy commands that
            # cause a race in parallel
            make(parallel=False)

            install('dwarfdump',      prefix.bin)
            install('dwarfdump.conf', prefix.lib)
            install('dwarfdump.1',    prefix.man.man1)

    @run_after('install')
    def darwin_fix(self):
        if sys.platform == 'darwin':
            fix_darwin_install_name(self.prefix.lib)
