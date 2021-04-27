# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import re

tools_url = 'https://github.com/ROCm-Developer-Tools'
compute_url = 'https://github.com/RadeonOpenCompute'

# Arrays of hashes are in order of the versions array below
# For example array[0] = 3.9.0, array[1] = 3.10.0, etc.

aomp = [
    "377ab59b685a73b3f95fba95f5e028678ec5aafabc4177b7f0ffb78da095d679",
    "808fca9bdefb109d5bcbbc9f5b59c564a6d422488869e986516f2a7233eda235",
    "aa75455cf1d333419e5310117678e5789c5222f7cb05b05e3dfacef855c55d84",
    "9e6ed2c7bdc3b4af069751b5d3e92913fd5ac318ae844f68bd78c5def990a8f7"
]

devlib = [
    "c99f45dacf5967aef9a31e3731011b9c142446d4a12bac69774998976f2576d7",
    "bca9291385d6bdc91a8b39a46f0fd816157d38abb1725ff5222e6a0daa0834cc",
    "d0aa495f9b63f6d8cf8ac668f4dc61831d996e9ae3f15280052a37b9d7670d2a",
    "f5f5aa6bfbd83ff80a968fa332f80220256447c4ccb71c36f1fbd2b4a8e9fc1b"
]

llvm = [
    "1ff14b56d10c2c44d36c3c412b190d3d8cd1bb12cfc7cd58af004c16fd9987d1",
    "8262aff88c1ff6c4deb4da5a4f8cda1bf90668950e2b911f93f73edaee53b370",
    "aa1f80f429fded465e86bcfaef72255da1af1c5c52d58a4c979bc2f6c2da5a69",
    "244e38d824fa7dfa8d0edf3c036b3c84e9c17a16791828e4b745a8d31eb374ae"
]

flang = [
    "5d113f44fb173bd0d5704b282c5cebbb2aa642c7c29f188764bfa1daa58374c9",
    "3990d39ff1c908b150f464f0653a123d94be30802f9cad6af18fbb560c4b412e",
    "f3e19699ce4ac404f41ffe08ef4546e31e2e741d8deb403b5477659e054275d5",
    "f41f661425534b5cfb20e2c0efd9d0800609dc3876ee9c3f76f026d36abbfa35"
]

extras = [
    "830a37cf1c6700f81fc00749206a37e7cda4d2867bbdf489e9e2d81f52d06b3d",
    "5d98d34aff97416d8b5b9e16e7cf474580f8de8a73bd0e549c4440a3c5df4ef5",
    "51cc8a7c5943e1d9bc657fc9b9797f45e3ce6a4e544d3d3a967c7cd0185a0510",
    "91fdfadb94aa6afc1942124d0953ddc80c297fa75de1897fb42ac8e7dea51ab9"
]

versions = ['3.9.0', '3.10.0', '4.0.0', '4.1.0']
versions_dict = dict()
components = ['aomp', 'devlib', 'llvm', 'flang', 'extras']
component_hashes = [aomp, devlib, llvm, flang, extras]

# Loop through versions and create necessary dictionaries of components
for outer_index, item in enumerate(versions):
    for inner_index, component in enumerate(component_hashes):
        versions_dict.setdefault(item, {})[components[inner_index]] = \
            component_hashes[inner_index][outer_index]


class RocmOpenmpExtras(Package):
    """OpenMP support for ROCm LLVM."""

    homepage = tools_url + "/aomp"
    url = tools_url + "/aomp/archive/rocm-4.1.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'estewart08']
    version('4.1.0', sha256=versions_dict['4.1.0']['aomp'])
    version('4.0.0', sha256=versions_dict['4.0.0']['aomp'])
    version('3.10.0', sha256=versions_dict['3.10.0']['aomp'])
    version('3.9.0', sha256=versions_dict['3.9.0']['aomp'])

    depends_on('cmake@3:', type='build')
    depends_on('mesa18~llvm@18.3:', type=('build', 'link'))
    depends_on('py-setuptools', type='build')
    depends_on('python@3:', type='build')
    depends_on('perl-data-dumper', type='build')
    depends_on('awk', type='build')
    depends_on('elfutils', type=('build', 'link'))
    depends_on('libffi', type=('build', 'link'))

    for ver in ['3.9.0', '3.10.0', '4.0.0', '4.1.0']:
        depends_on('hsakmt-roct@' + ver, type=('build', 'run'), when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type=('build', 'run'),
                   when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type=('build', 'run'),
                   when='@' + ver)
        depends_on('llvm-amdgpu@' + ver + ' ~openmp', type=('build', 'run'),
                   when='@' + ver)

        # tag changed to 'rocm-' in 4.0.0
        if ver == '3.9.0' or ver == '3.10.0':
            tag = 'rocm-uc-'
        else:
            tag = 'rocm-'

        resource(
            name='rocm-device-libs',
            url=compute_url +
            '/ROCm-Device-Libs/archive/' + tag + ver + '.tar.gz',
            sha256=versions_dict[ver]['devlib'],
            expand=True,
            destination='rocm-openmp-extras',
            placement='rocm-device-libs',
            when='@' + ver)

        resource(
            name='flang',
            url=tools_url + '/flang/archive/' + tag + ver + '.tar.gz',
            sha256=versions_dict[ver]['flang'],
            expand=True,
            destination='rocm-openmp-extras',
            placement='flang',
            when='@' + ver)

        resource(
            name='aomp-extras',
            url=tools_url + '/aomp-extras/archive/' + tag + ver + '.tar.gz',
            sha256=versions_dict[ver]['extras'],
            expand=True,
            destination='rocm-openmp-extras',
            placement='aomp-extras',
            when='@' + ver)

        resource(
            name='llvm-project',
            url=compute_url + '/llvm-project/archive/rocm-' + ver + '.tar.gz',
            sha256=versions_dict[ver]['llvm'],
            expand=True,
            destination='rocm-openmp-extras',
            placement='llvm-project',
            when='@' + ver)

    def setup_run_environment(self, env):
        devlibs_prefix = self.spec['rocm-device-libs'].prefix
        openmp_extras_prefix = self.spec['rocm-openmp-extras'].prefix
        llvm_prefix = self.spec['llvm-amdgpu'].prefix
        env.set('AOMP', '{0}'.format(llvm_prefix))
        env.set('HIP_DEVICE_LIB_PATH',
                '{0}/amdgcn/bitcode'.format(devlibs_prefix))
        env.prepend_path('CPATH',
                         '{0}/include'.format(openmp_extras_prefix))
        env.prepend_path('LIBRARY_PATH',
                         '{0}/lib'.format(openmp_extras_prefix))
        if self.spec.version < Version('4.1.0'):
            env.set('AOMP_GPU',
                    '`{0}/rocm-bin/mygpu`'.format(openmp_extras_prefix))
        else:
            env.set('AOMP_GPU',
                    '`{0}/bin/mygpu`'.format(openmp_extras_prefix))

    def setup_build_environment(self, env):
        openmp_extras_prefix = self.spec['rocm-openmp-extras'].prefix
        llvm_prefix = self.spec['llvm-amdgpu'].prefix
        env.set('AOMP', '{0}'.format(llvm_prefix))
        env.set('FC', '{0}/bin/flang'.format(openmp_extras_prefix))
        env.set(
            'GFXLIST',
            'gfx700 gfx701 gfx801 gfx803 gfx900 gfx902 gfx906 gfx908')

    def patch(self):
        src = self.stage.source_path
        flang_warning = '-Wno-incompatible-pointer-types-discards-qualifiers)'
        aomp_extras = '{0}/rocm-openmp-extras/aomp-extras/aomp-device-libs'
        libomptarget = \
            '{0}/rocm-openmp-extras/llvm-project/openmp/libomptarget'
        flang = '{0}/rocm-openmp-extras/flang/'

        if self.spec.version < Version('4.1.0'):
            plugin = '/plugins/hsa/CMakeLists.txt'
        else:
            # Spack thinks some warnings from the flang build are errors.
            # Disable those warnings.
            filter_file('PRIVATE -fPIC)',
                        'PRIVATE -fPIC PRIVATE ' + flang_warning,
                        flang.format(src) + 'runtime/flang/CMakeLists.txt',
                        string=True)
            plugin = '/plugins/amdgpu/CMakeLists.txt'
        filter_file(
            '{ROCM_DIR}/amdgcn/bitcode', '{DEVICE_LIBS_DIR}',
            aomp_extras.format(src) + '/aompextras/CMakeLists.txt',
            aomp_extras.format(src) + '/libm/CMakeLists.txt',
            libomptarget.format(src) + '/deviceRTLs/amdgcn/CMakeLists.txt')

        # Openmp adjustments
        filter_file(
            '-nogpulib', '-nogpulib -nogpuinc',
            libomptarget.format(src) + '/deviceRTLs/amdgcn/CMakeLists.txt')

        filter_file(
            '-x hip', '-x hip -nogpulib -nogpuinc',
            libomptarget.format(src) + '/deviceRTLs/amdgcn/CMakeLists.txt')

        filter_file(
            '-c ', '-c -nogpulib -nogpuinc -I{LIMIT}',
            libomptarget.format(src) + '/hostrpc/CMakeLists.txt')

        filter_file(
            r'${ROCM_DIR}/hsa/include ${ROCM_DIR}/hsa/include/hsa',
            '${HSA_INCLUDE}/hsa/include ${HSA_INCLUDE}/hsa/include/hsa',
            libomptarget.format(src) + plugin,
            string=True)

        filter_file(
            '{ROCM_DIR}/hsa/lib', '{HSA_LIB}',
            libomptarget.format(src) + plugin)

        filter_file(
            r'{ROCM_DIR}/lib\)',
            '{HSAKMT_LIB})\nset(HSAKMT_LIB64 ${HSAKMT_LIB64})',
            libomptarget.format(src) + plugin)

        filter_file(
            r'-L${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}',
            '-L${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS} -L${HSAKMT_LIB64}',
            libomptarget.format(src) + plugin,
            string=True)

        filter_file(
            r'-rpath,${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}',
            '-rpath,${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}' +
            ',-rpath,${HSAKMT_LIB64}',
            libomptarget.format(src) + plugin,
            string=True)

        filter_file(
            '{ROCM_DIR}/include', '{COMGR_INCLUDE}',
            libomptarget.format(src) + plugin)

        filter_file(
            r'-L${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX}',
            '-L${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX} -L${COMGR_LIB}',
            libomptarget.format(src) + plugin,
            string=True)

        filter_file(
            r'rpath,${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX}',
            'rpath,${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX}' +
            '-Wl,-rpath,${COMGR_LIB}',
            libomptarget.format(src) + plugin,
            string=True)

        filter_file(
            'ADDITIONAL_VERSIONS 2.7', 'ADDITIONAL_VERSIONS 3',
            flang.format(src) + 'CMakeLists.txt')

    def install(self, spec, prefix):
        src = self.stage.source_path
        gfx_list = "gfx700;gfx701;gfx801;gfx803;gfx900;gfx902;gfx906;gfx908"
        openmp_extras_prefix = self.spec['rocm-openmp-extras'].prefix
        devlibs_prefix = self.spec['rocm-device-libs'].prefix
        devlibs_src = '{0}/rocm-openmp-extras/rocm-device-libs'.format(src)
        hsa_prefix = self.spec['hsa-rocr-dev'].prefix
        hsakmt_prefix = self.spec['hsakmt-roct'].prefix
        comgr_prefix = self.spec['comgr'].prefix
        llvm_inc = '/rocm-openmp-extras/llvm-project/llvm/include'
        llvm_prefix = self.spec['llvm-amdgpu'].prefix
        omp_bin_dir = '{0}/bin'.format(openmp_extras_prefix)
        omp_lib_dir = '{0}/lib'.format(openmp_extras_prefix)
        bin_dir = '{0}/bin'.format(llvm_prefix)
        lib_dir = '{0}/lib'.format(llvm_prefix)

        # flang1 and flang2 symlink needed for build of flang-runtime
        # libdevice symlink to rocm-openmp-extras for runtime
        # libdebug symlink to rocm-openmp-extras for runtime
        if not (os.path.islink((os.path.join(bin_dir, 'flang1')))):
            os.symlink(os.path.join(omp_bin_dir, 'flang1'),
                       os.path.join(bin_dir, 'flang1'))
        if not (os.path.islink((os.path.join(bin_dir, 'flang2')))):
            os.symlink(os.path.join(omp_bin_dir, 'flang2'),
                       os.path.join(bin_dir, 'flang2'))
        if not (os.path.islink((os.path.join(lib_dir, 'libdevice')))):
            os.symlink(os.path.join(omp_lib_dir, 'libdevice'),
                       os.path.join(lib_dir, 'libdevice'))
        if not (os.path.islink((os.path.join(llvm_prefix, 'lib-debug')))):
            os.symlink(os.path.join(openmp_extras_prefix, 'lib-debug'),
                       os.path.join(llvm_prefix, 'lib-debug'))

        # Set cmake args
        components = dict()

        components['aomp-extras'] = [
            '../rocm-openmp-extras/aomp-extras',
            '-DLLVM_DIR={0}'.format(llvm_prefix),
            '-DDEVICE_LIBS_DIR={0}/amdgcn/bitcode'.format(devlibs_prefix),
            '-DAOMP_STANDALONE_BUILD=0',
            '-DDEVICELIBS_ROOT={0}'.format(devlibs_src),
            '-DNEW_BC_PATH=1',
            '-DAOMP={0}'.format(llvm_prefix)
        ]

        # Shared cmake configuration for openmp, openmp-debug
        openmp_common_args = [
            '-DROCM_DIR={0}'.format(hsa_prefix),
            '-DDEVICE_LIBS_DIR={0}/amdgcn/bitcode'.format(devlibs_prefix),
            '-DAOMP_STANDALONE_BUILD=0',
            '-DDEVICELIBS_ROOT={0}'.format(devlibs_src),
            '-DOPENMP_TEST_C_COMPILER={0}/clang'.format(bin_dir),
            '-DOPENMP_TEST_CXX_COMPILER={0}/clang++'.format(bin_dir),
            '-DLIBOMPTARGET_AMDGCN_GFXLIST={0}'.format(gfx_list),
            '-DLIBOMP_COPY_EXPORTS=OFF',
            '-DHSA_LIB={0}/lib'.format(hsa_prefix),
            '-DHSAKMT_LIB={0}/lib'.format(hsakmt_prefix),
            '-DHSAKMT_LIB64={0}/lib64'.format(hsakmt_prefix),
            '-DCOMGR_INCLUDE={0}/include'.format(comgr_prefix),
            '-DCOMGR_LIB={0}/lib'.format(comgr_prefix),
            '-DOPENMP_ENABLE_LIBOMPTARGET=1',
            '-DOPENMP_ENABLE_LIBOMPTARGET_HSA=1',
            '-DLLVM_MAIN_INCLUDE_DIR={0}{1}'.format(src, llvm_inc),
            '-DLLVM_INSTALL_PREFIX={0}'.format(llvm_prefix)
        ]

        if self.spec.version < Version('4.1.0'):
            openmp_common_args += [
                '-DHSA_INCLUDE={0}'.format(hsa_prefix)
            ]
        else:
            openmp_common_args += [
                '-DHSA_INCLUDE={0}/include/hsa'.format(hsa_prefix)
            ]

        components['openmp'] = ['../rocm-openmp-extras/llvm-project/openmp']
        components['openmp'] += openmp_common_args

        components['openmp-debug'] = [
            '../rocm-openmp-extras/llvm-project/openmp',
            '-DLIBOMPTARGET_NVPTX_DEBUG=ON',
            '-DCMAKE_CXX_FLAGS=-g',
            '-DCMAKE_C_FLAGS=-g'
        ]

        components['openmp-debug'] += openmp_common_args

        # Shared cmake configuration for pgmath, flang, flang-runtime
        flang_common_args = [
            '-DLLVM_ENABLE_ASSERTIONS=ON',
            '-DLLVM_CONFIG={0}/llvm-config'.format(bin_dir),
            '-DCMAKE_CXX_COMPILER={0}/clang++'.format(bin_dir),
            '-DCMAKE_C_COMPILER={0}/clang'.format(bin_dir),
            '-DCMAKE_Fortran_COMPILER={0}/flang'.format(bin_dir),
            '-DLLVM_TARGETS_TO_BUILD=AMDGPU;x86'
        ]

        components['pgmath'] = [
            '../rocm-openmp-extras/flang/runtime/libpgmath'
        ]

        components['pgmath'] += flang_common_args

        components['flang'] = [
            '../rocm-openmp-extras/flang',
            '-DFLANG_OPENMP_GPU_AMD=ON',
            '-DFLANG_OPENMP_GPU_NVIDIA=ON'
        ]

        components['flang'] += flang_common_args

        components['flang-runtime'] = [
            '../rocm-openmp-extras/flang',
            '-DLLVM_INSTALL_RUNTIME=ON',
            '-DFLANG_BUILD_RUNTIME=ON',
            '-DOPENMP_BUILD_DIR={0}/spack-build-openmp/runtime/src'.format(src)
        ]
        components['flang-runtime'] += flang_common_args

        build_order = [
            "aomp-extras", "openmp", "openmp-debug", "pgmath",
            "flang", "flang-runtime"
        ]

        # Override standard CMAKE_BUILD_TYPE
        for arg in std_cmake_args:
            found = re.search("CMAKE_BUILD_TYPE", arg)
            if found:
                std_cmake_args.remove(arg)
        for component in build_order:
            with working_dir('spack-build-{0}'.format(component), create=True):
                cmake_args = components[component]
                cmake_args.extend(std_cmake_args)
                # OpenMP build needs to be run twice(Release, Debug)
                if component == "openmp-debug":
                    cmake_args.append("-DCMAKE_BUILD_TYPE=Debug")
                else:
                    cmake_args.append("-DCMAKE_BUILD_TYPE=Release")
                cmake(*cmake_args)
                make()
                make("install")
