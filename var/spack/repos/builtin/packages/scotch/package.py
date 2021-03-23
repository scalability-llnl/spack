# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Scotch(Package):
    """Scotch is a software package for graph and mesh/hypergraph
       partitioning, graph clustering, and sparse matrix ordering."""

    homepage = "http://scotch.gforge.inria.fr/"
    git      = "https://gitlab.inria.fr/scotch/scotch.git"
    url      = "http://gforge.inria.fr/frs/download.php/latestfile/298/scotch_6.0.4.tar.gz"
    list_url = "http://gforge.inria.fr/frs/?group_id=248"

    version('6.0.10', sha256='fd8b707b8200823312a1571d97d3776ff3dfd3280cfa4b6e38987153cea5dbda')
    version('6.0.9', sha256='622b4143cf01c480bb15708b3651b29c25e4aeb00c8c6447ff196aca2eca5c93')
    version('6.0.8', sha256='0ba3f145026174304f910c8770a3cbb034f213c91d939573751cfbb4fd46d45e')
    version('6.0.6', sha256='686f0cad88d033fe71c8b781735ff742b73a1d82a65b8b1586526d69729ac4cf')
    version('6.0.5a', sha256='5b21b95e33acd5409d682fa7253cefbdffa8db82875549476c006d8cbe7c556f')
    version('6.0.4', sha256='f53f4d71a8345ba15e2dd4e102a35fd83915abf50ea73e1bf6efe1bc2b4220c7')
    version('6.0.3', sha256='6461cc9f28319a9dbe6cc10e28c0cbe90b4b25e205723c3edcde9a3ff974d6d8')
    version('6.0.0', sha256='8206127d038bda868dda5c5a7f60ef8224f2e368298fbb01bf13fa250e378dd4')
    version('5.1.10b', sha256='54c9e7fafefd49d8b2017d179d4f11a655abe10365961583baaddc4eeb6a9add')

    variant('mpi', default=True,
            description='Activate the compilation of parallel libraries')
    variant('compression', default=True,
            description='Activate the posibility to use compressed files')
    variant('esmumps', default=False,
            description='Activate the compilation of esmumps needed by mumps')
    variant('shared', default=True,
            description='Build a shared version of the library')
    variant('metis', default=True,
            description='Build metis and parmetis wrapper libraries')
    variant('int64', default=False,
            description='Use int64_t for SCOTCH_Num typedef')

    # Does not build with flex 2.6.[23]
    depends_on('flex@:2.6.1,2.6.4:', type='build')
    depends_on('bison', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('zlib', when='+compression')

    # Version-specific patches
    patch('nonthreaded-6.0.4.patch', when='@6.0.4')
    patch('esmumps-ldflags-6.0.4.patch', when='@6.0.4')
    patch('metis-headers-6.0.4.patch', when='@6.0.4')

    patch('libscotchmetis-return-6.0.5a.patch', when='@6.0.5a')

    # NOTE: In cross-compiling environment parallel build
    # produces weird linker errors.
    parallel = False

    # NOTE: Versions of Scotch up to version 6.0.0 don't include support for
    # building with 'esmumps' in their default packages.  In order to enable
    # support for this feature, we must grab the 'esmumps' enabled archives
    # from the Scotch hosting site.  These alternative archives include a
    # superset of the behavior in their default counterparts, so we choose to
    # always grab these versions for older Scotch versions for simplicity.
    @when('@:6.0.0')
    def url_for_version(self, version):
        url = "http://gforge.inria.fr/frs/download.php/latestfile/298/scotch_{0}_esmumps.tar.gz"
        return url.format(version)

    @property
    def libs(self):

        shared = '+shared' in self.spec
        libraries = ['libscotch', 'libscotcherr']
        zlibs     = []

        if '+mpi' in self.spec:
            libraries = ['libptscotch', 'libptscotcherr'] + libraries
            if '+esmumps' in self.spec:
                libraries = ['libptesmumps'] + libraries
        elif '~mpi+esmumps' in self.spec:
            libraries = ['libesmumps'] + libraries

        scotchlibs = find_libraries(
            libraries, root=self.prefix, recursive=True, shared=shared
        )
        if '+compression' in self.spec:
            zlibs = self.spec['zlib'].libs

        return scotchlibs + zlibs

    def patch(self):
        self.configure()

    # NOTE: Configuration of Scotch is achieved by writing a 'Makefile.inc'
    # file that contains all of the configuration variables and their desired
    # values for the installation.  This function writes this file based on
    # the given installation variants.
    def configure(self):
        makefile_inc = []
        cflags = [
            '-O3',
            '-DCOMMON_RANDOM_FIXED_SEED',
            '-DSCOTCH_DETERMINISTIC',
            '-DSCOTCH_RENAME',
        ]

        if '+int64' in self.spec:
            # SCOTCH_Num typedef: size of integers in arguments
            cflags.append('-DINTSIZE64')
            cflags.append('-DIDXSIZE64')  # SCOTCH_Idx typedef: indices for addressing
        else:
            cflags.append('-DIDXSIZE32')  # SCOTCH_Idx typedef: indices for addressing

        if self.spec.satisfies('platform=darwin'):
            cflags.extend([
                '-Drestrict=__restrict'
            ])

        # Library Build Type #
        if '+shared' in self.spec:
            if self.spec.satisfies('platform=darwin'):
                makefile_inc.extend([
                    'LIB       = .dylib',
                    'CLIBFLAGS = -dynamiclib {0}'.format(
                        self.compiler.cc_pic_flag
                    ),
                    'RANLIB    = echo',
                    'AR        = $(CC)',
                    'ARFLAGS   = -dynamiclib $(LDFLAGS) -Wl,-install_name -Wl,%s/$(notdir $@) -undefined dynamic_lookup -o ' % prefix.lib  # noqa
                ])
            else:
                makefile_inc.extend([
                    'LIB       = .so',
                    'CLIBFLAGS = -shared {0}'.format(
                        self.compiler.cc_pic_flag),
                    'RANLIB    = echo',
                    'AR        = $(CC)',
                    'ARFLAGS   = -shared $(LDFLAGS) -o'
                ])
            cflags.append(self.compiler.cc_pic_flag)
        else:
            makefile_inc.extend([
                'LIB       = .a',
                'CLIBFLAGS = ',
                'RANLIB    = ranlib',
                'AR        = ar',
                'ARFLAGS   = -ruv '
            ])

        # Compiler-Specific Options #

        if self.compiler.name == 'gcc':
            cflags.append('-Drestrict=__restrict')
        elif self.compiler.name == 'intel':
            cflags.append('-Drestrict=')

        mpicc_path = self.spec['mpi'].mpicc if '+mpi' in self.spec else 'mpicc'
        makefile_inc.append('CCS       = $(CC)')
        makefile_inc.append('CCP       = %s' % mpicc_path)
        makefile_inc.append('CCD       = $(CCS)')

        # Extra Features #

        ldflags = []

        if '+compression' in self.spec:
            cflags.append('-DCOMMON_FILE_COMPRESS_GZ')
            ldflags.append(' {0} '.format(self.spec['zlib'].libs.joined()))

        cflags.append('-DCOMMON_PTHREAD')

        # NOTE: bg-q platform needs -lpthread (and not -pthread)
        # otherwise we get illegal instruction error during runtime
        if self.spec.satisfies('platform=darwin'):
            cflags.append('-DCOMMON_PTHREAD_BARRIER')
            ldflags.append('-lm -pthread')
        else:
            ldflags.append('-lm -lrt -pthread')

        makefile_inc.append('LDFLAGS   = %s' % ' '.join(ldflags))

        # General Features #

        flex_path = self.spec['flex'].command.path
        bison_path = self.spec['bison'].command.path
        makefile_inc.extend([
            'EXE       =',
            'OBJ       = .o',
            'MAKE      = make',
            'CAT       = cat',
            'LN        = ln',
            'MKDIR     = mkdir',
            'MV        = mv',
            'CP        = cp',
            'CFLAGS    = %s' % ' '.join(cflags),
            'LEX       = %s -Pscotchyy -olex.yy.c' % flex_path,
            'YACC      = %s -pscotchyy -y -b y' % bison_path,
            'prefix    = %s' % self.prefix
        ])

        with working_dir('src'):
            with open('Makefile.inc', 'w') as fh:
                fh.write('\n'.join(makefile_inc))

    def install(self, spec, prefix):
        targets = ['scotch']
        if '+mpi' in self.spec:
            targets.append('ptscotch')

        if self.spec.version >= Version('6.0.0'):
            if '+esmumps' in self.spec:
                targets.append('esmumps')
                if '+mpi' in self.spec:
                    targets.append('ptesmumps')

        with working_dir('src'):
            for target in targets:
                # It seams that building ptesmumps in parallel fails, for
                # version prior to 6.0.0 there is no separated targets force
                # ptesmumps, this library is built by the ptscotch target. This
                # should explain the test for the can_make_parallel variable
                can_make_parallel = \
                    not (target == 'ptesmumps' or
                         (self.spec.version < Version('6.0.0') and
                          target == 'ptscotch'))
                make(target, parallel=can_make_parallel)

        lib_ext = dso_suffix if '+shared' in self.spec else 'a'
        # It seams easier to remove metis wrappers from the folder that will be
        # installed than to tweak the Makefiles
        if '+metis' not in self.spec:
            with working_dir('lib'):
                force_remove('libscotchmetis.{0}'.format(lib_ext))
                force_remove('libptscotchparmetis.{0}'.format(lib_ext))

            with working_dir('include'):
                force_remove('metis.h')
                force_remove('parmetis.h')

        if '~esmumps' in self.spec and self.spec.version < Version('6.0.0'):
            with working_dir('lib'):
                force_remove('libesmumps.{0}'.format(lib_ext))
                force_remove('libptesmumps.{0}'.format(lib_ext))

            with working_dir('include'):
                force_remove('esmumps.h')

        install_tree('bin', prefix.bin)
        install_tree('lib', prefix.lib)
        install_tree('include', prefix.include)
        install_tree('man/man1', prefix.share.man.man1)
