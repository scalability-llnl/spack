# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.pkgkit import *


class Legion(CMakePackage):
    """Legion is a data-centric parallel programming system for writing
       portable high performance programs targeted at distributed heterogeneous
       architectures. Legion presents abstractions which allow programmers to
       describe properties of program data (e.g. independence, locality). By
       making the Legion programming system aware of the structure of program
       data, it can automate many of the tedious tasks programmers currently
       face, including correctly extracting task- and data-level parallelism
       and moving data around complex memory hierarchies. A novel mapping
       interface provides explicit programmer controlled placement of data in
       the memory hierarchy and assignment of tasks to processors in a way
       that is orthogonal to correctness, thereby enabling easy porting and
       tuning of Legion applications to new architectures.
    """
    homepage = "http://legion.stanford.edu/"
    url      = "https://github.com/StanfordLegion/legion/tarball/legion-17.02.0"
    git      = "https://github.com/StanfordLegion/legion.git"

    maintainers = ['streichler']

    version('master', branch='master')
    version('ctrl-rep', branch='control_replication')
    version('20.03.0', sha256='ae5feedb5ed9f357b56424b9d73cea4f224a61e291e022556f796d1ff24d1244')
    version('19.12.0', sha256='ea517638de7256723bb9c119796d4d9d4ef662c52d0151ad24af5288e5a72e7d')
    version('19.09.1', sha256='c507133fb9dce16b7fcccd7eb2933d13cce96ecf835da60a27c0f66840cabf51')
    version('19.09.0', sha256='a01c3e3c6698cafb64b77a66341cc06d039faed4fa31b764159f021b94ce13e8')
    version('19.06.0', sha256='31cd97e9264c510ab83b1f9e8e1e6bf72021a0c6ee4a028966fce08736e39fbf')
    version('19.04.0', sha256='279bbc8dcdab4c75be570318989a9fc9821178143e9db9c3f62e58bf9070b5ac')
    version('18.12.0', sha256='71f2c409722975c0ad92f2caffcc9eaa9260f7035e2b55b731d819eb6a94016c')
    version('18.09.0', sha256='58c5a3072d2b5086225982563c23524692ca5758cbfda8d0f0a4f00ef17b3b8d')
    version('18.05.0', sha256='4c3cef548b3a459827e4c36b5963c06b6fcf0a4ca1800fbb0f73e6ba3b1cced4')
    version('18.02.0', sha256='e08aeef98003593391a56f11a99d9d65af49647fe87a2a5e8837c8682a337a60')
    version('17.10.0', sha256='af4f1e9215e57c4aac4805ae2bf53defe13eeaf192576bf5a702978f43171b1e')
    version('17.08.0', sha256='20aabdb0fabb1e32aa713cd5fa406525093f8dad33fca5d23046408d42d3c7b3')
    version('17.02.0', sha256='423d8699729b0e7fef663740e239aa722cca544f6bda8c9f782eaba4274bf60a')

    variant('mpi', default=True,
            description='Build on top of mpi conduit for mpi inoperability')
    variant('ibv', default=False,
            description='Build on top of ibv conduit for InfiniBand support')
    variant('shared', default=True, description='Build shared libraries')
    variant('hdf5', default=True, description='Enable HDF5 support')
    variant('spy', default=False,
            description='Enable detailed logging for Legion Spy')
    variant('build_type', default='Release',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'),
            description='The build type to build', multi=False)

    depends_on("cmake@3.1:", type='build')
    depends_on("gasnet~aligned-segments~pshm segment-mmap-max='16GB'", when='~mpi')
    depends_on("gasnet~aligned-segments~pshm segment-mmap-max='16GB' +mpi", when='+mpi')
    depends_on("gasnet~aligned-segments~pshm segment-mmap-max='16GB' +ibv", when='+ibv')
    depends_on("hdf5", when='+hdf5')

    def cmake_args(self):
        cmake_cxx_flags = [
            '-DPRIVILEGE_CHECKS',
            '-DBOUNDS_CHECKS',
            '-DENABLE_LEGION_TLS']

        options = [
            '-DLegion_USE_GASNet=ON',
            '-DLEGION_USE_CUDA=OFF',
            '-DLEGION_USE_OPENMP=OFF',
            '-DLegion_BUILD_EXAMPLES=ON',
            '-DBUILD_SHARED_LIBS=%s' % ('+shared' in self.spec)]

        if self.spec.variants['build_type'].value == 'Debug':
            cmake_cxx_flags.extend([
                '-DDEBUG_REALM',
                '-DDEBUG_LEGION',
                '-ggdb',
            ])

        options.append('-DCMAKE_CXX_FLAGS=%s' % (" ".join(cmake_cxx_flags)))

        if '+mpi' in self.spec:
            options.append('-DGASNet_CONDUIT=mpi')

        if '+hdf5' in self.spec:
            options.append('-DLegion_USE_HDF5=ON')
        else:
            options.append('-DLegion_USE_HDF5=OFF')

        if '+spy' in self.spec:
            options.append('-DLegion_SPY=ON')

        return options
