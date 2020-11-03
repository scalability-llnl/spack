# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.prefix import Prefix
import os


class Hip(CMakePackage):
    """HIP is a C++ Runtime API and Kernel Language that allows developers to
       create portable applications for AMD and NVIDIA GPUs from
       single source code."""

    homepage = "https://github.com/ROCm-Developer-Tools/HIP"
    url      = "https://github.com/ROCm-Developer-Tools/HIP/archive/rocm-3.8.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.8.0', sha256='6450baffe9606b358a4473d5f3e57477ca67cff5843a84ee644bcf685e75d839')
    version('3.7.0', sha256='757b392c3beb29beea27640832fbad86681dbd585284c19a4c2053891673babd')
    version('3.5.0', sha256='ae8384362986b392288181bcfbe5e3a0ec91af4320c189bd83c844ed384161b3')

    depends_on('cmake@3:', type='build')
    depends_on('perl@5.10:', type=('build', 'run'))
    depends_on('mesa~llvm@18.3:')

    for ver in ['3.5.0', '3.7.0', '3.8.0']:
        depends_on('hip-rocclr@' + ver,  type='build', when='@' + ver)
        depends_on('hsakmt-roct@' + ver, type='build', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type='link', when='@' + ver)
        depends_on('comgr@' + ver, type=('build', 'link', 'run'), when='@' + ver)
        depends_on('llvm-amdgpu@' + ver, type='build', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type=('build', 'link', 'run'), when='@' + ver)
        depends_on('rocminfo@' + ver, type=('build', 'run'), when='@' + ver)

    # Notice: most likely this will only be a hard dependency on 3.7.0
    depends_on('numactl', when='@3.7.0:')

    # Note: the ROCm ecosystem expects `lib/` and `bin/` folders with symlinks
    # in the parent directory of the package, which is incompatible with spack.
    # In hipcc the ROCM_PATH variable is used to point to the parent directory
    # of the package. With the following patch we should never hit code that
    # uses the ROCM_PATH variable again; just to be sure we set it to an empty
    # string.
    patch('0001-Make-it-possible-to-specify-the-package-folder-of-ro.patch', when='@3.5.0:')

    # See https://github.com/ROCm-Developer-Tools/HIP/pull/2141
    patch('0002-Fix-detection-of-HIP_CLANG_ROOT.patch', when='@3.5.0:')

    def setup_run_environment(self, env):
        env.set('ROCM_PATH', '')
        env.set('HIP_COMPILER', 'clang')
        env.set('HIP_PLATFORM', 'hcc')
        env.set('HIP_CLANG_PATH', self.spec['llvm-amdgpu'].prefix.bin)
        env.set('HSA_PATH', self.spec['hsa-rocr-dev'].prefix)
        env.set('ROCMINFO_PATH', self.spec['rocminfo'].prefix)
        env.set('DEVICE_LIB_PATH',
                self.spec['rocm-device-libs'].prefix.lib)

    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_run_environment(env)

    def get_rocm_prefix_info(self):
        # External packages in Spack do not currently contain dependency
        # information. External installations of hip therefore must compute
        # necessary paths to other rocm components by relative paths. This
        # assumes all components are installed under a single umbrella
        # directory. Manual edits to `fallback_path` may be necessary if this
        # assumption does not hold.
        if self.spec.external:
            # typically, self.spec.prefix is /opt/rocm/hip, so fallback_path
            # will be /opt/rocm. The rocminfo executable is usually
            # found at /opt/rocm/bin/rocminfo.
            fallback_prefix = Prefix(os.path.dirname(self.spec.prefix))
            if not os.path.isdir(fallback_prefix):
                msg = "Could not determine prefix for other rocm components\n"
                msg += "Either report a bug at github.com/spack/spack or "
                msg += "manually edit fallback_prefix in the package file as "
                msg += "a workaround."
                raise RuntimeError(msg)

            return {
                'llvm-amdgpu': fallback_prefix.llvm,
                'hsa-rocr-dev': fallback_prefix.hsa,
                'rocminfo': fallback_prefix.bin,
                'rocm-device-libs': fallback_prefix,
            }
        else:
            return dict((name, self.spec[name].prefix)
                        for name in ('llvm-amdgpu', 'hsa-rocr-dev', 'rocminfo',
                                     'rocm-device-libs'))

    def setup_dependent_build_environment(self, env, dependent_spec):
        # Indirection for dependency paths because hip may be an external in
        # Spack. See block comment on get_rocm_prefix_info
        rocm_prefixes = self.get_rocm_prefix_info()

        env.set('ROCM_PATH', '')
        env.set('HIP_COMPILER', 'clang')
        env.set('HIP_PLATFORM', 'hcc')
        env.set('HIP_CLANG_PATH', rocm_prefixes['llvm-amdgpu'].bin)
        env.set('HSA_PATH', rocm_prefixes['hsa-rocr-dev'])
        env.set('ROCMINFO_PATH', rocm_prefixes['rocminfo'])
        env.set('DEVICE_LIB_PATH', rocm_prefixes['rocm-device-libs'].lib)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.hipcc = join_path(self.prefix.bin, 'hipcc')

    def patch(self):
        filter_file(
            'INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/../include"',
            'INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"',
            'hip-config.cmake.in', string=True)

    def flag_handler(self, name, flags):
        if name == 'cxxflags' and '@3.7.0:' in self.spec:
            incl = self.spec['hip-rocclr'].prefix.include
            flags.append('-I {0}/compiler/lib/include'.format(incl))

        return (flags, None, None)

    @run_before('install')
    def filter_sbang(self):
        perl = self.spec['perl'].command
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}

        with working_dir('bin'):
            match = '^#!/usr/bin/perl'
            substitute = "#!{perl}".format(perl=perl)
            files = [
                'hipify-perl', 'hipcc', 'extractkernel',
                'hipconfig', 'hipify-cmakefile'
            ]
            filter_file(match, substitute, *files, **kwargs)

    @run_before('install')
    def filter_numactl(self):
        if '@3.7.0:' in self.spec:
            numactl = self.spec['numactl'].prefix.lib
            kwargs = {'ignore_absent': False, 'backup': False, 'string': False}

            with working_dir('bin'):
                match = ' -lnuma'
                substitute = " -L{numactl} -lnuma".format(numactl=numactl)
                filter_file(match, substitute, 'hipcc', **kwargs)

    def cmake_args(self):
        args = [
            '-DHIP_COMPILER=clang',
            '-DHIP_PLATFORM=rocclr',
            '-DHSA_PATH={0}'.format(self.spec['hsa-rocr-dev'].prefix),
            '-DLIBROCclr_STATIC_DIR={0}/lib'.format
            (self.spec['hip-rocclr'].prefix)
        ]
        return args
