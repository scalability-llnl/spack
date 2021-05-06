# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class LlvmOpenmpOmpt(CMakePackage):
    """The OpenMP subproject provides an OpenMP runtime for use with the
       OpenMP implementation in Clang. This branch includes experimental
       changes for OMPT, the OpenMP Tools interface"""

    homepage = "https://github.com/OpenMPToolsInterface/LLVM-openmp"
    git      = "https://github.com/OpenMPToolsInterface/LLVM-openmp.git"

    # tr6_forwards branch
    version('tr6_forwards', branch='tr6_forwards')
    version('3.9.2b2', commit='5cdca5dd3c0c336d42a335ca7cff622e270c9d47')

    # align-to-tr-rebased branch
    version('3.9.2b', commit='982a08bcf3df9fb5afc04ac3bada47f19cc4e3d3')

    # variant for building llvm-openmp-ompt as a stand alone library
    variant('standalone', default=False,
            description="Build llvm openmpi ompt library as a \
                         stand alone entity.")
    # variant for building libomptarget
    variant('libomptarget', default=True,
            description='Enable building libomptarget for offloading')

    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    depends_on('cmake@2.8:', type='build')
    depends_on('llvm', when='~standalone')
    depends_on('ninja@1.5:', type='build')
    depends_on('perl@5.22.0:', type='build')
    depends_on('elf', when='+libomptarget')
    depends_on('libffi', when='+libomptarget')

    generator = 'Ninja'

    def cmake_args(self):
        cmake_args = [
            '-DLIBOMP_OMPT_SUPPORT=on',
            '-DLIBOMP_OMPT_BLAME=on',
            '-DLIBOMP_OMPT_TRACE=on',
            '-DCMAKE_C_COMPILER=%s' % spack_cc,
            '-DCMAKE_CXX_COMPILER=%s' % spack_cxx
        ]

        # Build llvm-openmp-ompt as a stand alone library
        # CMAKE rpath variable prevents standalone error
        # where this package wants the llvm tools path
        if '+standalone' in self.spec:
            cmake_args.extend(
                ['-DLIBOMP_STANDALONE_BUILD=true',
                 '-DCMAKE_BUILD_WITH_INSTALL_RPATH=true',
                 '-DLIBOMP_USE_DEBUGGER=false'])

        # Build llvm-openmp-ompt using the tr6_forwards branch
        # This requires the version to be 5.0 (50)
        if '@tr6_forwards' in self.spec:
            cmake_args.extend(
                ['-DLIBOMP_OMP_VERSION=50'])

        # Disable support for libomptarget
        if '~libomptarget' in self.spec:
            cmake_args.extend(
                ['-DOPENMP_ENABLE_LIBOMPTARGET=OFF'])

        return cmake_args

    @property
    def libs(self):
        return find_libraries('libomp', root=self.prefix, recursive=True)
