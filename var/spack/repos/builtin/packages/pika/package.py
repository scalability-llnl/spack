# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import sys

from spack.package import *


class Pika(CMakePackage, CudaPackage, ROCmPackage):
    """C++ runtime system for parallellism and concurrency."""

    homepage = "https://github.com/pika-org/pika/"
    url = "https://github.com/pika-org/pika/archive/0.0.0.tar.gz"
    git = "https://github.com/pika-org/pika.git"
    maintainers("msimberg", "albestro", "teonnik", "aurianer")

    license("BSL-1.0")

    version("0.29.0", sha256="2c61079f52f3e135a8d0845a993e6e4fb64031fbee9b5cef0ead57efb6175e3c")
    version("0.28.0", sha256="a64ebac04135c0c8d392ddcd8d683fe02e2c0782abfe130754244d58f27ae6cf")
    version("0.27.0", sha256="4a58dc4014edc2074399e4a6ecfa244537c89ce1319b3e14ff3dfe617fb9f9e8")
    version("0.26.1", sha256="d7cc842238754019abdb536e22325e9a57186cd2ac8cc9c7140a5385f9d730f6")
    version("0.26.0", sha256="bbec5472c71006c1f55e7946c8dc517dae76c41cacb36fa98195312c74a1bb9a")
    version("0.25.0", sha256="6646e12f88049116d84ce0caeedaa039a13caaa0431964caea4660b739767b2e")
    version("0.24.0", sha256="3b97c684107f892a633f598d94bcbd1e238d940e88e1c336f205e81b99326cc3")
    version("0.23.0", sha256="d1981e198ac4f8443770cebbeff7a132b8f6c1a42e32b0b06fea02cc9df99595")
    version("0.22.2", sha256="eeffa8584336b239aca167f0056e815b1b6d911e46cbb3cd6b8b811d101c1052")
    version("0.22.1", sha256="b0de0649bee336847622f97b59b34a80cb3cfd9a931bbdb38299bc4904f19b92")
    version("0.22.0", sha256="75f8932f3a233958c69802b483335eeeb39032ea66f12442f6f77048e259bdea")
    version("0.21.0", sha256="0ab24966e6ae026b355147f02354af4bd2117c342915fe844addf8e493735a33")
    version("0.20.0", sha256="f338cceea66a0e3954806b2aca08f6560bba524ecea222f04bc18b483851c877")
    version("0.19.1", sha256="674675abf0dd4c6f5a0b2fa3db944b277ed65c62f654029d938a8cab608a9c1d")
    version("0.19.0", sha256="f45cc16e4e50cbb183ed743bdc8b775d49776ee33c13ea39a650f4230a5744cb")
    version("0.18.0", sha256="f34890e0594eeca6ac57f2b988d0807b502782817e53a7f7043c3f921b08c99f")
    version("0.17.0", sha256="717429fc1bc986d62cbec190a69939e91608122d09d54bda1b028871c9ca9ad4")
    version("0.16.0", sha256="59f2baec91cc9bf71ca96d21d0da1ec0092bf59da106efa51789089e0d7adcbb")
    version("0.15.1", sha256="b68b87cf956ad1448f5c2327a72ba4d9fb339ecabeabb0a87b8ea819457e293b")
    version("0.15.0", sha256="4ecd5b64bd8067283a161e1aeacfbab7658d89fe1504b788fd3236298fe66b00")
    version("0.14.0", sha256="c0fc10a3c2c24bccbdc292c22a3373a2ad579583ee9d8bd31aaf1755e49958a4")
    version("0.13.0", sha256="67e0843141fb711787e71171a7a669c9cdb9587e4afd851ee2b0339a62b9a254")
    version("0.12.0", sha256="daa1422eb73d6a897ce7b8ff8022e09e7b0fec83d92728ed941a92e57dec5da3")
    version("0.11.0", sha256="3c3d94ca1a3960884bad7272bb9434d61723f4047ebdb097fcf522c6301c3fda")
    version("0.10.0", sha256="3b443b8f0f75b9a558accbaef0334a113a71b0205770e6c7ff02ea2d7c6aca5b")
    version("0.9.0", sha256="c349b2a96476d6974d2421288ca4d2e14ef9e5897d44cd7d5343165faa2d1299")
    version("0.8.0", sha256="058e82d7c8f95badabe52bbb4682d55aadf340d67ced1226c0673b4529adc182")
    version("0.7.0", sha256="e1bf978c88515f7af28ee47f98b795ffee521c15b39877ea4cfb405f31d507ed")
    version("0.6.0", sha256="cb4ebd7b92da39ec4df7b0d05923b94299d6ee2f2f49752923ffa2266ca76568")
    version("0.5.0", sha256="c43de7e92d04bea0ce59716756ef5f3a5a54f9e4affed872c1468632ad855f7c")
    version("0.4.0", sha256="31084a0a61103ee9574aaa427f879682e3e37cb11e8d147f2649949bee324591")
    version("0.3.0", sha256="bbb89f9824c58154ed59e2e14276c0ad132fd7b90b2be64ddd0e284f3b57cc0f")
    version("0.2.0", sha256="712bb519f22bdc9d5ee4ac374d251a54a0af4c9e4e7f62760b8ab9a177613d12")
    version("0.1.0", sha256="aa0ae2396cd264d821a73c4c7ecb118729bb3de042920c9248909d33755e7327")
    version("main", branch="main")

    depends_on("cxx", type="build")

    generator("ninja")

    variant("shared", default=True, description="Build shared libraries")
    conflicts("~shared", when="@:0.25")

    cxxstds = ("17", "20", "23")
    variant(
        "cxxstd",
        default="17",
        values=cxxstds,
        description="Use the specified C++ standard when building",
    )

    mallocs = ("system", "jemalloc", "mimalloc", "tbbmalloc", "tcmalloc")
    variant(
        "malloc",
        default="mimalloc",
        description="Define which allocator will be linked in",
        values=mallocs,
    )

    default_generic_coroutines = True
    if sys.platform.startswith("linux") or sys.platform == "win32":
        default_generic_coroutines = False
    variant(
        "generic_coroutines",
        default=default_generic_coroutines,
        description="Use Boost.Context as the underlying coroutines"
        " context switch implementation",
    )

    variant("examples", default=False, description="Build and install examples")
    variant("mpi", default=False, description="Enable MPI support")
    variant("apex", default=False, description="Enable APEX support", when="@0.2:")
    variant("tracy", default=False, description="Enable Tracy support", when="@0.7:")
    variant(
        "sanitizers",
        default=False,
        description="Enable support for sanitizers. "
        "Specific sanitizers must be explicitly enabled with -fsanitize=*.",
    )
    variant("valgrind", default=False, description="Enable support for valgrind")
    variant(
        "stdexec",
        default=False,
        description="Use stdexec for sender/receiver functionality",
        when="@0.9:",
    )

    # Build dependencies
    depends_on("cmake@3.18:", type="build")
    depends_on("cmake@3.22:", when="@0.8:", type="build")

    conflicts("%gcc@:6")
    conflicts("%clang@:6")
    # Pika is requiring the std::filesystem support starting from version 0.2.0
    conflicts("%gcc@:8", when="@0.2:")
    conflicts("%clang@:8", when="@0.2:")
    conflicts("+stdexec", when="cxxstd=17")
    conflicts("cxxstd=23", when="^cmake@:3.20.2")
    # nvcc version <= 11 does not support C++20 and newer
    for cxxstd in filter(lambda x: x != "17", cxxstds):
        requires("%nvhpc", when=f"cxxstd={cxxstd} ^cuda@:11")

    # Other dependencies
    depends_on("boost@1.71:")
    depends_on("fmt@9:", when="@0.11:")
    # https://github.com/pika-org/pika/issues/686
    conflicts("^fmt@10:", when="@:0.15 +cuda")
    conflicts("^fmt@10:", when="@:0.15 +rocm")
    # https://github.com/pika-org/pika/pull/1074
    conflicts("^fmt@11:", when="@:0.23")
    depends_on("spdlog@1.9.2:", when="@0.25:")
    depends_on("hwloc@1.11.5:")
    # https://github.com/pika-org/pika/issues/1223
    conflicts("^hwloc@2.11:", when="@:0.27 target=aarch64:")

    depends_on("gperftools", when="malloc=tcmalloc")
    depends_on("jemalloc", when="malloc=jemalloc")
    depends_on("mimalloc", when="malloc=mimalloc")
    depends_on("tbb", when="malloc=tbbmalloc")
    for malloc in filter(lambda x: x != "system", mallocs):
        conflicts("^apex +gperftools", when=f"+apex malloc={malloc}")
        conflicts("^apex +jemalloc", when=f"+apex malloc={malloc}")

    depends_on("apex", when="+apex")
    depends_on("cuda@11:", when="+cuda")
    depends_on("hip@5.2:", when="@0.8: +rocm")
    # https://github.com/pika-org/pika/issues/1238
    conflicts("%gcc@13:", when="+rocm")
    depends_on("hipblas", when="@:0.8 +rocm")
    depends_on("mpi", when="+mpi")
    with when("+stdexec"):
        depends_on("stdexec")
        depends_on("stdexec@24.09:", when="@0.29:")
    depends_on("rocblas", when="+rocm")
    depends_on("rocsolver", when="@0.5: +rocm")
    depends_on("tracy-client", when="+tracy")
    conflicts("^tracy-client@0.9:", when="@:0.9")
    depends_on("whip@0.1: +rocm", when="@0.9: +rocm")
    depends_on("whip@0.1: +cuda", when="@0.9: +cuda")

    depends_on("valgrind", when="+valgrind")

    with when("+rocm"):
        for val in ROCmPackage.amdgpu_targets:
            depends_on(f"whip@0.1: amdgpu_target={val}", when=f"@0.9: amdgpu_target={val}")
            depends_on(f"rocsolver amdgpu_target={val}", when=f"@0.5: amdgpu_target={val}")
            depends_on(f"rocblas amdgpu_target={val}", when=f"amdgpu_target={val}")

    with when("+cuda"):
        for val in CudaPackage.cuda_arch_values:
            depends_on(f"whip@0.1: cuda_arch={val}", when=f"@0.9: cuda_arch={val}")

    for cxxstd in cxxstds:
        depends_on(f"boost cxxstd={cxxstd}", when=f"cxxstd={cxxstd}")
        depends_on(f"fmt cxxstd={cxxstd}", when=f"@0.11: cxxstd={cxxstd}")

    # COROUTINES
    # ~generic_coroutines conflict is not fully implemented
    # for additional information see:
    # https://github.com/spack/spack/pull/17654
    # https://github.com/STEllAR-GROUP/hpx/issues/4829
    depends_on("boost+context", when="+generic_coroutines")
    depends_on("boost+atomic+chrono+thread", when="@:0.3.0+generic_coroutines")
    _msg_generic_coroutines = "This platform requires +generic_coroutines"
    conflicts("~generic_coroutines", when="platform=darwin", msg=_msg_generic_coroutines)

    # Patches
    patch("transform_mpi_includes.patch", when="@0.3.0 +mpi")
    patch("mimalloc_no_version_requirement.patch", when="@:0.5 malloc=mimalloc")
    patch("generic_context_allocate_guard_0_13_14.patch", when="@0.13:0.14 platform=darwin")
    patch("generic_context_allocate_guard_0_10_12.patch", when="@0.10:0.12 platform=darwin")
    patch("posix_stack_non_executable_0_13.patch", when="@0.13 platform=darwin")
    patch("posix_stack_non_executable_0_6_0_12.patch", when="@0.6:0.12 platform=darwin")
    patch("posix_stack_non_executable_0_1_0_5.patch", when="@:0.5 platform=darwin")

    # Fix missing template instantiation on macOS
    patch(
        "https://github.com/pika-org/pika/commit/dd1dfb85781ec2e76fa37ce7311323e69fbe42a1.patch?full_index=1",
        sha256="2944f746f5ae4385aba11b7c4a2f991abc108b08ea3dc394bf61c20fc7a2c4f2",
        when="@0.7.0 platform=darwin",
    )

    # Fix constexpr/fmt bug on macOS
    # Upstream patch is
    # https://github.com/pika-org/pika/commit/33655188fe4b9bcfad1e98a05e9ebcc22afc7ef8.patch,
    # but it requires changes to apply to 0.11.0.
    patch("thread_id_fmt.patch", when="@0.11 platform=darwin")

    def cmake_args(self):
        spec, args = self.spec, []

        args += [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("PIKA_WITH_CXX_STANDARD", spec.variants["cxxstd"].value),
            self.define_from_variant("PIKA_WITH_EXAMPLES", "examples"),
            self.define_from_variant("PIKA_WITH_MALLOC", "malloc"),
            self.define_from_variant("PIKA_WITH_CUDA", "cuda"),
            self.define_from_variant("PIKA_WITH_HIP", "rocm"),
            self.define_from_variant("PIKA_WITH_MPI", "mpi"),
            self.define_from_variant("PIKA_WITH_APEX", "apex"),
            self.define_from_variant("PIKA_WITH_TRACY", "tracy"),
            self.define_from_variant("PIKA_WITH_SANITIZERS", "sanitizers"),
            self.define_from_variant("PIKA_WITH_VALGRIND", "valgrind"),
            self.define("PIKA_WITH_TESTS", self.run_tests),
            self.define_from_variant("PIKA_WITH_GENERIC_CONTEXT_COROUTINES", "generic_coroutines"),
            self.define("BOOST_ROOT", spec["boost"].prefix),
            self.define("HWLOC_ROOT", spec["hwloc"].prefix),
        ]

        if spec.satisfies("@0.14:"):
            args.append(self.define_from_variant("PIKA_WITH_STDEXEC", "stdexec"))
        else:
            args.append(
                self.define_from_variant("PIKA_WITH_P2300_REFERENCE_IMPLEMENTATION", "stdexec")
            )

        # HIP support requires compiling with hipcc for < 0.8.0
        if spec.satisfies("@:0.7 +rocm"):
            args.append(self.define("CMAKE_CXX_COMPILER", spec["hip"].hipcc))
            if spec.satisfies("^cmake@3.21.0:3.21.2"):
                args.append(self.define("__skip_rocmclang", True))
        if spec.satisfies("@0.8: +rocm"):
            rocm_archs = spec.variants["amdgpu_target"].value
            if "none" not in rocm_archs:
                rocm_archs = ";".join(rocm_archs)
                args.append(self.define("CMAKE_HIP_ARCHITECTURES", rocm_archs))

        return args
