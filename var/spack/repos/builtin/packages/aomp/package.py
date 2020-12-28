# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


tools_url = 'https://github.com/ROCm-Developer-Tools'
compute_url = 'https://github.com/RadeonOpenCompute'

# 3.9 SHA Keys
aomp39 = dict()
aomp39 = {
    "aomp":
        "14fc6867af0b17e3bff8cb42cb36f509c95a29b7a933a106bf6778de21f6c123",
    "devlib":
        "c99f45dacf5967aef9a31e3731011b9c142446d4a12bac69774998976f2576d7",
    "llvm":
        "f0a0b9fec0626878340a15742e73a56f155090011716461edcb069dcf05e6b30",
    "flang":
        "43d57bcc87fab092ac242e36da62588a87b6fa91f9e81fdb330159497afdecb3",
    "extras":
        "014fca1fba54997c6db0e84822df274fb6807698b6856da4f737f38f10ab0e5d"

}

# 3.8 SHA Keys
aomp38 = dict()
aomp38 = {
    "aomp":
        "86f90d6505eccdb2840069cadf57f7111d4685653c4974cf65fb22b172e55478",
    "devlib":
        "e82cc9a8eb7d92de02cabb856583e28f17a05c8cf9c97aec5275608ef1a38574",
    "llvm":
        "98deabedb6cb3067ee960a643099631902507f236e4d9dc65b3e0f8d659eb55c",
    "flang":
        "54cc6a9706dba6d7808258632ed40fa6493838edb309709d3b25e0f9b02507f8",
    "extras":
        "4460a4f4b03022947f536221483e85dcd9b07064a54516ec103a1939c3f587b5"
}

# 3.7 SHA Keys
aomp37 = dict()
aomp37 = {
    "aomp":
        "970374c3acb9dda8b9a17d7a579dbaab48fac731db8fdce566a65abee37e5ed3",
    "devlib":
        "b3a114180bf184b3b829c356067bc6a98021d52c1c6f9db6bc57272ebafc5f1d",
    "llvm":
        "89b967de5e79f6df7c62fdc12529671fa30989ae7b634d5a7c7996629ec1140e",
    "flang":
        "1fe07a0da20eb66a2a2aa8d354bf95c6f216ec38cc4a051e98041e0d13c34b36",
    "extras":
        "adaf7670b2497ff3ac09636e0dd30f666a5a5b742ecdcb8551d722102dcfbd85"
}

# 3.5 SHA Keys
aomp35 = dict()

aomp35 = {
    "aomp":
        "e4526489833896bbc47ba865e0d115fab278ce269789a8c99a97f444595f5f6a",
    "devlib":
        "dce3a4ba672c4a2da4c2260ee4dc96ff6dd51877f5e7e1993cb107372a35a378",
    "llvm":
        "b4fd7305dc57887eec17cce77bbf42215db46a4a3d14d8e517ab92f4e200b29d",
    "flang":
        "cc27f8bfb49257b7a4f0b03f4ba5e06a28dcb6c337065c4201b6075dd2d5bc48",
    "extras":
        "5dbf27f58b8114318208b97ba99a90483b78eebbcad4117cac6881441977e855",
    "hip":
        "86eb7749ff6f6c5f6851cd6c528504d42f9286967324a50dd0dd54a6a74cacc7",
    "vdi":
        "b21866c7c23dc536356db139b88b6beb3c97f58658836974a7fc167feb31ad7f",
    "opencl":
        "8963fcd5a167583b3db8b94363778d4df4593bfce8141e1d3c32a59fb64a0cf6"
}


class Aomp(Package):
    """llvm openmp compiler from AMD."""

    homepage = tools_url + "/aomp"
    url = tools_url + "/aomp/archive/rocm-3.9.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'estewart08']
    version('3.9.0', sha256=aomp38['aomp'])
    version('3.8.0', sha256=aomp38['aomp'])
    version('3.7.0', sha256=aomp37['aomp'])
    version('3.5.0', sha256=aomp35['aomp'])

    depends_on('cmake@3.5.2:3.13.4', type='build')
    depends_on('mesa18~llvm@18.3:', type=('build', 'link'))
    depends_on('py-setuptools@44.1.0', type='build')
    depends_on('python@2.7.18', type='build', when='@3.5.0:3.8.0')
    depends_on('python@3.6.9', type='build', when='@3.9.0:')
    depends_on('py-pip', when='@3.8.0:', type='build')
    depends_on('py-wheel@0.29.0', when='@3.8.0:', type=('build', 'run'))
    depends_on('perl-data-dumper', type='build')
    depends_on('awk', type='build')
    depends_on('elfutils', type=('build', 'link'))
    depends_on('libffi', type=('build', 'link'))

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0']:
        depends_on('hsakmt-roct@' + ver, type=('build', 'run'), when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type=('build', 'run'),
                   when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type=('build', 'run'),
                   when='@' + ver)

        if ver != '3.5.0':
            depends_on('hip@' + ver, type=('build', 'run'), when='@' + ver)
            depends_on('hip-rocclr@' + ver, type='build', when='@' + ver)

        if ver == '3.9.0':
            depends_on('rocm-gdb@' + ver, type=('build', 'run'),
                       when='@' + ver)

        # 3.9.0 Resources
        if ver == '3.9.0':
            resource(
                name='rocm-device-libs',
                url=compute_url +
                '/ROCm-Device-Libs/archive/rocm-3.9.0.tar.gz',
                sha256=aomp39['devlib'],
                expand=True,
                destination='aomp-dir',
                placement='rocm-device-libs',
                when='@3.9.0')

            resource(
                name='amd-llvm-project',
                url=tools_url + '/amd-llvm-project/archive/rocm-3.9.0.tar.gz',
                sha256=aomp39['llvm'],
                expand=True,
                destination='aomp-dir',
                placement='amd-llvm-project',
                when='@3.9.0')

            resource(
                name='flang',
                url=tools_url + '/flang/archive/rocm-3.9.0.tar.gz',
                sha256=aomp39['flang'],
                expand=True,
                destination='aomp-dir',
                placement='flang',
                when='@3.9.0')

            resource(
                name='aomp-extras',
                url=tools_url + '/aomp-extras/archive/rocm-3.9.0.tar.gz',
                sha256=aomp39['extras'],
                expand=True,
                destination='aomp-dir',
                placement='aomp-extras',
                when='@3.9.0')

        # 3.8.0 Resources
        if ver == '3.8.0':
            resource(
                name='rocm-device-libs',
                url=compute_url +
                '/ROCm-Device-Libs/archive/rocm-3.8.0.tar.gz',
                sha256=aomp38['devlib'],
                expand=True,
                destination='aomp-dir',
                placement='rocm-device-libs',
                when='@3.8.0')

            resource(
                name='amd-llvm-project',
                url=tools_url + '/amd-llvm-project/archive/rocm-3.8.0.tar.gz',
                sha256=aomp38['llvm'],
                expand=True,
                destination='aomp-dir',
                placement='amd-llvm-project',
                when='@3.8.0')

            resource(
                name='flang',
                url=tools_url + '/flang/archive/rocm-3.8.0.tar.gz',
                sha256=aomp38['flang'],
                expand=True,
                destination='aomp-dir',
                placement='flang',
                when='@3.8.0')

            resource(
                name='aomp-extras',
                url=tools_url + '/aomp-extras/archive/rocm-3.8.0.tar.gz',
                sha256=aomp38['extras'],
                expand=True,
                destination='aomp-dir',
                placement='aomp-extras',
                when='@3.8.0')

        # 3.7.0 Resources
        if ver == '3.7.0':
            resource(
                name='rocm-device-libs',
                url=compute_url +
                '/ROCm-Device-Libs/archive/rocm-3.7.0.tar.gz',
                sha256=aomp37['devlib'],
                expand=True,
                destination='aomp-dir',
                placement='rocm-device-libs',
                when='@3.7.0')

            resource(
                name='amd-llvm-project',
                url=tools_url + '/amd-llvm-project/archive/rocm-3.7.0.tar.gz',
                sha256=aomp37['llvm'],
                expand=True,
                destination='aomp-dir',
                placement='amd-llvm-project',
                when='@3.7.0')

            resource(
                name='flang',
                url=tools_url + '/flang/archive/rocm-3.7.0.tar.gz',
                sha256=aomp37['flang'],
                expand=True,
                destination='aomp-dir',
                placement='flang',
                when='@3.7.0')

            resource(
                name='aomp-extras',
                url=tools_url + '/aomp-extras/archive/rocm-3.7.0.tar.gz',
                sha256=aomp37['extras'],
                expand=True,
                destination='aomp-dir',
                placement='aomp-extras',
                when='@3.7.0')

        # 3.5.0 Resources
        elif ver == '3.5.0':
            resource(
                name='rocm-device-libs',
                url=compute_url +
                '/ROCm-Device-Libs/archive/rocm-3.5.0.tar.gz',
                sha256=aomp35['devlib'],
                expand=True,
                destination='aomp-dir',
                placement='rocm-device-libs',
                when='@3.5.0')

            resource(
                name='amd-llvm-project',
                url=tools_url + '/amd-llvm-project/archive/rocm-3.5.0.tar.gz',
                sha256=aomp35['llvm'],
                expand=True,
                destination='aomp-dir',
                placement='amd-llvm-project',
                when='@3.5.0')

            resource(
                name='flang',
                url=tools_url + '/flang/archive/rocm-3.5.0.tar.gz',
                sha256=aomp35['flang'],
                expand=True,
                destination='aomp-dir',
                placement='flang',
                when='@3.5.0')

            resource(
                name='aomp-extras',
                url=tools_url + '/aomp-extras/archive/rocm-3.5.0.tar.gz',
                sha256=aomp35['extras'],
                expand=True,
                destination='aomp-dir',
                placement='aomp-extras',
                when='@3.5.0')

            resource(
                name='hip-on-vdi',
                url=tools_url + '/hip/archive/aomp-3.5.0.tar.gz',
                sha256=aomp35['hip'],
                expand=True,
                destination='aomp-dir',
                placement='hip-on-vdi',
                when='@3.5.0')

            resource(
                name='vdi',
                url=tools_url + '/rocclr/archive/aomp-3.5.0.tar.gz',
                sha256=aomp35['vdi'],
                expand=True,
                destination='aomp-dir',
                placement='vdi',
                when='@3.5.0')

            resource(
                name='opencl-on-vdi',
                sha256=aomp35['opencl'],
                url=compute_url +
                '/ROCm-OpenCL-Runtime/archive/aomp-3.5.0.tar.gz',
                expand=True,
                destination='aomp-dir',
                placement='opencl-on-vdi',
                when='@3.5.0')

    # Copy source files over for debug build in 3.9.0
    patch('0001-Add-cmake-option-for-copying-source-for-debugging.patch',
          working_dir='aomp-dir/amd-llvm-project', when='@3.9.0:')

    # Revert back to .amdgcn.bc naming scheme for 3.8.0
    patch('0001-Add-amdgcn-to-devicelibs-bitcode-names-3.8.patch',
          working_dir='aomp-dir/amd-llvm-project', when='@3.8.0')

    # Revert back to .amdgcn.bc naming scheme for 3.7.0
    patch('0001-Add-amdgcn-to-devicelibs-bitcode-names.patch',
          working_dir='aomp-dir/amd-llvm-project', when='@3.7.0')

    def patch(self):
        # Make sure python2.7 is used for the generation of hip header
        if self.spec.version == Version('3.5.0'):
            kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
            with working_dir('aomp-dir/hip-on-vdi'):
                match = '^#!/usr/bin/python'
                python = self.spec['python'].command.path
                substitute = "#!{python}".format(python=python)
                files = [
                    'hip_prof_gen.py', 'vdi/hip_prof_gen.py'
                ]
                filter_file(match, substitute, *files, **kwargs)
        src = self.stage.source_path
        libomptarget = '{0}/aomp-dir/amd-llvm-project/openmp/libomptarget'
        aomp_extras = '{0}/aomp-dir/aomp-extras/aomp-device-libs'
        flang = '{0}/aomp-dir/flang/'

        if self.spec.version >= Version('3.9.0'):
            filter_file(
                'ADDITIONAL_VERSIONS 2.7', 'ADDITIONAL_VERSIONS 3',
                flang.format(src) + 'CMakeLists.txt')

        if self.spec.version >= Version('3.8.0'):
            filter_file(
                '{CMAKE_INSTALL_PREFIX}', '{HSA_INCLUDE}',
                libomptarget.format(src) + '/hostrpc/services/CMakeLists.txt')

            filter_file(
                'CONFIG',
                'CONFIG PATHS ${CMAKE_INSTALL_PREFIX} NO_DEFAULT_PATH',
                libomptarget.format(src) + '/../libompd/test/CMakeLists.txt')

        if self.spec.version != Version('3.5.0'):
            filter_file(
                '{ROCM_DIR}/aomp/amdgcn/bitcode', '{DEVICE_LIBS_DIR}',
                libomptarget.format(src) + '/hostrpc/CMakeLists.txt',
                libomptarget.format(src) + '/deviceRTLs/amdgcn/CMakeLists.txt')

        if self.spec.version == Version('3.5.0'):
            filter_file(
                '{ROCM_DIR}/lib/bitcode', '{DEVICE_LIBS_DIR}',
                libomptarget.format(src) +
                '/deviceRTLs/hostcall/CMakeLists.txt')

        filter_file(
            '{ROCM_DIR}/lib/bitcode', '{DEVICE_LIBS_DIR}',
            aomp_extras.format(src) + '/aompextras/CMakeLists.txt',
            aomp_extras.format(src) + '/libm/CMakeLists.txt',
            libomptarget.format(src) + '/deviceRTLs/amdgcn/CMakeLists.txt',
            string=True)

        filter_file(
            r'\${ROCM_DIR}/hsa/include \${ROCM_DIR}/hsa/include/hsa',
            '${HSA_INCLUDE}/hsa/include ${HSA_INCLUDE}/hsa/include/hsa',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            '{ROCM_DIR}/hsa/lib', '{HSA_LIB}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            r'{ROCM_DIR}/lib\)',
            '{HSAKMT_LIB})\nset(HSAKMT_LIB64 ${HSAKMT_LIB64})',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            r'-L\${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}',
            '-L${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS} -L${HSAKMT_LIB64}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            r'-rpath,\${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}',
            '-rpath,${LIBOMPTARGET_DEP_LIBHSAKMT_LIBRARIES_DIRS}' +
            ',-rpath,${HSAKMT_LIB64}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            '{ROCM_DIR}/include', '{COMGR_INCLUDE}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            '{ROCM_DIR}/include', '{COMGR_INCLUDE}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            r'-L\${LLVM_LIBDIR}\${OPENMP_LIBDIR_SUFFIX}',
            '-L${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX} -L${COMGR_LIB}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

        filter_file(
            r'rpath,\${LLVM_LIBDIR}\${OPENMP_LIBDIR_SUFFIX}',
            'rpath,${LLVM_LIBDIR}${OPENMP_LIBDIR_SUFFIX}' +
            '-Wl,-rpath,${COMGR_LIB}',
            libomptarget.format(src) + '/plugins/hsa/CMakeLists.txt')

    def setup_run_environment(self, env):
        devlibs_prefix = self.spec['rocm-device-libs'].prefix
        aomp_prefix = self.spec['aomp'].prefix
        env.set('HIP_DEVICE_LIB_PATH',
                '{0}/amdgcn/bitcode'.format(format(devlibs_prefix)))
        env.set('AOMP', '{0}'.format(format(aomp_prefix)))

    def setup_build_environment(self, env):
        aomp_prefix = self.spec['aomp'].prefix
        env.set('AOMP', '{0}'.format(format(aomp_prefix)))
        env.set('FC', '{0}/bin/flang'.format(format(aomp_prefix)))
        env.set(
            'GFXLIST',
            'gfx700 gfx701 gfx801 gfx803 gfx900 gfx902 gfx906 gfx908')

    def install(self, spec, prefix):
        src = self.stage.source_path
        gfx_list = "gfx700;gfx701;gfx801;gfx803;gfx900;gfx902;gfx906;gfx908"
        aomp_prefix = self.spec['aomp'].prefix
        devlibs_prefix = self.spec['rocm-device-libs'].prefix
        hsa_prefix = self.spec['hsa-rocr-dev'].prefix
        hsakmt_prefix = self.spec['hsakmt-roct'].prefix
        comgr_prefix = self.spec['comgr'].prefix
        opencl_src = '/aomp-dir/opencl-on-vdi/api/opencl'
        omp_src = '/aomp-dir/amd-llvm-project/openmp'
        debug_map = '-fdebug-prefix-map={0}{1}={2}'
        debug_map_format = debug_map.format(src, omp_src, aomp_prefix)
        components = dict()
        if self.spec.version >= Version('3.9.0'):
            bitcode_dir = '/amdgcn/bitcode'
        else:
            bitcode_dir = '/lib'

        components['amd-llvm-project'] = [
            '../aomp-dir/amd-llvm-project/llvm',
            '-DLLVM_ENABLE_PROJECTS=clang;lld;compiler-rt',
            '-DCMAKE_BUILD_TYPE=release',
            '-DLLVM_ENABLE_ASSERTIONS=ON',
            '-DLLVM_TARGETS_TO_BUILD=AMDGPU;X86',
            '-DCMAKE_C_COMPILER={0}'.format(self.compiler.cc),
            '-DCMAKE_CXX_COMPILER={0}'.format(self.compiler.cxx),
            '-DCMAKE_ASM_COMPILER={0}'.format(self.compiler.cc),
            '-DBUG_REPORT_URL=https://github.com/ROCm-Developer-Tools/aomp',
            '-DLLVM_ENABLE_BINDINGS=OFF',
            '-DLLVM_INCLUDE_BENCHMARKS=OFF',
            '-DLLVM_BUILD_TESTS=OFF',
            '-DLLVM_INCLUDE_TESTS=OFF',
            '-DCLANG_INCLUDE_TESTS=OFF',
            '-DCMAKE_VERBOSE_MAKEFILE=1',
            '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=FALSE'
        ]

        if self.spec.version == Version('3.5.0'):
            components['vdi'] = [
                '../aomp-dir/vdi',
                '-DUSE_COMGR_LIBRARY=yes',
                '-DOPENCL_DIR={0}{1}'.format(src, opencl_src)
            ]

            components['hip-on-vdi'] = [
                '../aomp-dir/hip-on-vdi',
                '-DVDI_ROOT={0}/aomp-dir/vdi'.format(src),
                '-DHIP_COMPILER=clang',
                '-DHIP_PLATFORM=vdi',
                '-DVDI_DIR={0}/aomp-dir/vdi'.format(src),
                '-DHSA_PATH={0}'.format(hsa_prefix),
                '-DLIBVDI_STATIC_DIR={0}/spack-build-vdi'.format(src),
                '-DCMAKE_CXX_FLAGS=-Wno-ignored-attributes'
            ]

        components['aomp-extras'] = [
            '../aomp-dir/aomp-extras',
            '-DROCM_PATH=$ROCM_DIR ',
            '-DDEVICE_LIBS_DIR={0}{1}'.format(devlibs_prefix, bitcode_dir),
            '-DAOMP_STANDALONE_BUILD=0',
            '-DDEVICELIBS_ROOT={0}/aomp-dir/rocm-device-libs'.format(src),
            '-DCMAKE_VERBOSE_MAKEFILE=1'
        ]

        components['openmp'] = [
            '../aomp-dir/amd-llvm-project/openmp',
            '-DROCM_DIR={0}'.format(hsa_prefix),
            '-DDEVICE_LIBS_DIR={0}{1}'.format(devlibs_prefix, bitcode_dir),
            '-DAOMP_STANDALONE_BUILD=0',
            '-DDEVICELIBS_ROOT={0}/aomp-dir/rocm-device-libs'.format(src),
            '-DOPENMP_TEST_C_COMPILER=$AOMP/bin/clang',
            '-DOPENMP_TEST_CXX_COMPILER=$AOMP/bin/clang++',
            '-DLIBOMPTARGET_AMDGCN_GFXLIST={0}'.format(gfx_list),
            '-DLIBOMP_COPY_EXPORTS=OFF',
            '-DHSA_INCLUDE={0}'.format(hsa_prefix),
            '-DHSA_LIB={0}/lib'.format(hsa_prefix),
            '-DHSAKMT_LIB={0}/lib'.format(hsakmt_prefix),
            '-DHSAKMT_LIB64={0}/lib64'.format(hsakmt_prefix),
            '-DCOMGR_INCLUDE={0}/include'.format(comgr_prefix),
            '-DCOMGR_LIB={0}/lib'.format(comgr_prefix),
            '-DOPENMP_ENABLE_LIBOMPTARGET=1',
            '-DOPENMP_ENABLE_LIBOMPTARGET_HSA=1'
        ]

        components['openmp-debug'] = [
            '../aomp-dir/amd-llvm-project/openmp',
            '-DROCM_DIR={0}'.format(hsa_prefix),
            '-DDEVICE_LIBS_DIR={0}{1}'.format(devlibs_prefix, bitcode_dir),
            '-DAOMP_STANDALONE_BUILD=0',
            '-DDEVICELIBS_ROOT={0}/aomp-dir/rocm-device-libs'.format(src),
            '-DOPENMP_TEST_C_COMPILER=$AOMP/bin/clang',
            '-DOPENMP_TEST_CXX_COMPILER=$AOMP/bin/clang++',
            '-DLIBOMPTARGET_AMDGCN_GFXLIST={0}'.format(gfx_list),
            '-DLIBOMP_COPY_EXPORTS=OFF',
            '-DHSA_INCLUDE={0}'.format(hsa_prefix),
            '-DHSA_LIB={0}/lib'.format(hsa_prefix),
            '-DHSAKMT_LIB={0}/lib'.format(hsakmt_prefix),
            '-DHSAKMT_LIB64={0}/lib64'.format(hsakmt_prefix),
            '-DCOMGR_INCLUDE={0}/include'.format(comgr_prefix),
            '-DCOMGR_LIB={0}/lib'.format(comgr_prefix),
            '-DLIBOMPTARGET_NVPTX_DEBUG=ON',
            '-DOPENMP_ENABLE_LIBOMPTARGET=1',
            '-DOPENMP_ENABLE_LIBOMPTARGET_HSA=1'
        ]

        if self.spec.version >= Version('3.9.0'):
            components['openmp-debug'] += [
                '-DENABLE_SOURCE_COPY=ON',
                '-DOPENMP_SOURCE_DEBUG_MAP={0}'.format(debug_map_format),
            ]

        if self.spec.version >= Version('3.8.0'):
            components['openmp-debug'] += [
                '-DLIBOMP_ARCH=x86_64',
                '-DLIBOMP_OMP_VERSION=50',
                '-DLIBOMP_OMPT_SUPPORT=ON',
                '-DLIBOMP_USE_DEBUGGER=ON',
                '-DLIBOMP_CFLAGS=-O0',
                '-DLIBOMP_CPPFLAGS=-O0',
                '-DLIBOMP_OMPD_ENABLED=ON',
                '-DLIBOMP_OMPD_SUPPORT=ON',
                '-DLIBOMP_OMPT_DEBUG=ON',
                '-DCMAKE_CXX_FLAGS=-g',
                '-DCMAKE_C_FLAGS=-g'
            ]

        components['pgmath'] = [
            '../aomp-dir/flang/runtime/libpgmath',
            '-DLLVM_ENABLE_ASSERTIONS=ON',
            '-DLLVM_CONFIG={0}/bin/llvm-config'.format(aomp_prefix),
            '-DCMAKE_CXX_COMPILER={0}/bin/clang++'.format(aomp_prefix),
            '-DCMAKE_C_COMPILER={0}/bin/clang'.format(aomp_prefix),
            '-DCMAKE_Fortran_COMPILER={0}/bin/flang'.format(aomp_prefix),
            '-DLLVM_TARGETS_TO_BUILD=AMDGPU;x86'
        ]

        components['flang'] = [
            '../aomp-dir/flang',
            '-DLLVM_ENABLE_ASSERTIONS=ON',
            '-DLLVM_CONFIG={0}/bin/llvm-config'.format(aomp_prefix),
            '-DCMAKE_CXX_COMPILER={0}/bin/clang++'.format(aomp_prefix),
            '-DCMAKE_C_COMPILER={0}/bin/clang'.format(aomp_prefix),
            '-DCMAKE_Fortran_COMPILER={0}/bin/flang'.format(aomp_prefix),
            '-DLLVM_TARGETS_TO_BUILD=AMDGPU;x86',
            '-DFLANG_OPENMP_GPU_AMD=ON',
            '-DFLANG_OPENMP_GPU_NVIDIA=ON'
        ]

        components['flang-runtime'] = [
            '../aomp-dir/flang',
            '-DLLVM_ENABLE_ASSERTIONS=ON',
            '-DLLVM_CONFIG={0}/bin/llvm-config'.format(aomp_prefix),
            '-DCMAKE_CXX_COMPILER={0}/bin/clang++'.format(aomp_prefix),
            '-DCMAKE_C_COMPILER={0}/bin/clang'.format(aomp_prefix),
            '-DCMAKE_Fortran_COMPILER={0}/bin/flang'.format(aomp_prefix),
            '-DLLVM_TARGETS_TO_BUILD=AMDGPU;x86',
            '-DLLVM_INSTALL_RUNTIME=ON',
            '-DFLANG_BUILD_RUNTIME=ON',
            '-DOPENMP_BUILD_DIR={0}/spack-build-openmp/runtime/src'.format(src)
        ]

        if self.spec.version != Version('3.5.0'):
            build_order = [
                "amd-llvm-project", "aomp-extras",
                "openmp", "openmp-debug", "pgmath", "flang", "flang-runtime"
            ]
        elif self.spec.version == Version('3.5.0'):
            build_order = [
                "amd-llvm-project", "vdi", "hip-on-vdi", "aomp-extras",
                "openmp", "openmp-debug", "pgmath", "flang", "flang-runtime"
            ]

        # Override standard CMAKE_BUILD_TYPE
        std_cmake_args.remove("-DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo")
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
