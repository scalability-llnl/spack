# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flecsi(CMakePackage, CudaPackage, ROCmPackage):
    """FleCSI is a compile-time configurable framework designed to support
    multi-physics application development. As such, FleCSI attempts to
    provide a very general set of infrastructure design patterns that can
    be specialized and extended to suit the needs of a broad variety of
    solver and data requirements. Current support includes multi-dimensional
    mesh topology, mesh geometry, and mesh adjacency information.
    """

    homepage = "http://flecsi.org/"
    git = "https://github.com/flecsi/flecsi.git"
    maintainers("rbberger", "opensdh")

    tags = ["e4s"]

    version("develop", branch="develop", deprecated=True)
    version("2.3.0", tag="v2.3.0", commit="90bc8267fceb02060e54646f73b45d4252aef491")
    version("2.2.1", tag="v2.2.1", commit="84b5b232aebab40610f57387778db80f6c8c84c5")
    version("2.2.0", tag="v2.2.0", commit="dd531ac16c5df124d76e385c6ebe9b9589c2d3ad")
    version("2.1.0", tag="v2.1.0", commit="533df139c267e2a93c268dfe68f9aec55de11cf0")
    version("2.0.0", tag="v2.0.0", commit="5ceebadf75d1c98999ea9e9446926722d061ec22")

    variant(
        "backend",
        default="mpi",
        values=("mpi", "legion", "hpx"),
        description="Backend to use for distributed memory",
        multi=False,
    )
    variant("shared", default=True, description="Build shared libraries")
    variant("flog", default=False, description="Enable logging support")
    variant("graphviz", default=False, description="Enable GraphViz Support")
    variant("doc", default=False, description="Enable documentation", when="@2.2:")
    variant("hdf5", default=True, description="Enable HDF5 Support")
    variant(
        "caliper_detail",
        default="none",
        values=("none", "low", "medium", "high"),
        description="Set Caliper Profiling Detail",
        multi=False,
    )
    variant("kokkos", default=False, description="Enable Kokkos Support")
    variant("openmp", default=False, description="Enable OpenMP Support")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    # All Current FleCSI Releases
    for level in ("low", "medium", "high"):
        depends_on("caliper@:2.5,2.8:", when=f"caliper_detail={level}")

    depends_on("graphviz", when="+graphviz")
    depends_on("hdf5+hl+mpi", when="+hdf5")
    depends_on("metis@5.1.0:")
    depends_on("parmetis@4.0.3:")
    depends_on("boost@1.70.0: cxxstd=17 +program_options +stacktrace")

    depends_on("cmake@3.15:")
    depends_on("cmake@3.19:", when="@2.2:")
    depends_on("cmake@3.23:", when="@2.3:")
    depends_on("boost +atomic +filesystem +regex +system", when="@:2.2.1")
    depends_on("boost@1.79.0:", when="@2.2:")
    depends_on("kokkos@3.2.00:", when="+kokkos")
    depends_on("kokkos@3.7:", when="+kokkos @2.3:")
    depends_on("kokkos +cuda +cuda_constexpr +cuda_lambda", when="+kokkos +cuda")
    depends_on("kokkos +rocm", when="+kokkos +rocm")
    depends_on("kokkos +openmp", when="+kokkos +openmp")
    depends_on("legion@cr-20210122", when="backend=legion @2.0:2.2.1")
    depends_on("legion@cr-20230307", when="backend=legion @2.2.0:2.2.1")
    depends_on("legion@24.03.0:", when="backend=legion @2.2.2:")
    depends_on("legion+shared", when="backend=legion +shared")
    depends_on("legion+hdf5", when="backend=legion +hdf5")
    depends_on("legion+kokkos", when="backend=legion +kokkos")
    depends_on("legion+openmp", when="backend=legion +openmp")
    depends_on("legion+cuda", when="backend=legion +cuda")
    depends_on("legion+rocm", when="backend=legion +rocm")
    depends_on("hdf5@1.10.7:", when="backend=legion +hdf5")
    depends_on("hpx@1.10.0: cxxstd=17 malloc=system", when="backend=hpx")
    depends_on("mpi")
    depends_on("mpich@3.4.1:", when="^[virtuals=mpi] mpich")
    depends_on("openmpi@4.1.0:", when="^[virtuals=mpi] openmpi")
    depends_on("graphviz@2.49.0:", when="+graphviz @2.3:")

    # FleCSI 2.2+ documentation dependencies
    depends_on("py-sphinx", when="+doc")
    depends_on("py-sphinx-rtd-theme", when="+doc")
    depends_on("py-recommonmark", when="@:2.2 +doc")
    depends_on("doxygen", when="+doc")
    depends_on("graphviz", when="+doc")

    # Propagate cuda_arch requirement to dependencies
    for _flag in CudaPackage.cuda_arch_values:
        depends_on(f"kokkos cuda_arch={_flag}", when=f"+cuda+kokkos cuda_arch={_flag}")
        depends_on(f"legion cuda_arch={_flag}", when=f"backend=legion +cuda cuda_arch={_flag}")

    # Propagate amdgpu_target requirement to dependencies
    for _flag in ROCmPackage.amdgpu_targets:
        depends_on(f"kokkos amdgpu_target={_flag}", when=f"+kokkos +rocm amdgpu_target={_flag}")
        depends_on(
            f"legion amdgpu_target={_flag}", when=f"backend=legion +rocm amdgpu_target={_flag}"
        )

    requires("%gcc@9:", when="%gcc", msg="Version 9 or newer of GNU compilers required!")

    # Disallow conduit=none when using legion as a backend
    conflicts("^legion conduit=none", when="backend=legion")
    conflicts("+hdf5", when="backend=hpx", msg="HPX backend doesn't support HDF5")

    def cmake_args(self):
        spec = self.spec

        if spec.satisfies("@2.2:"):
            options = [
                self.define_from_variant("FLECSI_BACKEND", "backend"),
                self.define_from_variant("CALIPER_DETAIL", "caliper_detail"),
                self.define_from_variant("ENABLE_FLOG", "flog"),
                self.define_from_variant("ENABLE_GRAPHVIZ", "graphviz"),
                self.define_from_variant("ENABLE_HDF5", "hdf5"),
                self.define_from_variant("ENABLE_KOKKOS", "kokkos"),
                self.define_from_variant("ENABLE_OPENMP", "openmp"),
                self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
                self.define("ENABLE_UNIT_TESTS", self.run_tests),
                self.define_from_variant("ENABLE_DOCUMENTATION", "doc"),
            ]

            if self.spec.satisfies("+rocm"):
                options.append(self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc))
                options.append(self.define("CMAKE_C_COMPILER", self.spec["hip"].hipcc))
                if self.spec.satisfies("backend=legion"):
                    # CMake pulled in via find_package(Legion) won't work without this
                    options.append(self.define("HIP_PATH", "{0}/hip".format(spec["hip"].prefix)))
            elif self.spec.satisfies("+kokkos"):
                options.append(self.define("CMAKE_CXX_COMPILER", self.spec["kokkos"].kokkos_cxx))
        else:
            # kept for supporing version prior to 2.2
            options = [
                self.define_from_variant("FLECSI_RUNTIME_MODEL", "backend"),
                self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
                self.define_from_variant("CALIPER_DETAIL", "caliper_detail"),
                self.define_from_variant("ENABLE_GRAPHVIZ", "graphviz"),
                self.define_from_variant("ENABLE_KOKKOS", "kokkos"),
                self.define_from_variant("ENABLE_OPENMP", "openmp"),
                self.define_from_variant("ENABLE_DOXYGEN", "doc"),
                self.define_from_variant("ENABLE_FLOG", "flog"),
                self.define("ENABLE_MPI", True),
                self.define("ENABLE_UNIT_TESTS", self.run_tests),
                self.define_from_variant("ENABLE_HDF5", "hdf5"),
            ]

            if spec.variants["backend"].value == "hpx":
                options.append(self.define("HPX_IGNORE_CMAKE_BUILD_TYPE_COMPATIBILITY", True))

        return options
