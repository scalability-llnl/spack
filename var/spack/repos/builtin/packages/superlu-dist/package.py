# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import glob

class SuperluDist(Package):
    """A general purpose library for the direct solution of large, sparse,
    nonsymmetric systems of linear equations on high performance machines."""

    homepage = "http://crd-legacy.lbl.gov/~xiaoye/SuperLU/"
    url      = "https://github.com/xiaoyeli/superlu_dist/archive/v6.0.0.tar.gz"
    git      = "https://github.com/xiaoyeli/superlu_dist.git"

    maintainers = ['xiaoye', 'gchavez2', 'balay']

    version('develop', branch='master')
    version('xsdk-0.2.0', tag='xsdk-0.2.0')
    version('6.1.1', '35d25cff592c724439870444ed45e1d1d15ca2c65f02ccd4b83a6d3c9d220bd1')
    version('6.1.0', '92c6d1424dd830ee2d1e7396a418a5f6645160aea8472e558c4e4bfe006593c4')
    version('6.0.0', 'ff6cdfa0263d595708bbb6d11fb780915d8cfddab438db651e246ea292f37ee4')
    version('5.4.0', '3ac238fe082106a2c4dbaf0c22af1ff1247308ffa8f053de9d78c3ec7dd0d801')
    version('5.3.0', '49ed110bdef1e284a0181d6c7dd1fae3aa110cb45f67c6aa5cb791070304d670')
    version('5.2.2', '65cfb9ace9a81f7affac4ad92b9571badf0f10155b3468531b0fffde3bd8e727')
    version('5.2.1', '67cf3c46cbded4cee68e2a9d601c30ab13b08091c8cdad95b0a8e018b6d5d1f1')
    version('5.1.3', '58e3dfdb4ae6f8e3f6f3d5ee5e851af59b967c4483cdb3b15ccd1dbdf38f44f9')
    version('5.1.2', 'e34865ad6696ee6a6d178b4a01c8e19103a7d241ba9de043603970d63b0ee1e2')
    version('5.1.0', '73f292ab748b590b6dd7469e6986aeb95d279b8b8b3da511c695a396bdbc996c')
    version('5.0.0', '78d1d6460ff16b3f71e4bcd7306397574d54d421249553ccc26567f00a10bfc6')
    version('4.3', 'ee66c84e37b4f7cc557771ccc3dc43ae',
        url='https://portal.nersc.gov/project/sparse/superlu/superlu_dist_4.3.tar.gz')
    version('4.2', 'ae9fafae161f775fbac6eba11e530a65',
        url='https://portal.nersc.gov/project/sparse/superlu/superlu_dist_4.2.tar.gz')
    version('4.1', '4edee38cc29f687bd0c8eb361096a455',
        url='https://portal.nersc.gov/project/sparse/superlu/superlu_dist_4.1.tar.gz')
    version('4.0', 'c0b98b611df227ae050bc1635c6940e0',
        url='https://portal.nersc.gov/project/sparse/superlu/superlu_dist_4.0.tar.gz')
    version('3.3', 'f4805659157d93a962500902c219046b',
        url='https://portal.nersc.gov/project/sparse/superlu/superlu_dist_3.3.tar.gz')

    variant('int64', default=False, description='Build with 64 bit integers')
    variant('shared', default=True, description='Build shared libraries')  # Should only be for version 5 and greater

    depends_on('mpi')
    depends_on('blas')
    depends_on('lapack')
    depends_on('parmetis')
    depends_on('metis@5:')

    def install(self, spec, prefix):

        if self.version >= Version('5.0.0'):
            sub = SuperluDist_CMake(spec)
        else:
            sub = SuperluDist_Legacy(spec)

        # See lib/spack/spack/directives.py
        sub.versions = self.versions
        sub.name = self.name
        sub.dependencies = self.dependencies
        sub.conflicts = self.conflicts
        sub.extendees = self.extendees
        sub.provided = self.provided
        # sub.pkg = self.pkg    # ???
        sub.variants = self.variants
        sub.resources = self.resources

#        sub.patches = self.patches
#        sub.conditions = self.conditions
#        sub.cur_patches = self.cur_patches

        # See similar code in lib/spack/spack/package.py
        for phase_name, phase_attr in zip(
            sub.phases, sub._InstallPhase_phases):

            #with logger.force_echo():
            #    tty.msg(
            #        "Executing phase: '%s'" % phase_name)

            # Redirect stdout and stderr to daemon pipe
            phase = getattr(sub, phase_attr)
            phase(sub.spec, sub.prefix)




class SuperluDist_CMake(CMakePackage):

    def cmake_args(self):
        spec = self.spec
        args = [
            '-DCMAKE_C_COMPILER=%s' % spec['mpi'].mpicc,
            '-DCMAKE_CXX_COMPILER=%s' % spec['mpi'].mpicxx,
            '-DCMAKE_INSTALL_LIBDIR:STRING=%s' % self.prefix.lib,
            '-DTPL_BLAS_LIBRARIES=%s' % spec['blas'].libs.joined(";"),
            '-DTPL_LAPACK_LIBRARIES=%s' % spec['lapack'].libs.joined(";"),
            '-DUSE_XSDK_DEFAULTS=YES',
            '-DTPL_PARMETIS_LIBRARIES=%s' % spec['parmetis'].libs.ld_flags +
            ';' + spec['metis'].libs.ld_flags,
            '-DTPL_PARMETIS_INCLUDE_DIRS=%s' % spec['parmetis'].prefix.include
        ]

        if '+int64' in spec:
            args.append('-DXSDK_INDEX_SIZE=64')
        else:
            args.append('-DXSDK_INDEX_SIZE=32')

        if '+shared' in spec:
            args.append('-DBUILD_SHARED_LIBS:BOOL=ON')
        else:
            args.append('-DBUILD_SHARED_LIBS:BOOL=OFF')
        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == 'cxxflags':
            flags.append(self.compiler.cxx11_flag)
        if name == 'cflags' and '%pgi' not in self.spec:
            flags.append('-std=c99')
        return (None, None, flags)

class SuperluDist_Legacy(Package):

    def install(self, spec, prefix):
        lapack_blas = spec['lapack'].libs + spec['blas'].libs
        makefile_inc = []
        makefile_inc.extend([
            'PLAT         = _mac_x',
            'DSuperLUroot = %s' % self.stage.source_path,
            'DSUPERLULIB  = $(DSuperLUroot)/lib/libsuperlu_dist.a',
            'BLASDEF      = -DUSE_VENDOR_BLAS',
            'BLASLIB      = %s' % lapack_blas.ld_flags,
            'METISLIB     = %s' % spec['metis'].libs.ld_flags,
            'PARMETISLIB  = %s' % spec['parmetis'].libs.ld_flags,
            'HAVE_PARMETIS= TRUE',
            'FLIBS        =',
            'LIBS         = $(DSUPERLULIB) $(BLASLIB) $(PARMETISLIB) $(METISLIB)',  # noqa
            'ARCH         = ar',
            'ARCHFLAGS    = cr',
            'RANLIB       = true',
            'CXX          = {0}'.format(self.spec['mpi'].mpicxx),
            'CXXFLAGS     = {0} {1} {2}'.format(
                ' '.join(self.spec.compiler_flags['cxxflags']),
                self.compiler.pic_flag,
                self.compiler.cxx11_flag),
            'CC           = {0}'.format(self.spec['mpi'].mpicc),
            'CFLAGS       = %s %s -O2 %s %s %s' % (
                self.compiler.pic_flag,
                '' if '%pgi' in spec else '-std=c99',
                spec['parmetis'].headers.cpp_flags,
                spec['metis'].headers.cpp_flags,
                '-D_LONGINT' if '+int64' in spec and not
                self.spec.satisfies('@5.2.0:') else ''),
            'XSDK_INDEX_SIZE = %s' % ('64' if '+int64' in spec else '32'),
            'NOOPTS       = %s -std=c99' % (
                self.compiler.pic_flag),
            'FORTRAN      = {0}'.format(self.spec['mpi'].mpif77),
            'F90FLAGS     = -O2',
            'LOADER       = {0}'.format(self.spec['mpi'].mpif77),
            'INCLUDEDIR   = $(SuperLUroot)/include',
            'LOADOPTS     =',
            'CDEFS        = %s' % ("-DNoChange"
                                       if spack_f77.endswith('xlf') or
                                          spack_f77.endswith('xlf_r')
                                       else "-DAdd_")
        ])

        with open('make.inc', 'w') as fh:
            fh.write('\n'.join(makefile_inc))

        mkdirp(os.path.join(self.stage.source_path, 'lib'))
        make("lib", parallel=False)

        # FIXME:
        # cd "EXAMPLE" do
        # system "make"

        # need to install by hand
        headers_location = self.prefix.include
        mkdirp(headers_location)
        mkdirp(prefix.lib)

        headers = glob.glob(join_path(self.stage.source_path, 'SRC', '*.h'))
        for h in headers:
            install(h, headers_location)

        superludist_lib = join_path(self.stage.source_path,
                                    'lib/libsuperlu_dist.a')
        install(superludist_lib, self.prefix.lib)
