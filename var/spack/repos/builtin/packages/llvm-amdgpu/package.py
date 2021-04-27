# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class LlvmAmdgpu(CMakePackage):
    """Toolkit for the construction of highly optimized compilers,
       optimizers, and run-time environments."""

    homepage = "https://github.com/RadeonOpenCompute/llvm-project"
    git      = "https://github.com/RadeonOpenCompute/llvm-project.git"
    url      = "https://github.com/RadeonOpenCompute/llvm-project/archive/rocm-4.1.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('master', branch='amd-stg-open')
    version('4.1.0', sha256='244e38d824fa7dfa8d0edf3c036b3c84e9c17a16791828e4b745a8d31eb374ae')
    version('4.0.0', sha256='aa1f80f429fded465e86bcfaef72255da1af1c5c52d58a4c979bc2f6c2da5a69')
    version('3.10.0', sha256='8262aff88c1ff6c4deb4da5a4f8cda1bf90668950e2b911f93f73edaee53b370')
    version('3.9.0', sha256='1ff14b56d10c2c44d36c3c412b190d3d8cd1bb12cfc7cd58af004c16fd9987d1')
    version('3.8.0', sha256='93a28464a4d0c1c9f4ba55e473e5d1cde4c5c0e6d087ec8a0a3aef1f5f5208e8')
    version('3.7.0', sha256='3e2542ce54b91b5c841f33d542143e0e43eae95e8785731405af29f08ace725b')
    version('3.5.0', sha256='4878fa85473b24d88edcc89938441edc85d2e8a785e567b7bd7ce274ecc2fd9c')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    variant('openmp', default=True, description='Enable OpenMP')

    depends_on('cmake@3.4.3:',  type='build', when='@:3.8.99')
    depends_on('cmake@3.13.4:', type='build', when='@3.9.0:')
    depends_on('python', type='build')
    depends_on('z3', type='link')
    depends_on('zlib', type='link')
    depends_on('ncurses+termlib', type='link')
    # openmp dependencies
    depends_on("perl-data-dumper", type=("build"), when='+openmp')
    depends_on("hwloc", when='+openmp')
    depends_on('libelf', type='link', when='+openmp')

    # Will likely only be fixed in LLVM 12 upstream
    patch('fix-system-zlib-ncurses.patch', when='@3.5.0:3.8.0')
    patch('fix-ncurses-3.9.0.patch', when='@3.9.0:4.0.0')

    conflicts('^cmake@3.19.0')

    root_cmakelists_dir = 'llvm'

    install_targets = ['clang-tidy', 'install']

    def cmake_args(self):
        llvm_projects = [
            'clang',
            'lld',
            'clang-tools-extra',
            'compiler-rt'
        ]

        if '+openmp' in self.spec:
            llvm_projects.append('openmp')

        args = [
            '-DLLVM_ENABLE_PROJECTS={0}'.format(';'.join(llvm_projects)),
            '-DLLVM_ENABLE_ASSERTIONS=1'
        ]

        if self.compiler.name == "gcc":
            compiler = Executable(self.compiler.cc)
            gcc_output = compiler('-print-search-dirs', output=str, error=str)

            gcc_prefix = ""
            for line in gcc_output.splitlines():
                if line.startswith("install:"):
                    # Get path and strip any whitespace
                    # (causes oddity with ancestor)
                    gcc_prefix = line.split(":")[1].strip()
                    gcc_prefix = ancestor(gcc_prefix, 4)
                    break
            args.append("-DGCC_INSTALL_PREFIX=" + gcc_prefix)

        return args
