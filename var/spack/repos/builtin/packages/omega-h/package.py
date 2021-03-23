# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class OmegaH(CMakePackage):
    """Omega_h is a C++11 library providing data structures and algorithms
    for adaptive discretizations. Its specialty is anisotropic triangle and
    tetrahedral mesh adaptation. It runs efficiently on most modern HPC
    hardware including GPUs.
    """

    homepage = "https://github.com/SNLComputation/omega_h"
    url      = "https://github.com/SNLComputation/omega_h/archive/v9.29.0.tar.gz"
    git      = "https://github.com/SNLComputation/omega_h.git"

    maintainers = ['ibaned']

    version('main', branch='main')
    version('9.32.5', sha256='963a203e9117024cd48d829d82b8543cd9133477fdc15386113b594fdc3246d8')
    version('9.29.0', sha256='b41964b018909ffe9cea91c23a0509b259bfbcf56874fcdf6bd9f6a179938014')
    version('9.27.0', sha256='aa51f83508cbd14a41ae953bda7da98a6ad2979465c76e5b3a3d9a7a651cb34a')
    version('9.22.2', sha256='ab5636be9dc171a514a7015df472bd85ab86fa257806b41696170842eabea37d')
    version('9.19.1', sha256='60ef65c2957ce03ef9d1b995d842fb65c32c5659d064de002c071effe66b1b1f')
    version('9.19.0', sha256='4a1606c4e7287a1b67359cf6ef1c2d7e24b7dc379065566a1d2e0b0330c0abbd')
    version('9.15.0', sha256='342a506a0ff22f6cac759862efdcf34e360110f7901eb9b4c5de8afe38741522')
    version('9.14.0', sha256='035d0f47142f965a57818d1cb6c5c00b5ae6b5a0178b67b0bc9177fa99ba083d')
    version('9.13.14', sha256='f617dfd024c9cc323e56800ca23df3386bfa37e1b9bd378847d1f5d32d2b8e5d')
    version('9.13.13', sha256='753702edf4bda9ae57ea21f09ca071e341604a468d8c86468c9aebba049f581c')

    variant('shared', default=True, description='Build shared libraries')
    variant('mpi', default=True, description='Activates MPI support')
    variant('zlib', default=True, description='Activates ZLib support')
    variant('trilinos', default=True, description='Use Teuchos and Kokkos')
    variant('throw', default=False, description='Errors throw exceptions instead of abort')
    variant('examples', default=False, description='Compile examples')
    variant('optimize', default=True, description='Compile C++ with optimization')
    variant('symbols', default=True, description='Compile C++ with debug symbols')
    variant('warnings', default=False, description='Compile C++ with warnings')

    depends_on('gmsh', when='+examples', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('trilinos +kokkos +teuchos', when='+trilinos')
    depends_on('zlib', when='+zlib')

    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=86610
    conflicts('%gcc@8:8.2.99', when='@:9.22.1')

    def _bob_options(self):
        cmake_var_prefix = 'Omega_h_CXX_'
        for variant in ['optimize', 'symbols', 'warnings']:
            cmake_var = cmake_var_prefix + variant.upper()
            if '+' + variant in self.spec:
                yield '-D' + cmake_var + ':BOOL=ON'
            else:
                yield '-D' + cmake_var + ':BOOL=FALSE'

    def cmake_args(self):
        args = ['-DUSE_XSDK_DEFAULTS:BOOL=OFF']
        if '+shared' in self.spec:
            args.append('-DBUILD_SHARED_LIBS:BOOL=ON')
        else:
            args.append('-DBUILD_SHARED_LIBS:BOOL=OFF')
        if '+mpi' in self.spec:
            args.append('-DOmega_h_USE_MPI:BOOL=ON')
            args.append('-DCMAKE_CXX_COMPILER:FILEPATH={0}'.format(
                self.spec['mpi'].mpicxx))
        else:
            args.append('-DOmega_h_USE_MPI:BOOL=OFF')
        if '+trilinos' in self.spec:
            args.append('-DOmega_h_USE_Trilinos:BOOL=ON')
        if '+zlib' in self.spec:
            args.append('-DOmega_h_USE_ZLIB:BOOL=ON')
            args.append('-DZLIB_ROOT:PATH={0}'.format(
                self.spec['zlib'].prefix))
        else:
            args.append('-DOmega_h_USE_ZLIB:BOOL=OFF')
        if '+examples' in self.spec:
            args.append('-DOmega_h_EXAMPLES:BOOL=ON')
        else:
            args.append('-DOmega_h_EXAMPLES:BOOL=OFF')
        if '+throw' in self.spec:
            args.append('-DOmega_h_THROW:BOOL=ON')
        else:
            args.append('-DOmega_h_THROW:BOOL=OFF')
        # omega-h requires empty CMAKE_BUILD_TYPE
        args.append('-DCMAKE_BUILD_TYPE:STRING=')
        args += list(self._bob_options())
        return args

    def flag_handler(self, name, flags):
        flags = list(flags)
        if name == 'cxxflags':
            flags.append(self.compiler.cxx11_flag)
        return (None, None, flags)
