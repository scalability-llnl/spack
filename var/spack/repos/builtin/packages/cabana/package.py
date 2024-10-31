# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.kokkos import Kokkos


class Cabana(CMakePackage, CudaPackage, ROCmPackage):
    """The Exascale Co-Design Center for Particle Applications Toolkit"""

    homepage = "https://github.com/ECP-copa/Cabana"
    git = "https://github.com/ECP-copa/Cabana.git"
    url = "https://github.com/ECP-copa/Cabana/archive/0.7.0.tar.gz"

    maintainers("junghans", "streeve", "sslattery")

    tags = ["e4s", "ecp"]

    version("master", branch="master")
    version("0.7.0", sha256="3d46532144ea9a3f36429a65cccb7562d1244f1389dd8aff0d253708d1ec9838")
    version("0.6.1", sha256="fea381069fe707921831756550a665280da59032ea7914f7ce2a01ed467198bc")
    version("0.6.0", sha256="a88a3f80215998169cdbd37661c0c0af57e344af74306dcd2b61983d7c69e6e5")
    version("0.5.0", sha256="b7579d44e106d764d82b0539285385d28f7bbb911a572efd05c711b28b85d8b1")
    version("0.4.0", sha256="c347d23dc4a5204f9cc5906ccf3454f0b0b1612351bbe0d1c58b14cddde81e85")
    version("0.3.0", sha256="fb67ab9aaf254b103ae0eb5cc913ddae3bf3cd0cf6010e9686e577a2981ca84f")
    version("0.2.0", sha256="3e0c0e224e90f4997f6c7e2b92f00ffa18f8bcff72f789e0908cea0828afc2cb")
    version("0.1.0", sha256="3280712facf6932b9d1aff375b24c932abb9f60a8addb0c0a1950afd0cb9b9cf")
    version("0.1.0-rc0", sha256="73754d38aaa0c2a1e012be6959787108fec142294774c23f70292f59c1bdc6c5")

    depends_on("c", type="build", when="+mpi")
    depends_on("cxx", type="build")

    _kokkos_backends = Kokkos.devices_variants
    for _backend in _kokkos_backends:
        _deflt, _descr = _kokkos_backends[_backend]
        variant(_backend.lower(), default=_deflt, description=_descr)

    variant("shared", default=True, description="Build shared libraries")
    variant("mpi", default=True, description="Build with mpi support")
    variant("all", default=False, description="Build with ALL support")
    variant("arborx", default=False, description="Build with ArborX support")
    variant("heffte", default=False, description="Build with heFFTe support")
    variant("hypre", default=False, description="Build with HYPRE support")
    variant("silo", default=False, description="Build with SILO support")
    variant("hdf5", default=False, description="Build with HDF5 support")
    variant("cajita", default=False, description="Build Cajita subpackage (Grid in 0.6:)")
    variant("grid", default=False, description="Build Grid subpackage")
    variant("testing", default=False, description="Build unit tests")
    variant("examples", default=False, description="Build tutorial examples")
    variant("performance_testing", default=False, description="Build performance tests")

    depends_on("cmake@3.9:", type="build", when="@:0.4.0")
    depends_on("cmake@3.16:", type="build", when="@0.5.0:")

    depends_on("googletest", type="build", when="+testing")
    _versions = {":0.2": "-legacy", "0.3:": "@3.1:", "0.4:": "@3.2:", "0.6:": "@3.7:"}
    for _version in _versions:
        _kk_version = _versions[_version]
        for _backend in _kokkos_backends:
            if _kk_version == "-legacy" and _backend == "pthread":
                _kk_spec = "kokkos-legacy+pthreads"
            elif _kk_version == "-legacy" and _backend not in ["serial", "openmp", "cuda"]:
                continue
            # Handled separately by Cuda/ROCmPackage below
            elif _backend == "cuda" or _backend == "hip":
                continue
            else:
                _kk_spec = "kokkos{0}+{1}".format(_kk_version, _backend)
            depends_on(_kk_spec, when="@{0}+{1}".format(_version, _backend))

    # Propagate cuda architectures down to Kokkos and optional submodules
    for arch in CudaPackage.cuda_arch_values:
        cuda_dep = "+cuda cuda_arch={0}".format(arch)
        depends_on("kokkos {0}".format(cuda_dep), when=cuda_dep)
        depends_on("heffte {0}".format(cuda_dep), when="+heffte {0}".format(cuda_dep))
        depends_on("arborx {0}".format(cuda_dep), when="+arborx {0}".format(cuda_dep))
        depends_on("hypre {0}".format(cuda_dep), when="+hypre {0}".format(cuda_dep))

    for arch in ROCmPackage.amdgpu_targets:
        rocm_dep = "+rocm amdgpu_target={0}".format(arch)
        depends_on("kokkos {0}".format(rocm_dep), when=rocm_dep)
        depends_on("heffte {0}".format(rocm_dep), when="+heffte {0}".format(rocm_dep))
        depends_on("arborx {0}".format(rocm_dep), when="+arborx {0}".format(rocm_dep))
        depends_on("hypre {0}".format(rocm_dep), when="+hypre {0}".format(rocm_dep))

    conflicts("+cuda", when="cuda_arch=none")
    conflicts("+rocm", when="amdgpu_target=none")

    # https://github.com/ECP-copa/Cabana/releases/tag/0.7.0
    depends_on("kokkos+cuda_lambda@3.7:", when="+cuda")
    depends_on("kokkos+cuda_lambda@4.1:", when="+cuda@0.7:")

    # Dependencies for subpackages
    depends_on("all", when="@0.5.0:+all")
    depends_on("arborx", when="@0.3.0:+arborx")
    depends_on("hypre-cmake@2.22.0:", when="@0.4.0:+hypre")
    depends_on("hypre-cmake@2.22.1:", when="@0.5.0:+hypre")
    depends_on("heffte@2.0.0", when="@0.4.0+heffte")
    depends_on("heffte@2.1.0", when="@0.5.0+heffte")
    depends_on("heffte@2.3.0:", when="@0.6.0:+heffte")
    depends_on("silo", when="@0.5.0:+silo")
    depends_on("hdf5", when="@0.6.0:+hdf5")
    depends_on("mpi", when="+mpi")

    # CMakeLists.txt of Cabana>=0.6 always enables HDF5 with CMake >= 3.26 (not changed post-0.6):
    conflicts("~hdf5", when="@0.6.0: ^cmake@3.26:")

    # Cabana HDF5 support requires MPI.
    conflicts("+hdf5 ~mpi")

    # Cajita support requires MPI
    conflicts("+cajita ~mpi")
    conflicts("+grid ~mpi")

    # The +grid does not support gcc>=13 (missing iostream/cstdint includes):
    conflicts("+grid", when="@:0.6 %gcc@13:")

    # Conflict variants only available in newer versions of cabana
    conflicts("+rocm", when="@:0.2.0")
    conflicts("+sycl", when="@:0.3.0")
    conflicts("+silo", when="@:0.3.0")
    conflicts("+hdf5", when="@:0.5.0")

    @when("+mpi")
    def patch(self):
        # CMakeLists.txt tries to enable C when MPI is requsted, but too late:
        filter_file("LANGUAGES CXX", "LANGUAGES C CXX", "CMakeLists.txt")

    def cmake_args(self):
        options = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]

        enable = ["CAJITA", "TESTING", "EXAMPLES", "PERFORMANCE_TESTING"]
        require = ["ALL", "ARBORX", "HEFFTE", "HYPRE", "SILO", "HDF5"]

        # These variables were removed in 0.3.0 (where backends are
        # automatically used from Kokkos)
        if self.spec.satisfies("@:0.2.0"):
            enable += ["Serial", "OpenMP", "Cuda"]
        # MPI was changed from ENABLE to REQUIRE in 0.4.0
        if self.spec.satisfies("@:0.3.0"):
            enable += ["MPI"]
        else:
            require += ["MPI"]

        # Cajita was renamed Grid in 0.6
        if self.spec.satisfies("@0.6.0:"):
            enable += ["GRID"]

        for category, cname in zip([enable, require], ["ENABLE", "REQUIRE"]):
            for var in category:
                cbn_option = "Cabana_{0}_{1}".format(cname, var)
                options.append(self.define_from_variant(cbn_option, var.lower()))

        # Attempt to disable find_package() calls for disabled options(if option supports it):
        for var in require:
            if not self.spec.satisfies("+" + var.lower()):
                options.append(self.define("CMAKE_DISABLE_FIND_PACKAGE_" + var, "ON"))

        # Use hipcc for HIP.
        if self.spec.satisfies("+rocm"):
            options.append(self.define("CMAKE_CXX_COMPILER", self.spec["hip"].hipcc))

        return options
