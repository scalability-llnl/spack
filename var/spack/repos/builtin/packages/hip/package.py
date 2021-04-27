# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.prefix import Prefix
from spack.hooks.sbang import filter_shebang
import os


class Hip(CMakePackage):
    """HIP is a C++ Runtime API and Kernel Language that allows developers to
       create portable applications for AMD and NVIDIA GPUs from
       single source code."""

    homepage = "https://github.com/ROCm-Developer-Tools/HIP"
    git      = "https://github.com/ROCm-Developer-Tools/HIP.git"
    url      = "https://github.com/ROCm-Developer-Tools/HIP/archive/rocm-4.1.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('4.1.0', sha256='e21c10b62868ece7aa3c8413ec0921245612d16d86d81fe61797bf9a64bc37eb')
    version('4.0.0', sha256='d7b78d96cec67c55b74ea3811ce861b16d300410bc687d0629e82392e8d7c857')
    version('3.10.0', sha256='0082c402f890391023acdfd546760f41cb276dffc0ffeddc325999fd2331d4e8')
    version('3.9.0', sha256='25ad58691456de7fd9e985629d0ed775ba36a2a0e0b21c086bd96ba2fb0f7ed1')
    version('3.8.0', sha256='6450baffe9606b358a4473d5f3e57477ca67cff5843a84ee644bcf685e75d839')
    version('3.7.0', sha256='757b392c3beb29beea27640832fbad86681dbd585284c19a4c2053891673babd')
    version('3.5.0', sha256='ae8384362986b392288181bcfbe5e3a0ec91af4320c189bd83c844ed384161b3')

    depends_on('cmake@3:', type='build')
    depends_on('perl@5.10:', type=('build', 'run'))
    depends_on('mesa18~llvm@18.3:')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0']:
        depends_on('hip-rocclr@' + ver,  type=('build', 'run'), when='@' + ver)
        depends_on('hsakmt-roct@' + ver, type='build', when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver, type='link', when='@' + ver)
        depends_on('comgr@' + ver, type=('build', 'link', 'run'), when='@' + ver)
        depends_on('llvm-amdgpu@' + ver, type='build', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type=('build', 'link', 'run'), when='@' + ver)
        depends_on('rocminfo@' + ver, type=('build', 'run'), when='@' + ver)

    # hipcc likes to add `-lnuma` by default :(
    # ref https://github.com/ROCm-Developer-Tools/HIP/pull/2202
    depends_on('numactl', when='@3.7.0:')

    # Note: the ROCm ecosystem expects `lib/` and `bin/` folders with symlinks
    # in the parent directory of the package, which is incompatible with spack.
    # In hipcc the ROCM_PATH variable is used to point to the parent directory
    # of the package. With the following patch we should never hit code that
    # uses the ROCM_PATH variable again; just to be sure we set it to an empty
    # string.
    patch('0001-Make-it-possible-to-specify-the-package-folder-of-ro.patch', when='@3.5.0:')

    # See https://github.com/ROCm-Developer-Tools/HIP/pull/2141
    patch('0002-Fix-detection-of-HIP_CLANG_ROOT.patch', when='@:3.9.0')

    # See https://github.com/ROCm-Developer-Tools/HIP/pull/2218
    patch('0003-Improve-compilation-without-git-repo.3.7.0.patch', when='@3.7.0:3.9.0')
    patch('0003-Improve-compilation-without-git-repo.3.10.0.patch', when='@3.10.0:4.0.0')
    patch('0003-Improve-compilation-without-git-repo.4.1.0.patch', when='@4.1.0')

    # See https://github.com/ROCm-Developer-Tools/HIP/pull/2219
    patch('0004-Drop-clang-rt-builtins-linking-on-hip-host.3.7.0.patch', when='@3.7.0:3.9.0')
    patch('0004-Drop-clang-rt-builtins-linking-on-hip-host.3.10.0.patch', when='@3.10.0:4.1.0')

    def get_paths(self):
        if self.spec.external:
            # For external packages we only assume the `hip` prefix is known,
            # because spack does not set prefixes of dependencies of externals.
            # We assume self.spec.prefix is /opt/rocm-x.y.z/hip and rocm has a
            # default installation with everything installed under
            # /opt/rocm-x.y.z
            rocm_prefix = Prefix(os.path.dirname(self.spec.prefix))

            if not os.path.isdir(rocm_prefix):
                msg = "Could not determine prefix for other rocm components\n"
                msg += "Either report a bug at github.com/spack/spack or "
                msg += "manually edit rocm_prefix in the package file as "
                msg += "a workaround."
                raise RuntimeError(msg)

            paths = {
                'rocm-path': rocm_prefix,
                'llvm-amdgpu': rocm_prefix.llvm,
                'hsa-rocr-dev': rocm_prefix.hsa,
                'rocminfo': rocm_prefix,
                'rocm-device-libs': rocm_prefix,
            }
        else:
            paths = {
                'rocm-path': self.spec.prefix,
                'llvm-amdgpu': self.spec['llvm-amdgpu'].prefix,
                'hsa-rocr-dev': self.spec['hsa-rocr-dev'].prefix,
                'rocminfo': self.spec['rocminfo'].prefix,
                'rocm-device-libs': self.spec['rocm-device-libs'].prefix,
            }

        # `device_lib_path` is the path to the bitcode directory
        if '@:3.8.0' in self.spec:
            paths['device_lib_path'] = paths['rocm-device-libs'].lib
        else:
            paths['device_lib_path'] = paths['rocm-device-libs'].amdgcn.bitcode

        return paths

    def set_variables(self, env):
        # Note: do not use self.spec[name] here, since not all dependencies
        # have defined prefixes when hip is marked as external.
        paths = self.get_paths()

        # Used in hipcc, but only useful when hip is external, since only then
        # there is a common prefix /opt/rocm-x.y.z.
        env.set('ROCM_PATH', paths['rocm-path'])

        # hipcc recognizes HIP_PLATFORM == hcc and HIP_COMPILER == clang, even
        # though below we specified HIP_PLATFORM=rocclr and HIP_COMPILER=clang
        # in the CMake args.
        if self.spec.satisfies('@:4.0.0'):
            env.set('HIP_PLATFORM', 'hcc')
        else:
            env.set('HIP_PLATFORM', 'amd')

        env.set('HIP_COMPILER', 'clang')

        # bin directory where clang++ resides
        env.set('HIP_CLANG_PATH', paths['llvm-amdgpu'].bin)

        # Path to hsa-rocr-dev prefix used by hipcc.
        env.set('HSA_PATH', paths['hsa-rocr-dev'])

        # This is a variable that does not exist in hipcc but was introduced
        # in a patch of ours since 3.5.0 to locate rocm_agent_enumerator:
        # https://github.com/ROCm-Developer-Tools/HIP/pull/2138
        env.set('ROCMINFO_PATH', paths['rocminfo'])

        # This one is used in hipcc to run `hipcc --hip-device-lib-path=...`
        env.set('DEVICE_LIB_PATH', paths['device_lib_path'])

        # And this is used in clang whenever the --hip-device-lib-path is not
        # used (e.g. when clang is invoked directly)
        env.set('HIP_DEVICE_LIB_PATH', paths['device_lib_path'])

        # Just the prefix of hip (used in hipcc)
        env.set('HIP_PATH', paths['rocm-path'])

        # Used in comgr and seems necessary when using the JIT compiler, e.g.
        # hiprtcCreateProgram:
        # https://github.com/RadeonOpenCompute/ROCm-CompilerSupport/blob/rocm-4.0.0/lib/comgr/src/comgr-env.cpp
        env.set('LLVM_PATH', paths['llvm-amdgpu'])

        # Finally we have to set --rocm-path=<prefix> ourselves, which is not
        # the same as --hip-device-lib-path (set by hipcc). It's used to set
        # default bin, include and lib folders in clang. If it's not set it is
        # infered from the clang install dir (and they try to find
        # /opt/rocm again...). If this path is set, there is no strict checking
        # and parsing of the <prefix>/bin/.hipVersion file. Let's just set this
        # to the hip prefix directory for non-external builds so that the
        # bin/.hipVersion file can still be parsed.
        # See also https://github.com/ROCm-Developer-Tools/HIP/issues/2223
        if '@3.8.0:' in self.spec:
            env.append_path('HIPCC_COMPILE_FLAGS_APPEND',
                            '--rocm-path={0}'.format(paths['rocm-path']),
                            separator=' ')

    def setup_run_environment(self, env):
        self.set_variables(env)

    def setup_dependent_build_environment(self, env, dependent_spec):
        self.set_variables(env)

        if 'amdgpu_target' in dependent_spec.variants:
            arch = dependent_spec.variants['amdgpu_target'].value
            if arch != 'none':
                env.set('HCC_AMDGPU_TARGET', ','.join(arch))

    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_dependent_build_environment(env, dependent_spec)

    def setup_dependent_package(self, module, dependent_spec):
        self.spec.hipcc = join_path(self.prefix.bin, 'hipcc')

    def patch(self):
        filter_file(
            'INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/../include"',
            'INTERFACE_INCLUDE_DIRECTORIES "${_IMPORT_PREFIX}/include"',
            'hip-config.cmake.in', string=True)

        perl = self.spec['perl'].command
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}

        with working_dir('bin'):
            match = '^#!/usr/bin/perl'
            substitute = "#!{perl}".format(perl=perl)

            if self.spec.satisfies('@:4.0.0'):
                files = [
                    'hipify-perl', 'hipcc', 'extractkernel',
                    'hipconfig', 'hipify-cmakefile'
                ]
            else:
                files = [
                    'hipify-perl', 'hipcc', 'roc-obj-extract',
                    'hipconfig', 'hipify-cmakefile',
                    'roc-obj-ls', 'hipvars.pm'
                ]

            filter_file(match, substitute, *files, **kwargs)

            # This guy is used during the cmake phase, so we have to fix the
            # shebang already here in case it is too long.
            filter_shebang('hipconfig')

        if '@3.7.0:' in self.spec:
            numactl = self.spec['numactl'].prefix.lib
            kwargs = {'ignore_absent': False, 'backup': False, 'string': False}

            with working_dir('bin'):
                match = ' -lnuma'
                substitute = " -L{numactl} -lnuma".format(numactl=numactl)
                filter_file(match, substitute, 'hipcc', **kwargs)

    def flag_handler(self, name, flags):
        if name == 'cxxflags' and '@3.7.0:' in self.spec:
            incl = self.spec['hip-rocclr'].prefix.include
            flags.append('-I {0}/compiler/lib/include'.format(incl))
            flags.append('-I {0}/elf'.format(incl))

        return (flags, None, None)

    def cmake_args(self):
        args = [
            self.define('HIP_COMPILER', 'clang'),
            self.define('HSA_PATH', self.spec['hsa-rocr-dev'].prefix)
        ]
        if self.spec.satisfies('@:4.0.0'):
            args.append(self.define('HIP_RUNTIME', 'ROCclr'))
            args.append(self.define('HIP_PLATFORM', 'rocclr'))
        else:
            args.append(self.define('HIP_RUNTIME', 'rocclr'))
            args.append(self.define('HIP_PLATFORM', 'amd'))

        # LIBROCclr_STATIC_DIR is unused from 3.6.0 and above
        if '@3.5.0' in self.spec:
            args.append(self.define('LIBROCclr_STATIC_DIR',
                        self.spec['hip-rocclr'].prefix.lib))

        return args
