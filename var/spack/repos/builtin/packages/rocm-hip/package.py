# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.paths import spack_root
import os


class RocmHip(CMakePackage):
    """HIP is a C++ Runtime API and Kernel Language that allows
    developers to create portable applications for AMD and NVIDIA GPUs
    from single source code."""

    homepage = "https://github.com/ROCm-Developer-Tools/HIP"
    url = "https://github.com/ROCm-Developer-Tools/HIP/archive/rocm-3.5.0.tar.gz"

    version('3.5.0', 'ae8384362986b392288181bcfbe5e3a0ec91af4320c189bd83c844ed384161b3')
    depends_on('rocm-hip-clang')
    depends_on('rocm-rocclr')
    depends_on('rocm-roct-thunk-interface')
    depends_on('rocm-device-libs')
    depends_on('rocm-compilersupport')
    depends_on('rocm-rocr-runtime')
    patch('hip-config.patch')
    patch('hipcc.patch')

    def patch(self):
        filter_file(r'PROF_API_STR \"\$\{PROJECT_BINARY_DIR\}',
                    'PROF_API_STR "${CMAKE_CURRENT_SOURCE_DIR}',
                    'CMakeLists.txt')
        filter_file(r'\@HIP_CLANG_PREFIX_BIN\@',
                    '"{0}";'.format(self.spec['rocm-hip-clang'].prefix.bin),
                    'bin/hipcc')
        filter_file(r'\@ROCCLR_PREFIX\@',
                    '"{0}";'.format(self.spec['rocm-rocclr'].prefix),
                    'bin/hipcc')
        filter_file(r'\@DEVICE_LIBS_PREFIX\@',
                    '"{0}";'.format(self.spec['rocm-device-libs'].prefix.lib),
                    'bin/hipcc')
        filter_file(r'\@RUNTIME_PREFIX\@',
                    '"{0}";'.format(self.spec['rocm-rocr-runtime'].prefix),
                    'bin/hipcc')
        filter_file(r'\@SELF_PREFIX_INCLUDE\@',
                    '"{0}";'.format(self.prefix.include),
                    'bin/hipcc')
        filter_file(r'\@SELF_PREFIX_LIB\@',
                    '"{0}";'.format(self.prefix.lib),
                    'bin/hipcc')
        filter_file(r'\@SELF_PREFIX\@',
                    '"{0}";'.format(self.prefix),
                    'bin/hipcc')

    def cmake_args(self):
        spec = self.spec
        cmake_args = [
            "-DHSA_PATH={0}".format(spec['rocm-roct-thunk-interface'].prefix),
            "-DHIP_CLANG_PATH={0}".format(spec['rocm-hip-clang'].prefix.bin),
            "-DDEVICE_LIB_PATH={0}".format(
                spec['rocm-device-libs'].prefix.lib),
            "-DCMAKE_BUILD_WITH_INSTALL_RPATH=1",
            "-DHIP_COMPILER=clang",
            "-DHIP_PLATFORM=rocclr",
            "-DUSE_PROF_API=1",
        ]
        return cmake_args

    @run_after('install')
    def postinstall(self):
        with working_dir(self.prefix.bin):
            os.rename('hipcc', 'hipcc.orig')
            install('{0}/lib/spack/env/cc'.format(spack_root), 'hipcc')
            filter_file(r'FCC',
                        'FCC|hipcc',
                        'hipcc')
            filter_file(r'command\=\"\$SPACK_CXX\"',
                        'command="{0}/hipcc.orig"'.format(self.prefix.bin),
                        'hipcc')
            filter_file(r'die \"Spack compiler must be run.*',
                        'command="%s/hipcc.orig"\n'
                        '\texec "${command}" "$@"' % self.prefix.bin,
                        'hipcc')
