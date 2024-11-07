# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Legion(CMakePackage, ROCmPackage):
    """Legion is a data-centric parallel programming system for writing
    portable high performance programs targeted at distributed heterogeneous
    architectures. Legion presents abstractions which allow programmers to
    describe properties of program data (e.g. independence, locality). By
    making the Legion programming system aware of the structure of program
    data, it can automate many of the tedious tasks programmers currently
    face, including correctly extracting task- and data-level parallelism
    and moving data around complex memory hierarchies. A novel mapping
    interface provides explicit programmer controlled placement of data in
    the memory hierarchy and assignment of tasks to processors in a way
    that is orthogonal to correctness, thereby enabling easy porting and
    tuning of Legion applications to new architectures."""

    homepage = "https://legion.stanford.edu/"
    git = "https://github.com/StanfordLegion/legion.git"

    license("Apache-2.0")

    maintainers("pmccormick", "streichler", "elliottslaughter")
    tags = ["e4s"]
    version("24.09.0", tag="legion-24.09.0", commit="4a03402467547b99530042cfe234ceec2cd31b2e")
    version("24.06.0", tag="legion-24.06.0", commit="3f27977943626ef23038ef0049b7ad1b389caad1")
    version("24.03.0", tag="legion-24.03.0", commit="c61071541218747e35767317f6f89b83f374f264")
    version("23.12.0", tag="legion-23.12.0", commit="8fea67ee694a5d9fb27232a7976af189d6c98456")
    version("23.09.0", tag="legion-23.09.0", commit="7304dfcf9b69005dd3e65e9ef7d5bd49122f9b49")
    version("23.06.0", tag="legion-23.06.0", commit="7b5ff2fb9974511c28aec8d97b942f26105b5f6d")
    version("23.03.0", tag="legion-23.03.0", commit="12f6051c9d75229d00ac0b31d6be1ff2014f7e6a")
    version("22.12.0", tag="legion-22.12.0", commit="9ed6f4d6b579c4f17e0298462e89548a4f0ed6e5")
    version("22.09.0", tag="legion-22.09.0", commit="5b6e013ad74fa6b4c5a24cbb329c676b924550a9")
    version("22.06.0", tag="legion-22.06.0", commit="f721be968fb969339334b07a3175a0400700eced")
    version("22.03.0", tag="legion-22.03.0", commit="bf6ce4560c99397da4a5cf61a306b521ec7069d0")
    version("21.12.0", tag="legion-21.12.0", commit="e1443112edaa574804b3b9d2a24803e937b127fd")
    version("21.09.0", tag="legion-21.09.0", commit="5a991b714cf55c3eaa513c7a18abb436d86a0a90")
    version("21.06.0", tag="legion-21.06.0", commit="30e00fa6016527c4cf60025a461fb7865f8def6b")
    version("21.03.0", tag="legion-21.03.0", commit="0cf9ddd60c227c219c8973ed0580ddc5887c9fb2")
    version("stable", branch="stable")
    version("master", branch="master")

    # Old control replication commits used by FleCSI releases, prior to 24.03.0
    version("cr-20230307", commit="435183796d7c8b6ac1035a6f7af480ded750f67d", deprecated=True)
    version("cr-20210122", commit="181e63ad4187fbd9a96761ab3a52d93e157ede20", deprecated=True)
    version("cr-20191217", commit="572576b312509e666f2d72fafdbe9d968b1a6ac3", deprecated=True)

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("cmake@3.16:", type="build")
    # TODO: Need to spec version of MPI v3 for use of the low-level MPI transport
    # layer. At present the MPI layer is still experimental and we discourge its
    # use for general (not legion development) use cases.
    depends_on("mpi", when="network=mpi")
    depends_on("mpi", when="network=gasnet")  # MPI is required to build gasnet (needs mpicc).
    depends_on("ucx", when="network=ucx")
    depends_on("ucx", when="conduit=ucx")
    depends_on("mpi", when="conduit=mpi")
    depends_on("cuda@10.0:11.9", when="+cuda_unsupported_compiler @21.03.0:23.03.0")
    depends_on("cuda@10.0:11.9", when="+cuda @21.03.0:23.03.0")
    depends_on("cuda@10.0:", when="+cuda_unsupported_compiler")
    depends_on("cuda@10.0:", when="+cuda")
    depends_on("hip@5.1:5.7", when="+rocm @23.03.0:23.12.0")
    depends_on("hip@5.1:", when="+rocm")
    depends_on("hdf5", when="+hdf5")
    depends_on("hwloc", when="+hwloc")

    # cuda-centric
    cuda_arch_list = CudaPackage.cuda_arch_values
    for nvarch in cuda_arch_list:
        depends_on(
            f"kokkos@3.3.01:+cuda+cuda_lambda+wrapper cuda_arch={nvarch}",
            when=f"%gcc+kokkos+cuda cuda_arch={nvarch}",
        )
        depends_on(
            f"kokkos@3.3.01:+cuda+cuda_lambda~wrapper cuda_arch={nvarch}",
            when=f"%clang+kokkos+cuda cuda_arch={nvarch}",
        )

    depends_on("kokkos@3.3.01:~cuda", when="+kokkos~cuda")
    depends_on("kokkos@3.3.01:~cuda+openmp", when="+kokkos+openmp")

    # https://github.com/spack/spack/issues/37232#issuecomment-1553376552
    patch("hip-offload-arch.patch", when="@23.03.0 +rocm")

    def patch(self):
        if self.spec.satisfies(
            "network=gasnet conduit=ofi-slingshot11 ^[virtuals=mpi] cray-mpich+wrappers"
        ):
            filter_file(
                r"--with-mpi-cc=cc",
                f"--with-mpi-cc={self.spec['mpi'].mpicc}",
                "stanfordgasnet/gasnet/configs/config.ofi-slingshot11.release",
                string=True,
            )

    # HIP specific
    variant(
        "hip_hijack",
        default=False,
        description="Hijack application calls into the HIP runtime",
        when="+rocm",
    )
    variant(
        "hip_target",
        default="ROCM",
        values=("ROCM", "CUDA"),
        description="API used by HIP",
        multi=False,
        when="+rocm",
    )

    for arch in ROCmPackage.amdgpu_targets:
        depends_on(f"kokkos@3.3.01:+rocm amdgpu_target={arch}", when=f"+rocm amdgpu_target={arch}")

    depends_on("kokkos@3.3.01:+rocm", when="+kokkos+rocm")

    # https://github.com/StanfordLegion/legion/#dependencies
    depends_on("python@3.8:", when="+python")
    depends_on("py-cffi", when="+python")
    depends_on("py-numpy", when="+python")
    depends_on("py-pip", when="+python", type="build")
    depends_on("py-setuptools", when="+python", type="build")

    depends_on("papi", when="+papi")
    depends_on("zlib-api", when="+zlib")

    # A C++ standard variant to work-around some odd behaviors with apple-clang
    # but this might be helpful for other use cases down the road.  Legion's
    # current development policy is C++11 or greater so we capture that aspect
    # here.
    cpp_stds = (conditional("11", "14", when="@:24.03.0"), "17", "20")
    variant("cxxstd", default="17", description="C++ standard", values=cpp_stds, multi=False)

    # Network transport layer: the underlying data transport API should be used for
    # distributed data movement.  For Legion, gasnet is the currently the most
    # mature.  We have many users that default to using no network layer for
    # day-to-day development thus we default to 'none'.  MPI support is new and
    # should be considered as a beta release.
    variant(
        "network",
        default="none",
        values=("gasnet", "mpi", "ucx", "none"),
        description="The network communications/transport layer to use.",
        multi=False,
    )

    # Add Gasnet tarball dependency in spack managed manner
    # TODO: Provide less mutable tag instead of branch
    resource(
        name="stanfordgasnet",
        git="https://github.com/StanfordLegion/gasnet.git",
        destination="stanfordgasnet",
        branch="master",
        when="network=gasnet",
    )

    # We default to automatically embedding a gasnet build. To override this
    # point the package a pre-installed version of GASNet-Ex via the gasnet_root
    # variant.
    #
    # make sure we have a valid directory provided for gasnet_root...
    def validate_gasnet_root(value):
        if value == "none":
            return True

        if not os.path.isdir(value):
            print("gasnet_root:", value, "-- no such directory.")
            return False
        else:
            return True

    with when("network=gasnet"):
        variant(
            "gasnet_root",
            default="none",
            values=validate_gasnet_root,
            description="Path to a pre-installed version of GASNet (prefix directory).",
            multi=False,
        )
        variant(
            "conduit",
            default="none",
            values=("none", "aries", "ibv", "udp", "mpi", "ucx", "ofi-slingshot11"),
            description="The GASNet conduit(s) to enable.",
            sticky=True,
            multi=False,
        )
        conflicts(
            "conduit=none", msg="the 'conduit' variant must be set to a value other than 'none'"
        )
        variant("gasnet_debug", default=False, description="Build gasnet with debugging enabled.")

    variant("shared", default=False, description="Build shared libraries.")

    variant(
        "bounds_checks", default=False, description="Enable bounds checking in Legion accessors."
    )

    variant(
        "privilege_checks",
        default=False,
        description="Enable runtime privildge checks in Legion accessors.",
    )

    variant(
        "output_level",
        default="warning",
        # Note: these values are dependent upon those used in the cmake config.
        values=("spew", "debug", "info", "print", "warning", "error", "fatal", "none"),
        description="Set the compile-time logging level.",
        multi=False,
    )

    variant("spy", default=False, description="Enable detailed logging for Legion Spy debugging.")

    # note: we will be dependent upon spack's latest-and-greatest cuda version...
    variant("cuda", default=False, description="Enable CUDA support.")
    variant(
        "cuda_hijack",
        default=False,
        description="Hijack application calls into the CUDA runtime (+cuda).",
    )
    variant(
        "cuda_arch",
        default="70",
        values=cuda_arch_list,
        description="GPU/CUDA architecture to build for.",
        multi=False,
    )
    variant(
        "cuda_unsupported_compiler",
        default=False,
        description="Disable nvcc version check (--allow-unsupported-compiler).",
    )
    conflicts("+cuda_hijack", when="~cuda")

    variant("fortran", default=False, description="Enable Fortran bindings.")
    requires("+bindings", when="+fortran")

    variant("hdf5", default=False, description="Enable support for HDF5.")

    variant("hwloc", default=False, description="Use hwloc for topology awareness.")

    variant(
        "kokkos", default=False, description="Enable support for interoperability with Kokkos."
    )

    variant(
        "bindings", default=False, description="Build runtime language bindings (excl. Fortran)."
    )

    variant(
        "libdl", default=True, description="Enable support for dynamic object/library loading."
    )

    variant("openmp", default=False, description="Enable support for OpenMP within Legion tasks.")

    variant("papi", default=False, description="Enable PAPI performance measurements.")

    variant("python", default=False, description="Enable Python support.")
    requires("+bindings", when="+python")
    requires("+shared", when="+python")

    variant("zlib", default=True, description="Enable zlib support.")

    variant(
        "redop_complex", default=False, description="Use reduction operators for complex types."
    )
    requires("+redop_complex", when="+bindings")
    variant(
        "redop_half",
        default=False,
        description="Use reduction operators for half precision types.",
    )

    variant(
        "max_dims",
        values=int,
        default=3,
        description="Set max number of dimensions for logical regions.",
    )
    variant(
        "max_fields",
        values=int,
        default=512,
        description="Maximum number of fields allowed in a logical region.",
    )
    variant(
        "max_num_nodes",
        values=int,
        default=1024,
        description="Maximum number of nodes supported by Legion.",
    )
    variant("prof", default=False, description="Install Rust Legion prof")

    depends_on("rust@1.74:", type="build", when="+prof")

    variant("gc", default=False, description="Enable garbage collector logging")
    variant(
        "sysomp", default=False, description="Use system OpenMP implementation instead of Realm's"
    )

    def cmake_args(self):
        spec = self.spec
        from_variant = self.define_from_variant
        options = [from_variant("CMAKE_CXX_STANDARD", "cxxstd")]

        if spec.satisfies("network=gasnet"):
            options.append("-DLegion_NETWORKS=gasnetex")
            if spec.variants["gasnet_root"].value != "none":
                gasnet_dir = spec.variants["gasnet_root"].value
                options.append("-DGASNet_ROOT_DIR=%s" % gasnet_dir)
            else:
                gasnet_dir = join_path(self.stage.source_path, "stanfordgasnet", "gasnet")
                options.append("-DLegion_EMBED_GASNet=ON")
                options.append("-DLegion_EMBED_GASNet_LOCALSRC=%s" % gasnet_dir)

            gasnet_conduit = spec.variants["conduit"].value

            if "-" in gasnet_conduit:
                gasnet_conduit, gasnet_system = gasnet_conduit.split("-")
                options.append("-DGASNet_CONDUIT=%s" % gasnet_conduit)
                options.append("-DGASNet_SYSTEM=%s" % gasnet_system)
            else:
                options.append("-DGASNet_CONDUIT=%s" % gasnet_conduit)

            if spec.satisfies("+gasnet_debug"):
                options.append("-DLegion_EMBED_GASNet_CONFIGURE_ARGS=--enable-debug")
        elif spec.satisfies("network=mpi"):
            options.append("-DLegion_NETWORKS=mpi")
        elif spec.satisfies("network=ucx"):
            options.append("-DLegion_NETWORKS=ucx")
        else:
            options.append("-DLegion_EMBED_GASNet=OFF")

        if spec.satisfies("+shared"):
            options.append("-DBUILD_SHARED_LIBS=ON")
        else:
            options.append("-DBUILD_SHARED_LIBS=OFF")

        if spec.satisfies("+bounds_checks"):
            # default is off.
            options.append("-DLegion_BOUNDS_CHECKS=ON")
        if spec.satisfies("+privilege_checks"):
            # default is off.
            options.append("-DLegion_PRIVILEGE_CHECKS=ON")

        options.append(f"-DLegion_OUTPUT_LEVEL={str.upper(spec.variants['output_level'].value)}")

        if spec.satisfies("+spy"):
            # default is off.
            options.append("-DLegion_SPY=ON")

        if spec.satisfies("+cuda"):
            cuda_arch = spec.variants["cuda_arch"].value
            options.append("-DLegion_USE_CUDA=ON")
            options.append("-DLegion_GPU_REDUCTIONS=ON")
            options.append("-DLegion_CUDA_ARCH=%s" % cuda_arch)
            if spec.satisfies("+cuda_hijack"):
                options.append("-DLegion_HIJACK_CUDART=ON")
            else:
                options.append("-DLegion_HIJACK_CUDART=OFF")

            if spec.satisfies("+cuda_unsupported_compiler"):
                options.append("-DCUDA_NVCC_FLAGS:STRING=--allow-unsupported-compiler")

        if spec.satisfies("+rocm"):
            options.append("-DLegion_USE_HIP=ON")
            options.append("-DLegion_GPU_REDUCTIONS=ON")
            options.append(from_variant("Legion_HIP_TARGET", "hip_target"))
            options.append(from_variant("Legion_HIP_ARCH", "amdgpu_target"))
            options.append(from_variant("Legion_HIJACK_HIP", "hip_hijack"))
            if spec.satisfies("@23.03.0:23.12.0"):
                options.append(self.define("HIP_PATH", f"{spec['hip'].prefix}/hip"))
            else:
                options.append(self.define("ROCM_PATH", spec["hip"].prefix))

        if spec.satisfies("+fortran"):
            # default is off.
            options.append("-DLegion_USE_Fortran=ON")

        if spec.satisfies("+hdf5"):
            # default is off.
            options.append("-DLegion_USE_HDF5=ON")

        if spec.satisfies("+hwloc"):
            # default is off.
            options.append("-DLegion_USE_HWLOC=ON")

        if spec.satisfies("+kokkos"):
            # default is off.
            options.append("-DLegion_USE_Kokkos=ON")
            os.environ["KOKKOS_CXX_COMPILER"] = spec["kokkos"].kokkos_cxx
            if spec.satisfies("+cuda+cuda_unsupported_compiler ^kokkos%clang +cuda"):
                # Keep CMake CUDA compiler detection happy
                options.append(
                    self.define("CMAKE_CUDA_FLAGS", "--allow-unsupported-compiler -std=c++17")
                )

        if spec.satisfies("+libdl"):
            # default is on.
            options.append("-DLegion_USE_LIBDL=ON")
        else:
            options.append("-DLegion_USE_LIBDL=OFF")

        if spec.satisfies("+openmp"):
            # default is off.
            options.append("-DLegion_USE_OpenMP=ON")

        if spec.satisfies("+papi"):
            # default is off.
            options.append("-DLegion_USE_PAPI=ON")

        if spec.satisfies("+python"):
            # default is off.
            options.append("-DLegion_USE_Python=ON")

        if spec.satisfies("+zlib"):
            # default is on.
            options.append("-DLegion_USE_ZLIB=ON")
        else:
            options.append("-DLegion_USE_ZLIB=OFF")

        if spec.satisfies("+bindings"):
            # default is off.
            options.append("-DLegion_BUILD_BINDINGS=ON")

        if spec.satisfies("+redop_complex"):
            # default is off
            options.append("-DLegion_REDOP_COMPLEX=ON")

        if spec.satisfies("+redop_half"):
            # default is off
            options.append("-DLegion_REDOP_HALF=ON")

        maxdims = int(spec.variants["max_dims"].value)
        # TODO: sanity check if maxdims < 0 || > 9???
        options.append("-DLegion_MAX_DIM=%d" % maxdims)

        maxfields = int(spec.variants["max_fields"].value)
        if maxfields <= 0:
            maxfields = 512
        # make sure maxfields is a power of two.  if not,
        # find the next largest power of two and use that...
        if maxfields & (maxfields - 1) != 0:
            while maxfields & maxfields - 1:
                maxfields = maxfields & maxfields - 1
            maxfields = maxfields << 1
        options.append("-DLegion_MAX_FIELDS=%d" % maxfields)

        maxnodes = int(spec.variants["max_num_nodes"].value)
        if maxnodes <= 0:
            maxnodes = 1024
        # make sure maxnodes is a power of two.  if not,
        # find the next largest power of two and use that...
        if maxnodes & (maxnodes - 1) != 0:
            while maxnodes & maxnodes - 1:
                maxnodes = maxnodes & maxnodes - 1
            maxnodes = maxnodes << 1
        options.append("-DLegion_MAX_NUM_NODES=%d" % maxnodes)

        # This disables Legion's CMake build system's logic for targeting the native
        # CPU architecture in favor of Spack-provided compiler flags
        options.append("-DBUILD_MARCH:STRING=")

        if spec.satisfies("+openmp +sysomp"):
            options.append("-DLegion_OpenMP_SYSTEM_RUNTIME=ON")

        if spec.satisfies("+gc"):
            options.append("-DCMAKE_CXX_FLAGS=-DLEGION_GC")

        return options

    def build(self, spec, prefix):
        super().build(spec, prefix)
        if spec.satisfies("+prof"):
            with working_dir(join_path(self.stage.source_path, "tools", "legion_prof_rs")):
                cargo = which("cargo")
                cargo("install", "--root", "out", "--path", ".", "--all-features", "--locked")

    def install(self, spec, prefix):
        super().install(spec, prefix)
        if spec.satisfies("+prof"):
            with working_dir(join_path(self.stage.source_path, "tools", "legion_prof_rs")):
                install_tree("out", prefix)

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, [join_path("examples", "local_function_tasks")])

    def test_run_local_function_tasks(self):
        """Build and run external application example"""

        test_dir = join_path(
            self.test_suite.current_test_cache_dir, "examples", "local_function_tasks"
        )

        if not os.path.exists(test_dir):
            raise SkipTest(f"{test_dir} must exist")

        cmake_args = [
            f"-DCMAKE_C_COMPILER={self.compiler.cc}",
            f"-DCMAKE_CXX_COMPILER={self.compiler.cxx}",
            f"-DLegion_DIR={join_path(self.prefix, 'share', 'Legion', 'cmake')}",
        ]

        with working_dir(test_dir):
            cmake = self.spec["cmake"].command
            cmake(*cmake_args)

            make = which("make")
            make()

            exe = which("local_function_tasks")
            exe()
