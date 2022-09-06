# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os.path

from llnl.util import tty

from spack.package import *


class Kokkos(CMakePackage, CudaPackage, ROCmPackage):
    """Kokkos implements a programming model in C++ for writing performance
    portable applications targeting all major HPC platforms."""

    homepage = "https://github.com/kokkos/kokkos"
    git = "https://github.com/kokkos/kokkos.git"
    url = "https://github.com/kokkos/kokkos/archive/3.6.00.tar.gz"

    tags = ["e4s"]

    test_requires_compiler = True

    maintainers("janciesko", "crtrott")

    version("master", branch="master")
    version("develop", branch="develop")
    version("3.7.01", sha256="0481b24893d1bcc808ec68af1d56ef09b82a1138a1226d6be27c3b3c3da65ceb")
    version("3.7.00", sha256="62e3f9f51c798998f6493ed36463f66e49723966286ef70a9dcba329b8443040")
    version("3.6.01", sha256="1b80a70c5d641da9fefbbb652e857d7c7a76a0ebad1f477c253853e209deb8db")
    version("3.6.00", sha256="53b11fffb53c5d48da5418893ac7bc814ca2fde9c86074bdfeaa967598c918f4")
    version("3.5.00", sha256="748f06aed63b1e77e3653cd2f896ef0d2c64cb2e2d896d9e5a57fec3ff0244ff")
    version("3.4.01", sha256="146d5e233228e75ef59ca497e8f5872d9b272cb93e8e9cdfe05ad34a23f483d1")
    version("3.4.00", sha256="2e4438f9e4767442d8a55e65d000cc9cde92277d415ab4913a96cd3ad901d317")
    version("3.3.01", sha256="4919b00bb7b6eb80f6c335a32f98ebe262229d82e72d3bae6dd91aaf3d234c37")
    version("3.3.00", sha256="170b9deaa1943185e928f8fcb812cd4593a07ed7d220607467e8f0419e147295")
    version("3.2.01", sha256="9e27a3d8f81559845e190d60f277d84d6f558412a3df3301d9545e91373bcaf1")
    version("3.2.00", sha256="05e1b4dd1ef383ca56fe577913e1ff31614764e65de6d6f2a163b2bddb60b3e9")
    version("3.1.01", sha256="ff5024ebe8570887d00246e2793667e0d796b08c77a8227fe271127d36eec9dd")
    version("3.1.00", sha256="b935c9b780e7330bcb80809992caa2b66fd387e3a1c261c955d622dae857d878")
    version("3.0.00", sha256="c00613d0194a4fbd0726719bbed8b0404ed06275f310189b3493f5739042a92b")

    depends_on("cmake@3.16:", type="build")

    devices_variants = {
        "cuda": [False, "Whether to build CUDA backend"],
        "openmp": [False, "Whether to build OpenMP backend"],
        "pthread": [False, "Whether to build Pthread backend"],
        "serial": [True, "Whether to build serial backend"],
        "rocm": [False, "Whether to build HIP backend"],
        "sycl": [False, "Whether to build the SYCL backend"],
        "openmptarget": [False, "Whether to build the OpenMPTarget backend"],
    }
    conflicts("+rocm", when="@:3.0")
    conflicts("+sycl", when="@:3.3")
    conflicts("+openmptarget", when="@:3.5")

    # https://github.com/spack/spack/issues/29052
    conflicts("@:3.5 +sycl", when="%dpcpp@2022:")
    conflicts("@:3.5 +sycl", when="%oneapi@2022:")

    tpls_variants = {
        "hpx": [False, "Whether to enable the HPX library"],
        "hwloc": [False, "Whether to enable the HWLOC library"],
        "numactl": [False, "Whether to enable the LIBNUMA library"],
        "memkind": [False, "Whether to enable the MEMKIND library"],
    }

    options_variants = {
        "aggressive_vectorization": [False, "Aggressively vectorize loops"],
        "compiler_warnings": [False, "Print all compiler warnings"],
        "cuda_constexpr": [False, "Activate experimental constexpr features"],
        "cuda_lambda": [False, "Activate experimental lambda features"],
        "cuda_ldg_intrinsic": [False, "Use CUDA LDG intrinsics"],
        "cuda_relocatable_device_code": [False, "Enable RDC for CUDA"],
        "cuda_uvm": [False, "Enable unified virtual memory (UVM) for CUDA"],
        "debug": [False, "Activate extra debug features - may increase compiletimes"],
        "debug_bounds_check": [False, "Use bounds checking - will increase runtime"],
        "debug_dualview_modify_check": [False, "Debug check on dual views"],
        "deprecated_code": [False, "Whether to enable deprecated code"],
        "examples": [False, "Whether to build examples"],
        "explicit_instantiation": [False, "Explicitly instantiate template types"],
        "hpx_async_dispatch": [False, "Whether HPX supports asynchronous dispath"],
        "profiling": [True, "Create bindings for profiling tools"],
        "tuning": [False, "Create bindings for tuning tools"],
        "profiling_load_print": [False, "Print which profiling tools got loaded"],
        "qthread": [False, "Eenable the QTHREAD library"],
        "tests": [False, "Build for tests"],
    }

    spack_micro_arch_map = {
        "thunderx2": "THUNDERX2",
        "zen": "ZEN",
        "zen2": "ZEN2",
        "steamroller": "KAVERI",
        "excavator": "CARIZO",
        "power7": "POWER7",
        "power8": "POWER8",
        "power9": "POWER9",
        "power8le": "POWER8",
        "power9le": "POWER9",
        "sandybridge": "SNB",
        "haswell": "HSW",
        "mic_knl": "KNL",
        "cannonlake": "SKX",
        "cascadelake": "SKX",
        "westmere": "WSM",
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
        "30": "kepler30",
        "32": "kepler32",
        "35": "kepler35",
        "37": "kepler37",
        "50": "maxwell50",
        "52": "maxwell52",
        "53": "maxwell53",
        "60": "pascal60",
        "61": "pascal61",
        "70": "volta70",
        "72": "volta72",
        "75": "turing75",
        "80": "ampere80",
        "86": "ampere86",
    }
    cuda_arches = spack_cuda_arch_map.values()
    conflicts("+cuda", when="cuda_arch=none")

    amdgpu_arch_map = {
        "gfx900": "vega900",
        "gfx906": "vega906",
        "gfx908": "vega908",
        "gfx90a": "vega90A",
    }
    amd_support_conflict_msg = (
        "{0} is not supported; "
        "Kokkos supports the following AMD GPU targets: " + ", ".join(amdgpu_arch_map.keys())
    )
    for arch in ROCmPackage.amdgpu_targets:
        if arch not in amdgpu_arch_map:
            conflicts(
                "rocm-config target={0}".format(arch),
                msg=amd_support_conflict_msg.format(arch)
            )
    depends_on("rocm-suite", when="+rocm")

    intel_gpu_arches = (
        "intel_gen",
        "intel_gen9",
        "intel_gen11",
        "intel_gen12lp",
        "intel_dg1",
        "intel_xehp",
        "intel_pvc",
    )
    variant(
        "intel_gpu_arch",
        default="none",
        values=("none",) + intel_gpu_arches,
        description="Intel GPU architecture",
    )

    devices_values = list(devices_variants.keys())
    for dev in devices_variants:
        dflt, desc = devices_variants[dev]
        variant(dev, default=dflt, description=desc)
    conflicts("+cuda", when="+rocm", msg="CUDA and ROCm are not compatible in Kokkos.")

    options_values = list(options_variants.keys())
    for opt in options_values:
        if "cuda" in opt:
            conflicts("+%s" % opt, when="~cuda", msg="Must enable CUDA to use %s" % opt)
        dflt, desc = options_variants[opt]
        variant(opt, default=dflt, description=desc)

    tpls_values = list(tpls_variants.keys())
    for tpl in tpls_values:
        dflt, desc = tpls_variants[tpl]
        variant(tpl, default=dflt, description=desc)
        depends_on(tpl, when="+%s" % tpl)

    variant("wrapper", default=False, description="Use nvcc-wrapper for CUDA build")
    depends_on("kokkos-nvcc-wrapper", when="+wrapper")
    depends_on("kokkos-nvcc-wrapper@develop", when="@develop+wrapper")
    depends_on("kokkos-nvcc-wrapper@master", when="@master+wrapper")
    conflicts("+wrapper", when="~cuda")

    stds = ["11", "14", "17", "20"]
    # TODO: This should be named cxxstd for consistency with other packages
    variant("std", default="14", values=stds, multi=False)
    variant("pic", default=False, description="Build position independent code")

    # nvcc does not currently work with C++17 or C++20
    conflicts("+cuda", when="std=17 ^cuda@:10")
    conflicts("+cuda", when="std=20")

    # SYCL and OpenMPTarget require C++17 or higher
    for stdver in stds[: stds.index("17")]:
        conflicts("+sycl", when="std={0}".format(stdver), msg="SYCL requires C++17 or higher")
        conflicts(
            "+openmptarget",
            when="std={0}".format(stdver),
            msg="OpenMPTarget requires C++17 or higher",
        )

    # HPX should use the same C++ standard
    for std in stds:
        depends_on("hpx cxxstd={0}".format(std), when="+hpx std={0}".format(std))

    # HPX version constraints
    depends_on("hpx@:1.6", when="@:3.5 +hpx")
    depends_on("hpx@1.7:", when="@3.6: +hpx")

    # Patches
    patch("hpx_profiling_fences.patch", when="@3.5.00 +hpx")

    variant("shared", default=True, description="Build shared libraries")

    # Filter spack-generated files that may include links to the
    # spack compiler wrappers
    filter_compiler_wrappers("kokkos_launch_compiler", relative_root="bin")
    filter_compiler_wrappers(
        "KokkosConfigCommon.cmake", relative_root=os.path.join("lib64", "cmake", "Kokkos")
    )

    @classmethod
    def get_microarch(cls, target):
        """Get the Kokkos microarch name for a Spack target (spec.target)."""
        smam = cls.spack_micro_arch_map

        # Find closest ancestor that has a known microarch optimization
        if target.name not in smam:
            for target in target.ancestors:
                if target.name in smam:
                    break
            else:
                # No known microarch optimizatinos
                return None

        return smam[target.name]

    def append_args(self, cmake_prefix, cmake_options, spack_options):
        variant_to_cmake_option = {"rocm": "hip"}
        for variant_name in cmake_options:
            opt = variant_to_cmake_option.get(variant_name, variant_name)
            optname = "Kokkos_%s_%s" % (cmake_prefix, opt.upper())
            # Explicitly enable or disable
            option = self.define_from_variant(optname, variant_name)
            if option not in spack_options:
                spack_options.append(option)

    def setup_dependent_package(self, module, dependent_spec):
        try:
            self.spec.kokkos_cxx = self.spec["kokkos-nvcc-wrapper"].kokkos_cxx
        except Exception:
            self.spec.kokkos_cxx = spack_cxx

    def cmake_args(self):
        spec = self.spec
        from_variant = self.define_from_variant

        if spec.satisfies("~wrapper+cuda") and not (
            spec.satisfies("%clang") or spec.satisfies("%cce")
        ):
            raise InstallError("Kokkos requires +wrapper when using +cuda" "without clang")

        options = [
            from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            from_variant("CMAKE_CXX_STANDARD", "std"),
            from_variant("BUILD_SHARED_LIBS", "shared"),
        ]

        spack_microarches = []
        if "+cuda" in spec:
            # this is a list
            for cuda_arch in spec.variants["cuda_arch"].value:
                if not cuda_arch == "none":
                    kokkos_arch_name = self.spack_cuda_arch_map[cuda_arch]
                    spack_microarches.append(kokkos_arch_name)

        kokkos_microarch_name = self.get_microarch(spec.target)
        if kokkos_microarch_name:
            spack_microarches.append(kokkos_microarch_name)

        if "+rocm" in spec:
            for amdgpu_target in self.get_amdgpu_targets_without_features(spec):
                if amdgpu_target != "none":
                    if amdgpu_target in self.amdgpu_arch_map:
                        spack_microarches.append(self.amdgpu_arch_map[amdgpu_target])
                    else:
                        # Note that conflict declarations should prevent
                        # choosing an unsupported AMD GPU target
                        raise SpackError("Unsupported target: {0}".format(amdgpu_target))

        if self.spec.variants["intel_gpu_arch"].value != "none":
            spack_microarches.append(self.spec.variants["intel_gpu_arch"].value)

        for arch in spack_microarches:
            options.append(self.define("Kokkos_ARCH_" + arch.upper(), True))

        self.append_args("ENABLE", self.devices_values, options)
        self.append_args("ENABLE", self.options_values, options)
        self.append_args("ENABLE", self.tpls_values, options)

        for tpl in self.tpls_values:
            if spec.variants[tpl].value:
                options.append(self.define(tpl + "_DIR", spec[tpl].prefix))

        if "+rocm" in self.spec:
            options.append(self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc))
        elif "+wrapper" in self.spec:
            options.append(
                self.define("CMAKE_CXX_COMPILER", self.spec["kokkos-nvcc-wrapper"].kokkos_cxx)
            )

        return options

    test_script_relative_path = join_path("scripts", "spack_test")

    # TODO: Replace this method and its 'get' use for cmake path with
    #   join_path(self.spec['cmake'].prefix.bin, 'cmake') once stand-alone
    #   tests can access build dependencies through self.spec['cmake'].
    def cmake_bin(self, set=True):
        """(Hack) Set/get cmake dependency path."""
        filepath = join_path(self.install_test_root, "cmake_bin_path.txt")
        if set:
            with open(filepath, "w") as out_file:
                cmake_bin = join_path(self.spec["cmake"].prefix.bin, "cmake")
                out_file.write("{0}\n".format(cmake_bin))
        elif os.path.isfile(filepath):
            with open(filepath, "r") as in_file:
                return in_file.read().strip()

    @run_after("install")
    def setup_build_tests(self):
        # Skip if unsupported version
        cmake_source_path = join_path(self.stage.source_path, self.test_script_relative_path)
        if not os.path.exists(cmake_source_path):
            return
        """Copy test."""
        cmake_out_path = join_path(self.test_script_relative_path, "out")
        cmake_args = [
            cmake_source_path,
            "-DSPACK_PACKAGE_SOURCE_DIR:PATH={0}".format(self.stage.source_path),
            "-DSPACK_PACKAGE_TEST_ROOT_DIR:PATH={0}".format(
                join_path(self.install_test_root, cmake_out_path)
            ),
            "-DSPACK_PACKAGE_INSTALL_DIR:PATH={0}".format(self.prefix),
        ]
        cmake(*cmake_args)
        self.cache_extra_test_sources(cmake_out_path)
        self.cmake_bin(set=True)

    def build_tests(self, cmake_path):
        """Build test."""
        cmake_bin = self.cmake_bin(set=False)

        if not cmake_bin:
            tty.msg("Skipping kokkos test: cmake_bin_path.txt not found")
            return

        cmake_args = [cmake_path, "-DEXECUTABLE_OUTPUT_PATH=" + cmake_path]

        if not self.run_test(cmake_bin, options=cmake_args, purpose="Generate the Makefile"):
            tty.warn("Skipping kokkos test: failed to generate Makefile")
            return

        if not self.run_test("make", purpose="Build test software"):
            tty.warn("Skipping kokkos test: failed to build test")

    def run_tests(self, cmake_path):
        """Run test."""
        if not self.run_test(
            "make", options=[cmake_path, "test"], purpose="Checking ability to execute."
        ):
            tty.warn("Failed to run kokkos test")

    def test(self):
        # Skip if unsupported version
        cmake_path = join_path(
            self.test_suite.current_test_cache_dir, self.test_script_relative_path, "out"
        )

        if not os.path.exists(cmake_path):
            tty.warn("Skipping smoke tests: {0} is missing".format(cmake_path))
            return

        self.build_tests(cmake_path)
        self.run_tests(cmake_path)
