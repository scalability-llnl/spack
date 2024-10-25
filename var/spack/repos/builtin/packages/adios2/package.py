# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import tempfile

from spack.package import *


class Adios2(CMakePackage, CudaPackage, ROCmPackage):
    """The Adaptable Input Output System version 2,
    developed in the Exascale Computing Program"""

    homepage = "https://csmd.ornl.gov/software/adios2"
    url = "https://github.com/ornladios/ADIOS2/archive/v2.8.0.tar.gz"
    git = "https://github.com/ornladios/ADIOS2.git"
    test_requires_compiler = True

    maintainers("ax3l", "vicentebolea", "williamfgc")

    tags = ["e4s"]

    license("Apache-2.0")

    version("master", branch="master")
    version(
        "2.10.1",
        sha256="ce776f3a451994f4979c6bd6d946917a749290a37b7433c0254759b02695ad85",
        preferred=True,
    )
    version("2.10.0", sha256="e5984de488bda546553dd2f46f047e539333891e63b9fe73944782ba6c2d95e4")
    version("2.9.2", sha256="78309297c82a95ee38ed3224c98b93d330128c753a43893f63bbe969320e4979")
    version("2.9.1", sha256="ddfa32c14494250ee8a48ef1c97a1bf6442c15484bbbd4669228a0f90242f4f9")
    version("2.9.0", sha256="69f98ef58c818bb5410133e1891ac192653b0ec96eb9468590140f2552b6e5d1")
    version("2.8.3", sha256="4906ab1899721c41dd918dddb039ba2848a1fb0cf84f3a563a1179b9d6ee0d9f")
    version("2.8.2", sha256="9909f6409dc44b2c28c1fda0042dab4b711f25ec3277ef0cb6ffc40f5483910d")
    version("2.8.1", sha256="3f515b442bbd52e3189866b121613fe3b59edb8845692ea86fad83d1eba35d93")
    version("2.8.0", sha256="5af3d950e616989133955c2430bd09bcf6bad3a04cf62317b401eaf6e7c2d479")
    version("2.7.1", sha256="c8e237fd51f49d8a62a0660db12b72ea5067512aa7970f3fcf80b70e3f87ca3e")
    version("2.7.0", sha256="4b5df1a1f92d7ff380416dec7511cfcfe3dc44da27e486ed63c3e6cffb173924")
    version("2.6.0", sha256="45b41889065f8b840725928db092848b8a8b8d1bfae1b92e72f8868d1c76216c")
    version("2.5.0", sha256="7c8ff3bf5441dd662806df9650c56a669359cb0185ea232ecb3578de7b065329")
    version("2.4.0", sha256="50ecea04b1e41c88835b4b3fd4e7bf0a0a2a3129855c9cc4ba6cf6a1575106e2")
    version("2.3.1", sha256="3bf81ccc20a7f2715935349336a76ba4c8402355e1dc3848fcd6f4c3c5931893")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("fortran", type="build")

    # There's not really any consistency about how static and shared libs are
    # implemented across spack.  What we're trying to support is specifically three
    # library build types:
    #   shared (which is implicitly w/ pic)
    #     Implemented by +shared +pic
    #   static w/o pic
    #     Implemented by ~shared ~pic
    #   static w/ pic
    #     Implemented by ~shared +pic
    # shared w/o pic is not a valid configuration because shared libraries are Position
    # Independent # Code by design.  We're not inherently tied to this approach and can
    # change how we're supporting differnt library types in the package at anytime if
    # spack decides on a standardized way of doing it across packages
    variant("shared", default=True, when="+pic", description="Build shared libraries")

    # Features
    variant("mpi", default=True, description="Enable MPI")

    # Compression libraries
    variant(
        "libpressio", default=False, when="@2.8:", description="Enable LibPressio for compression"
    )
    variant("blosc", default=True, when="@2.4:2.8", description="Enable Blosc compression")
    variant("blosc2", default=True, when="@2.9:", description="Enable Blosc2 compression")
    variant("bzip2", default=True, when="@2.4:", description="Enable BZip2 compression")
    variant("zfp", default=True, description="Enable ZFP compression")
    variant("png", default=True, when="@2.4:", description="Enable PNG compression")
    variant("sz", default=True, description="Enable SZ compression")
    variant("mgard", default=True, when="@2.8:", description="Enable MGARD compression")

    # Rransport engines
    variant("sst", default=True, description="Enable the SST staging engine")
    variant(
        "dataman",
        default=False,
        when="+shared",
        description="Enable the DataMan engine for WAN transports",
    )
    variant("campaign", default=False, when="@2.10:", description="Enable campaign management")
    variant("dataspaces", default=False, when="@2.5:", description="Enable support for DATASPACES")
    variant("ssc", default=True, when="@:2.7", description="Enable the SSC staging engine")
    variant("hdf5", default=False, description="Enable the HDF5 engine")
    variant(
        "aws",
        default=False,
        when="@2.9:",
        description="Enable support for S3 compatible storage using AWS SDK's S3 module",
    )
    variant(
        "libcatalyst",
        default=True,
        when="@2.9:",
        description="Enable support for in situ visualization plugin using ParaView Catalyst",
    )

    # Optional language bindings, C++11 and C always provided
    variant("kokkos", default=False, when="@2.9:", description="Enable Kokkos support")
    variant("sycl", default=False, when="@2.10:", description="Enable SYCL support")
    variant("python", default=False, description="Enable the Python bindings")
    variant("fortran", default=True, description="Enable the Fortran bindings")

    # Requires mature C++11 implementations
    conflicts("%gcc@:4.7")
    conflicts("%intel@:15")
    conflicts("%pgi@:14")

    # ifx does not support submodules in separate files
    conflicts("%oneapi@:2022.1.0", when="+fortran")

    depends_on("cmake@3.12.0:", type="build")

    # Standalone CUDA support
    depends_on("cuda", when="+cuda ~kokkos")

    # Kokkos support
    with when("+kokkos"):
        depends_on("kokkos@3.7:")
        depends_on("kokkos +cuda +wrapper", when="+cuda")
        depends_on("kokkos +rocm", when="+rocm")
        depends_on("kokkos +sycl", when="+sycl")

    # Propagate CUDA target to kokkos for +cuda
    for cuda_arch in CudaPackage.cuda_arch_values:
        depends_on(
            "kokkos cuda_arch=%s" % cuda_arch, when="+kokkos +cuda cuda_arch=%s" % cuda_arch
        )

    # Propagate AMD GPU target to kokkos for +rocm
    for amdgpu_value in ROCmPackage.amdgpu_targets:
        depends_on(
            "kokkos amdgpu_target=%s" % amdgpu_value,
            when="+kokkos +rocm amdgpu_target=%s" % amdgpu_value,
        )

    conflicts("+cuda", when="@:2.7")
    conflicts("+rocm", when="@:2.8")

    conflicts("+cuda", when="+sycl")
    conflicts("+rocm", when="+cuda")
    conflicts("+rocm", when="+sycl")

    conflicts("+rocm", when="~kokkos", msg="ADIOS2 does not support HIP without Kokkos")
    conflicts("+sycl", when="~kokkos", msg="ADIOS2 does not support SYCL without Kokkos")

    for _platform in ["linux", "darwin"]:
        depends_on("pkgconfig", type="build", when=f"platform={_platform}")
        variant(
            "pic",
            default=False,
            description="Build pic-enabled static libraries",
            when=f"platform={_platform}",
        )
        # libffi and libfabric and not currently supported on Windows
        # see Paraview's superbuild handling of libfabric at
        # https://gitlab.kitware.com/paraview/paraview-superbuild/-/blob/master/projects/adios2.cmake#L3
        depends_on("libffi", when=f"+sst platform={_platform}")  # optional in DILL
        depends_on(
            "libfabric@1.6.0:", when=f"+sst platform={_platform}"
        )  # optional in EVPath and SST
        # depends_on('bison', when='+sst')     # optional in FFS, broken package
        # depends_on('flex', when='+sst')      # optional in FFS, depends on BISON

    depends_on("mpi", when="+mpi")
    depends_on("libzmq", when="+dataman")
    depends_on("dataspaces@1.8.0:", when="+dataspaces")

    depends_on("hdf5@:1.12", when="@:2.8 +hdf5")
    depends_on("hdf5~mpi", when="+hdf5~mpi")
    depends_on("hdf5+mpi", when="+hdf5+mpi")

    depends_on("sqlite@3", when="+campaign")

    depends_on("libpressio", when="+libpressio")
    depends_on("c-blosc", when="+blosc")
    depends_on("c-blosc2", when="+blosc2")
    depends_on("bzip2", when="+bzip2")
    depends_on("libpng@1.6:", when="+png")
    depends_on("zfp@0.5.1:0.5", when="+zfp")
    depends_on("sz@2.0.2.0:", when="+sz")
    depends_on("mgard", when="+mgard")

    extends("python", when="+python")
    depends_on("python@2.7:2.8,3.5:", when="@:2.4.0 +python", type=("build", "run"))
    depends_on("python@2.7:2.8,3.5:", when="@:2.4.0", type="test")
    depends_on("python@3.5:", when="@2.5.0: +python", type=("build", "run"))
    depends_on("python@3.5:", when="@2.5.0:", type="test")
    depends_on("py-numpy@1.6.1:", when="+python", type=("build", "run"))
    depends_on("py-mpi4py@2.0.0:", when="+mpi +python", type=("build", "run"))
    depends_on("aws-sdk-cpp", when="+aws")
    depends_on("libcatalyst@2", when="+libcatalyst")

    # Fix findmpi when called by dependees
    # See https://github.com/ornladios/ADIOS2/pull/1632
    patch("cmake-update-findmpi.patch", when="@2.4.0")

    # Fix the signature of the builtin clear_cache function in the
    # third-party dill library.
    # See https://github.com/ornladios/ADIOS2/pull/1899
    patch("2.5-fix-clear_cache.patch", when="@2.5.0")

    # Fix an unnecessary python dependency when testing is disabled
    # See https://github.com/ornladios/ADIOS2/pull/2596
    patch("2.7-fix-python-test-deps.patch", when="@2.5.0:2.7.0")

    # Fix unresolved symbols when built with gcc10.
    # See https://github.com/ornladios/ADIOS2/pull/2714
    patch("2.6-fix-gcc10-symbols.patch", when="@2.6.0")

    # add missing include <cstdint>
    patch("2.7-fix-missing-cstdint-include.patch", when="@2.7")

    # Add missing include <memory>
    # https://github.com/ornladios/adios2/pull/2710
    patch(
        "https://github.com/ornladios/adios2/pull/2710.patch?full_index=1",
        when="@:2.7.1",
        sha256="8221073d1b2f8944395a88a5d60a15c7370646b62f5fc6309867bbb6a8c2096c",
    )

    # Fix mismatched datatypes in comparison
    # See https://github.com/ornladios/ADIOS2/pull/2701
    patch("2.7.1-fix-broken-endian-reverse-compile.patch", when="@2.7.1")

    # cmake: find threads package first
    # https://github.com/ornladios/ADIOS2/pull/3893
    patch("2.9.2-cmake-find-threads-package-first.patch", when="@2.9")

    # ROCM: enable support for rocm >= 6
    # https://github.com/ornladios/ADIOS2/pull/4214
    patch("2.10-enable-rocm6.patch", when="@2.9.1:")

    @when("%fj")
    def patch(self):
        """add fujitsu mpi commands #16864"""
        f = join_path("cmake", "upstream", "FindMPI.cmake")
        filter_file("mpcc_r)", "mpcc_r mpifcc)", f, string=True)
        filter_file("mpc++_r)", "mpcc_r mpiFCC)", f, string=True)
        filter_file("mpf77_r", "mpf77_r mpifrt", f, string=True)

    def setup_build_environment(self, env):
        # https://github.com/ornladios/ADIOS2/issues/2228
        if self.spec.satisfies("%gcc@10: +fortran"):
            env.set("FFLAGS", "-fallow-argument-mismatch")
        elif self.spec.satisfies("%fj +fortran"):
            env.set("FFLAGS", "-Ccpp")

    def cmake_args(self):
        spec = self.spec
        from_variant = self.define_from_variant

        args = [
            from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            from_variant("BUILD_SHARED_LIBS", "shared"),
            from_variant("ADIOS2_USE_AWSSDK", "aws"),
            from_variant("ADIOS2_USE_Blosc", "blosc"),
            from_variant("ADIOS2_USE_Blosc2", "blosc2"),
            from_variant("ADIOS2_USE_BZip2", "bzip2"),
            from_variant("ADIOS2_USE_Campaign", "campaign"),
            from_variant("ADIOS2_USE_DataMan", "dataman"),
            from_variant("ADIOS2_USE_DataSpaces", "dataspaces"),
            from_variant("ADIOS2_USE_Fortran", "fortran"),
            from_variant("ADIOS2_USE_HDF5", "hdf5"),
            from_variant("ADIOS2_USE_MPI", "mpi"),
            from_variant("ADIOS2_USE_PNG", "png"),
            from_variant("ADIOS2_USE_Python", "python"),
            from_variant("ADIOS2_USE_SSC", "ssc"),
            from_variant("ADIOS2_USE_SST", "sst"),
            from_variant("ADIOS2_USE_SZ", "sz"),
            from_variant("ADIOS2_USE_ZFP", "zfp"),
            from_variant("ADIOS2_USE_Catalyst", "libcatalyst"),
            from_variant("ADIOS2_USE_LIBPRESSIO", "libpressio"),
            self.define("ADIOS2_USE_CUDA", self.spec.satisfies("+cuda ~kokkos")),
            self.define("ADIOS2_USE_Kokkos", self.spec.satisfies("+kokkos")),
            self.define("Kokkos_ENABLE_CUDA", self.spec.satisfies("+cuda +kokkos")),
            self.define("Kokkos_ENABLE_HIP", self.spec.satisfies("+rocm")),
            self.define("Kokkos_ENABLE_SYCL", self.spec.satisfies("+sycl")),
            self.define("BUILD_TESTING", self.run_tests),
            self.define("ADIOS2_BUILD_EXAMPLES", False),
            self.define("ADIOS2_USE_Endian_Reverse", True),
            self.define("ADIOS2_USE_IME", False),
            self.define("ADIOS2_USE_MGARD", False),
        ]

        if spec.satisfies("+sst"):
            args.extend(
                [
                    # Broken dependency package
                    "-DCMAKE_DISABLE_FIND_PACKAGE_BISON=TRUE",
                    # Depends on ^
                    "-DCMAKE_DISABLE_FIND_PACKAGE_FLEX=TRUE",
                    # Not yet packaged
                    "-DCMAKE_DISABLE_FIND_PACKAGE_CrayDRC=TRUE",
                    "-DCMAKE_DISABLE_FIND_PACKAGE_NVSTREAM=TRUE",
                ]
            )

        if spec.satisfies("%fj"):
            args.extend(["-DCMAKE_Fortran_SUBMODULE_EXT=.smod", "-DCMAKE_Fortran_SUBMODULE_SEP=."])

        # hip support
        if spec.satisfies("+cuda"):
            args.append(self.builder.define_cuda_architectures(self))

        # hip support
        if spec.satisfies("+rocm"):
            args.append(self.builder.define_hip_architectures(self))

        return args

    @property
    def libs(self):
        spec = self.spec
        libs_to_seek = set()

        if spec.satisfies("@2.6:"):
            libs_to_seek.add("libadios2_core")
            libs_to_seek.add("libadios2_c")
            libs_to_seek.add("libadios2_cxx11")
            if spec.satisfies("+fortran"):
                libs_to_seek.add("libadios2_fortran")

            if spec.satisfies("+mpi"):
                libs_to_seek.add("libadios2_core_mpi")
                libs_to_seek.add("libadios2_c_mpi")
                libs_to_seek.add("libadios2_cxx11_mpi")
                if spec.satisfies("+fortran"):
                    libs_to_seek.add("libadios2_fortran_mpi")

            if "@2.7: +shared+hdf5" in spec and "@1.12:" in spec["hdf5"]:
                libs_to_seek.add("libadios2_h5vol")

        else:
            libs_to_seek.add("libadios2")
            if spec.satisfies("+fortran"):
                libs_to_seek.add("libadios2_fortran")

        return find_libraries(
            list(libs_to_seek), root=self.spec.prefix, shared=("+shared" in spec), recursive=True
        )

    def setup_run_environment(self, env):
        try:
            all_libs = self.libs
            idx = all_libs.basenames.index("libadios2_h5vol.so")
            env.prepend_path("HDF5_PLUGIN_PATH", os.path.dirname(all_libs[idx]))
        except ValueError:
            pass

    @run_after("install")
    def setup_install_tests(self):
        """
        Copy the example files after the package is installed to an
        install test subdirectory for use during `spack test run`.
        """
        extra_install_tests = [join_path("testing", "install", "C")]
        cache_extra_test_sources(self, extra_install_tests)

    def test_run_executables(self):
        """Run installed adios2 executables"""

        commands_and_args = [("bpls", ["-v", "-V"]), ("adios2-config", ["-v"])]

        for cmd, opts in commands_and_args:
            with test_part(
                self,
                f"test_run_executables_{cmd}",
                purpose=f"run installed adios2 executable {cmd}",
            ):
                exe = which(join_path(self.prefix.bin, cmd))
                exe(*opts)

    def test_examples(self):
        """Build and run an example program"""
        src_dir = self.test_suite.current_test_cache_dir.testing.install.C
        test_stage_dir = self.test_suite.test_dir_for_spec(self.spec)

        # Create the build tree within this spec's test stage dir so it gets
        # cleaned up automatically
        build_dir = tempfile.mkdtemp(dir=test_stage_dir)

        std_cmake_args = []

        if self.spec.satisfies("+mpi"):
            mpi_exec = join_path(self.spec["mpi"].prefix, "bin", "mpiexec")
            std_cmake_args.append(f"-DMPIEXEC_EXECUTABLE={mpi_exec}")

        built_programs = ["adios_c_mpi_test", "adios_adios2c_test", "adios_c_test"]

        with working_dir(build_dir):
            with test_part(
                self, "test_examples_build", purpose="build example against installed adios2"
            ):
                cmake(src_dir, *std_cmake_args)
                make()

            for p in built_programs:
                exe = which(join_path(".", p))
                if exe:
                    with test_part(
                        self, f"test_examples_run_{p}", purpose=f"run built adios2 example {p}"
                    ):
                        exe()
