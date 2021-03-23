# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *
import os.path


class Kokkos(CMakePackage, CudaPackage, ROCmPackage):
    """Kokkos implements a programming model in C++ for writing performance
    portable applications targeting all major HPC platforms."""

    homepage = "https://github.com/kokkos/kokkos"
    git = "https://github.com/kokkos/kokkos.git"
    url = "https://github.com/kokkos/kokkos/archive/3.3.01.tar.gz"

    test_requires_compiler = True

    maintainers = ['jjwilke', 'jciesko']

    version('master',  branch='master')
    version('develop', branch='develop')
    version('3.3.01', sha256='4919b00bb7b6eb80f6c335a32f98ebe262229d82e72d3bae6dd91aaf3d234c37')
    version('3.2.00', sha256='05e1b4dd1ef383ca56fe577913e1ff31614764e65de6d6f2a163b2bddb60b3e9')
    version('3.1.01', sha256='ff5024ebe8570887d00246e2793667e0d796b08c77a8227fe271127d36eec9dd')
    version('3.1.00', sha256="b935c9b780e7330bcb80809992caa2b66fd387e3a1c261c955d622dae857d878")
    version('3.0.00', sha256="c00613d0194a4fbd0726719bbed8b0404ed06275f310189b3493f5739042a92b")

    depends_on("cmake@3.10:", type='build')

    devices_variants = {
        'cuda': [False, 'Whether to build CUDA backend'],
        'openmp': [False, 'Whether to build OpenMP backend'],
        'pthread': [False, 'Whether to build Pthread backend'],
        'serial': [True,  'Whether to build serial backend'],
        'rocm': [False, 'Whether to build HIP backend'],
    }
    conflicts("+rocm", when="@:3.0")

    tpls_variants = {
        'hpx': [False, 'Whether to enable the HPX library'],
        'hwloc': [False, 'Whether to enable the HWLOC library'],
        'numactl': [False, 'Whether to enable the LIBNUMA library'],
        'memkind': [False, 'Whether to enable the MEMKIND library'],
    }

    options_variants = {
        'aggressive_vectorization': [False,
                                     'Aggressively vectorize loops'],
        'compiler_warnings': [False,
                              'Print all compiler warnings'],
        'cuda_lambda': [False,
                        'Activate experimental lambda features'],
        'cuda_ldg_intrinsic': [False,
                               'Use CUDA LDG intrinsics'],
        'cuda_relocatable_device_code': [False,
                                         'Enable RDC for CUDA'],
        'cuda_uvm': [False,
                     'Enable unified virtual memory (UVM) for CUDA'],
        'debug': [False,
                  'Activate extra debug features - may increase compiletimes'],
        'debug_bounds_check': [False,
                               'Use bounds checking - will increase runtime'],
        'debug_dualview_modify_check': [False, 'Debug check on dual views'],
        'deprecated_code': [False, 'Whether to enable deprecated code'],
        'examples': [False, 'Whether to build OpenMP  backend'],
        'explicit_instantiation': [False,
                                   'Explicitly instantiate template types'],
        'hpx_async_dispatch': [False,
                               'Whether HPX supports asynchronous dispath'],
        'profiling': [True,
                      'Create bindings for profiling tools'],
        'tuning': [False,
                   'Create bindings for tuning tools'],
        'profiling_load_print': [False,
                                 'Print which profiling tools got loaded'],
        'qthread': [False, 'Eenable the QTHREAD library'],
        'tests': [False, 'Build for tests'],
    }

    spack_micro_arch_map = {
        "graviton": "",
        "graviton2": "",
        "aarch64": "",
        "arm": "",
        "ppc": "",
        "ppc64": "",
        "ppc64le": "",
        "ppcle": "",
        "sparc": None,
        "sparc64": None,
        "x86": "",
        "x86_64": "",
        "thunderx2": "THUNDERX2",
        "k10": None,
        "zen": "ZEN",
        "bulldozer": "",
        "piledriver": "",
        "zen2": "ZEN2",
        "steamroller": "KAVERI",
        "excavator": "CARIZO",
        "a64fx": "",
        "power7": "POWER7",
        "power8": "POWER8",
        "power9": "POWER9",
        "power8le": "POWER8",
        "power9le": "POWER9",
        "i686": None,
        "pentium2": None,
        "pentium3": None,
        "pentium4": None,
        "prescott": None,
        "nocona": None,
        "nehalem": None,
        "sandybridge": "SNB",
        "haswell": "HSW",
        "mic_knl": "KNL",
        "cannonlake": "SKX",
        "cascadelake": "SKX",
        "westmere": "WSM",
        "core2": None,
        "ivybridge": "SNB",
        "broadwell": "BDW",
        # @AndrewGaspar: Kokkos does not have an arch for plain-skylake - only
        # for Skylake-X (i.e. Xeon). For now, I'm mapping this to Broadwell
        # until Kokkos learns to optimize for SkyLake without the AVX-512
        # extensions. SkyLake with AVX-512 will still be optimized using the
        # separate `skylake_avx512` arch.
        "skylake": "BDW",
        "icelake": "SKX",
        "skylake_avx512": "SKX",
    }

    spack_cuda_arch_map = {
        "30": 'kepler30',
        "32": 'kepler32',
        "35": 'kepler35',
        "37": 'kepler37',
        "50": 'maxwell50',
        "52": 'maxwell52',
        "53": 'maxwell53',
        "60": 'pascal60',
        "61": 'pascal61',
        "70": 'volta70',
        "72": 'volta72',
        "75": 'turing75',
        "80": 'ampere80',
    }
    cuda_arches = spack_cuda_arch_map.values()
    conflicts("+cuda", when="cuda_arch=none")

    amdgpu_arch_map = {
        'gfx900': 'vega900',
        'gfx906': 'vega906',
        'gfx908': 'vega908'
    }
    amd_support_conflict_msg = (
        '{0} is not supported; '
        'Kokkos supports the following AMD GPU targets: '
        + ', '.join(amdgpu_arch_map.keys()))
    for arch in ROCmPackage.amdgpu_targets:
        if arch not in amdgpu_arch_map:
            conflicts('+rocm', when='amdgpu_target={0}'.format(arch),
                      msg=amd_support_conflict_msg.format(arch))

    devices_values = list(devices_variants.keys())
    for dev in devices_variants:
        dflt, desc = devices_variants[dev]
        variant(dev, default=dflt, description=desc)

    options_values = list(options_variants.keys())
    for opt in options_values:
        if "cuda" in opt:
            conflicts('+%s' % opt, when="~cuda",
                      msg="Must enable CUDA to use %s" % opt)
        dflt, desc = options_variants[opt]
        variant(opt, default=dflt, description=desc)

    tpls_values = list(tpls_variants.keys())
    for tpl in tpls_values:
        dflt, desc = tpls_variants[tpl]
        variant(tpl, default=dflt, description=desc)
        depends_on(tpl, when="+%s" % tpl)

    variant("wrapper", default=False,
            description="Use nvcc-wrapper for CUDA build")
    depends_on("kokkos-nvcc-wrapper", when="+wrapper")
    depends_on("kokkos-nvcc-wrapper@develop", when="@develop+wrapper")
    depends_on("kokkos-nvcc-wrapper@master", when="@master+wrapper")
    conflicts("+wrapper", when="~cuda")

    variant("std", default="14", values=["11", "14", "17", "20"], multi=False)
    variant("pic", default=False, description="Build position independent code")

    # nvcc does not currently work with C++17 or C++20
    conflicts("+cuda", when="std=17")
    conflicts("+cuda", when="std=20")

    variant('shared', default=True, description='Build shared libraries')

    def append_args(self, cmake_prefix, cmake_options, spack_options):
        variant_to_cmake_option = {'rocm': 'hip'}
        for variant_name in cmake_options:
            enablestr = "+%s" % variant_name
            opt = variant_to_cmake_option.get(variant_name, variant_name)
            optuc = opt.upper()
            optname = "Kokkos_%s_%s" % (cmake_prefix, optuc)
            option = None
            if enablestr in self.spec:
                option = "-D%s=ON" % optname
            else:
                # explicitly turn off if not enabled
                # this avoids any confusing implicit defaults
                # that come from the CMake
                option = "-D%s=OFF" % optname
            if option not in spack_options:
                spack_options.append(option)

    def setup_dependent_package(self, module, dependent_spec):
        try:
            self.spec.kokkos_cxx = self.spec["kokkos-nvcc-wrapper"].kokkos_cxx
        except Exception:
            self.spec.kokkos_cxx = spack_cxx

    def cmake_args(self):
        spec = self.spec

        if spec.satisfies('~wrapper+cuda') and not spec.satisfies('%clang'):
            raise InstallError("Kokkos requires +wrapper when using +cuda"
                               "without clang")

        options = []

        isdiy = "+diy" in spec
        if isdiy:
            options.append("-DSpack_WORKAROUND=On")

        if "+pic" in spec:
            options.append("-DCMAKE_POSITION_INDEPENDENT_CODE=ON")

        spack_microarches = []
        if "+cuda" in spec:
            # this is a list
            for cuda_arch in spec.variants["cuda_arch"].value:
                if not cuda_arch == "none":
                    kokkos_arch_name = self.spack_cuda_arch_map[cuda_arch]
                    spack_microarches.append(kokkos_arch_name)

        kokkos_microarch_name = self.spack_micro_arch_map[spec.target.name]
        if kokkos_microarch_name:
            spack_microarches.append(kokkos_microarch_name)

        if "+rocm" in spec:
            for amdgpu_target in spec.variants['amdgpu_target'].value:
                if amdgpu_target != "none":
                    if amdgpu_target in self.amdgpu_arch_map:
                        spack_microarches.append(
                            self.amdgpu_arch_map[amdgpu_target])
                    else:
                        # Note that conflict declarations should prevent
                        # choosing an unsupported AMD GPU target
                        raise SpackError("Unsupported target: {0}".format(
                            amdgpu_target))

        for arch in spack_microarches:
            options.append("-DKokkos_ARCH_%s=ON" % arch.upper())

        self.append_args("ENABLE", self.devices_values, options)
        self.append_args("ENABLE", self.options_values, options)
        self.append_args("ENABLE", self.tpls_values, options)

        for tpl in self.tpls_values:
            var = "+%s" % tpl
            if var in self.spec:
                options.append("-D%s_DIR=%s" % (tpl, spec[tpl].prefix))

        if '+rocm' in self.spec:
            options.append('-DCMAKE_CXX_COMPILER=%s' %
                           self.spec['hip'].hipcc)
        elif '+wrapper' in self.spec:
            options.append("-DCMAKE_CXX_COMPILER=%s" %
                           self.spec["kokkos-nvcc-wrapper"].kokkos_cxx)

        # Set the C++ standard to use
        options.append("-DKokkos_CXX_STANDARD=%s" %
                       self.spec.variants["std"].value)

        options.append('-DBUILD_SHARED_LIBS=%s' % ('+shared' in self.spec))

        return options

    test_script_relative_path = "scripts/spack_test"

    @run_after('install')
    def setup_build_tests(self):
        # Skip if unsupported version
        cmake_source_path = join_path(self.stage.source_path,
                                      self.test_script_relative_path)
        if not os.path.exists(cmake_source_path):
            return
        """Copy test."""
        cmake_out_path = join_path(self.test_script_relative_path, 'out')
        cmake_args = [cmake_source_path,
                      "-DSPACK_PACKAGE_SOURCE_DIR:PATH={0}".
                      format(self.stage.source_path),
                      "-DSPACK_PACKAGE_TEST_ROOT_DIR:PATH={0}".
                      format(join_path(self.install_test_root, cmake_out_path)),
                      "-DSPACK_PACKAGE_INSTALL_DIR:PATH={0}".format(self.prefix)]
        cmake(*cmake_args)
        self.cache_extra_test_sources(cmake_out_path)

    def build_tests(self):
        """Build test."""
        cmake_path = join_path(self.install_test_root,
                               self.test_script_relative_path, 'out')
        cmake_args = [cmake_path, '-DEXECUTABLE_OUTPUT_PATH=' + cmake_path]
        cmake(*cmake_args)
        make()

    def run_tests(self):
        """Run test."""
        reason = 'Checking ability to execute.'
        run_path = join_path(self.install_test_root,
                             self.test_script_relative_path, 'out')
        self.run_test('make', [run_path, 'test'], [], installed=False, purpose=reason)

    def test(self):
        # Skip if unsupported version
        cmake_path = join_path(self.install_test_root,
                               self.test_script_relative_path, 'out')
        if not os.path.exists(cmake_path):
            print('Skipping smoke tests: {0} is missing'.format(cmake_path))
            return
        self.build_tests()
        self.run_tests()
