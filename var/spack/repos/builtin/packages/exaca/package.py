# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.kokkos import Kokkos


class Exaca(CMakePackage, CudaPackage, ROCmPackage):
    """ExaCA: an exascale cellular automata application for alloy solidification modeling"""

    homepage = "https://github.com/LLNL/ExaCA"
    git = "https://github.com/LLNL/ExaCA.git"
    url = "https://github.com/LLNL/ExaCA/archive/2.0.0.tar.gz"

    maintainers("streeve", "MattRolchigo")

    tags = ["ecp"]

    license("MIT")

    version("master", branch="master")
    version("2.0.0", sha256="a33cc65a6e79bed37a644f5bfc9dd5fe356239f78c5b82830c6354acc43e016b")
    version("1.3.0", sha256="637215d3c64e8007b55d68bea6003b51671029d9045af847534e0e59c4271a94")
    version("1.2.0", sha256="5038d63de96c6142ddea956998e1f4ebffbc4a5723caa4da0e73eb185e6623e4")
    version("1.1.0", sha256="10106fb1836964a19bc5bab3f374baa24188ba786c768e554442ab896b31ff24")
    version("1.0.0", sha256="48556233360a5e15e1fc20849e57dd60739c1991c7dfc7e6b2956af06688b96a")

    depends_on("cxx", type="build")  # generated

    _kokkos_backends = Kokkos.devices_variants
    for _backend in _kokkos_backends:
        _deflt, _descr = _kokkos_backends[_backend]
        variant(_backend.lower(), default=_deflt, description=_descr)

    variant("shared", default=True, description="Build shared libraries")
    variant("testing", default=False, description="Build unit tests")

    depends_on("cmake@3.9:", type="build", when="@:1.1")
    depends_on("cmake@3.12:", type="build", when="@master")
    depends_on("googletest@1.10:", type="test", when="@1.1:+testing")
    depends_on("kokkos@3.0:", when="@:1.1")
    depends_on("kokkos@3.2:", when="@1.2:")
    depends_on("kokkos@4.0:", when="@1.3:")
    depends_on("mpi")
    depends_on("nlohmann-json", when="@1.2:")

    for _backend in _kokkos_backends:
        # Handled separately below
        if _backend != "cuda" and _backend != "rocm":
            _backend_dep = "+{0}".format(_backend)
            depends_on("kokkos {0}".format(_backend_dep), when=_backend_dep)

    for arch in CudaPackage.cuda_arch_values:
        cuda_dep = "+cuda cuda_arch={0}".format(arch)
        depends_on("kokkos {0}".format(cuda_dep), when=cuda_dep)
    for arch in ROCmPackage.amdgpu_targets:
        rocm_dep = "+rocm amdgpu_target={0}".format(arch)
        depends_on("kokkos {0}".format(rocm_dep), when=rocm_dep)

    def cmake_args(self):
        options = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]

        if self.spec.satisfies("@1.1:"):
            options += [self.define_from_variant("ExaCA_ENABLE_TESTING", "testing")]
        # Only release with optional json
        if self.spec.satisfies("@1.2"):
            options += [self.define("ExaCA_ENABLE_JSON", "ON")]
        # Use the json dependency, not an internal download
        if self.spec.satisfies("@2.0:"):
            options += [self.define("ExaCA_REQUIRE_EXTERNAL_JSON", "ON")]

        # Use hipcc if compiling for rocm. Modifying this instead of CMAKE_CXX_COMPILER
        # keeps the spack wrapper
        if self.spec.satisfies("+rocm"):
            env["SPACK_CXX"] = self.spec["hip"].hipcc

        return options
