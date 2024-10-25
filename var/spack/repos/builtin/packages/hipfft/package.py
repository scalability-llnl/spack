# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Hipfft(CMakePackage, CudaPackage, ROCmPackage):
    """hipFFT is an FFT marshalling library. Currently, hipFFT supports
    either rocFFT or cuFFT as backends.hipFFT exports an interface that
    does not require the client to change, regardless of the chosen backend.
    It sits between the application and the backend FFT library, marshalling
    inputs into the backend and results back to the application."""

    homepage = "https://github.com/ROCm/hipFFT"
    git = "https://github.com/ROCm/hipFFT.git"
    url = "https://github.com/ROCm/hipfft/archive/rocm-6.1.0.tar.gz"
    tags = ["rocm"]

    maintainers("renjithravindrankannath", "srekolam")

    license("MIT")

    version("master", branch="master")
    version("6.2.1", sha256="5f668fa8b5ed10d47d164d887699d3c14d900d78f6a31bf953f8fbbc08bc5fd1")
    version("6.2.0", sha256="8d19aebb1bbfea1f235ca08d34393ce39bea35dc9cbfa72a3cf7cdf1c56410e7")
    version("6.1.2", sha256="6753e45d9c671d58e68bed2b0c1bfcd40fad9d690dba3fe6011e67e51dbe3cc6")
    version("6.1.1", sha256="df84e488098d457a7411f6b459537fa5c5ee160027efc3a9a076980bbe57c4d3")
    version("6.1.0", sha256="1a9cf598a932192f7f12b8987d96477f09186f9a95c5a28742f9caeb81640c95")
    version("6.0.2", sha256="c0a4bac5fa9a757a19a4995fa9571328b6ee0a71e93c66a880069794d65d284a")
    version("6.0.0", sha256="44f328b7862c066459089dfe62833cb7d626c6ceb71c57d8c7d6bba45dad491e")
    version("5.7.1", sha256="33452576649df479f084076c47d0b30f6f1da34864094bce767dd9bf609f04aa")
    version("5.7.0", sha256="daa5dc44580145e85ff8ffa7eb40a3d1ef41f3217549c01281715ff696a31588")
    version("5.6.1", sha256="d2ae36b8eacd39b865e8a7972b8eb86bcea2de4ac90711bba7e29b39b01eaa74")
    version("5.6.0", sha256="c7f425b693caf9371b42226d86392335d993a117d23219b6ba1fd13523cb8261")
    version("5.5.1", sha256="3addd15a459752ad657e84c2a7b6b6289600d1d0a5f90d6e0946ba11e8148fc0")
    version("5.5.0", sha256="47ec6f7da7346c312b80daaa8f763e86c7bdc33ac8617cfa3344068e5b20dd9e")
    with default_args(deprecated=True):
        version("5.4.3", sha256="ae37f40b6019a11f10646ef193716836f366d269eab3c5cc2ed09af85355b945")
        version("5.4.0", sha256="d0a8e790182928b3d19774b8db1eece9b881a422f6a7055c051b12739fded624")
        version("5.3.3", sha256="fd1662cd5b1e1bce9db53b320c0fe614179cd196251efc2ef3365d38922b5cdc")
        version("5.3.0", sha256="ebbe2009b86b688809b6b4d5c3929fc589db455218d54a37790f21339147c5df")

    depends_on("cxx", type="build")  # generated

    # default to an 'auto' variant until amdgpu_targets can be given a better default than 'none'
    amdgpu_targets = ROCmPackage.amdgpu_targets
    variant(
        "amdgpu_target",
        description="AMD GPU architecture",
        values=spack.variant.DisjointSetsOfValues(("auto",), ("none",), amdgpu_targets)
        .with_default("auto")
        .with_error(
            "the values 'auto' and 'none' are mutually exclusive with any of the other values"
        )
        .with_non_feature_values("auto", "none"),
        sticky=True,
    )
    variant("rocm", default=True, description="Enable ROCm support")
    conflicts("+cuda +rocm", msg="CUDA and ROCm support are mutually exclusive")
    conflicts("~cuda ~rocm", msg="CUDA or ROCm support is required")
    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    depends_on("cmake@3.5:", type="build")

    depends_on("hip +cuda", when="+cuda")

    for ver in [
        "5.3.0",
        "5.3.3",
        "5.4.0",
        "5.4.3",
        "5.5.0",
        "5.5.1",
        "5.6.0",
        "5.6.1",
        "5.7.0",
        "5.7.1",
        "6.0.0",
        "6.0.2",
        "6.1.0",
        "6.1.1",
        "6.1.2",
        "6.2.0",
        "6.2.1",
        "master",
    ]:
        depends_on(f"rocm-cmake@{ver}:", type="build", when=f"@{ver}")
        depends_on(f"rocfft@{ver}", when=f"+rocm @{ver}")

    for tgt in ROCmPackage.amdgpu_targets:
        depends_on(f"rocfft amdgpu_target={tgt}", when=f"+rocm amdgpu_target={tgt}")
    # https://github.com/ROCm/rocFFT/pull/85)
    patch("001-remove-submodule-and-sync-shared-files-from-rocFFT.patch", when="@6.0.0")

    def setup_build_environment(self, env):
        if self.spec.satisfies("+asan"):
            self.asan_on(env)

    def cmake_args(self):
        args = [self.define("BUILD_CLIENTS_SAMPLES", "OFF")]

        if self.spec.satisfies("+rocm"):
            args.append(self.define("BUILD_WITH_LIB", "ROCM"))
        elif self.spec.satisfies("+cuda"):
            args.append(self.define("BUILD_WITH_LIB", "CUDA"))

        # FindHIP.cmake is still used for both +rocm and +cuda
        if self.spec["hip"].satisfies("@5.2:"):
            args.append(self.define("CMAKE_MODULE_PATH", self.spec["hip"].prefix.lib.cmake.hip))

        if self.spec.satisfies("@5.2.0:"):
            args.append(self.define("BUILD_FILE_REORG_BACKWARD_COMPATIBILITY", True))

        if self.spec.satisfies("@5.3.0:"):
            args.append(self.define("CMAKE_INSTALL_LIBDIR", "lib"))
        return args
