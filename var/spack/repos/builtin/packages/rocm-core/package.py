# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RocmCore(CMakePackage):
    """rocm-core is a utility which can be used to get ROCm release version.
    It also provides the Lmod modules files for the ROCm release.
    getROCmVersion function provides the ROCm version."""

    homepage = "https://github.com/ROCm/rocm-core"
    url = "https://github.com/ROCm/rocm-core/archive/refs/tags/rocm-6.0.0.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["librocm-core"]

    license("MIT")
    version("6.2.1", sha256="35cb5f6dfb1847469930bf0fa0913499b6c3f59b2b573a9f598b0956104ba5e2")
    version("6.2.0", sha256="9bafaf801721e98b398624c8d2fa78618d297d6800f96113e26c275889205526")
    version("6.1.2", sha256="ce9cbe12977f2058564ecb4cdcef4fd0d7880f6eff8591630f542441092f4fa3")
    version("6.1.1", sha256="a27bebdd1ba9d387f33b82a67f64c55cb565b482fe5017d5b5726d68da1ab839")
    version("6.1.0", sha256="9dfe542d1647c42993b06f594c316dad63ba6d6fb2a7398bd72c5768fd1d7b5b")
    version("6.0.2", sha256="04f01dca2862f0bf781de8afb74aabefc3c9b1d9f01bc8cadb2eb3d7395119cc")
    version("6.0.0", sha256="d950ee4b63336f34579b6e1dda2d05966b7afa9c84bcdc13874991d1147dc788")
    version("5.7.1", sha256="fc4915019ddfd126e8ef6a15006bce3aa7bd5fd11dc8eb04ce2ee6bdf9c6ae7f")
    version("5.7.0", sha256="722689bfec46c35f5428a41c5aacfc31efec2294fc3b0112861c562f8a71ac93")
    version("5.6.1", sha256="eeef75e16e05380ccbc8df17a02dc141a66dddaadb444a97f7278f78067c498c")
    version("5.6.0", sha256="3c3d47c8b774968d768d42810a3fed42d058b7d6da248d5295df2a7ffb262568")
    version("5.5.1", sha256="bc73060432ffdc2e210394835d383890b9652476074ef4708d447473f273ce76")
    version("5.5.0", sha256="684d3312bb14f05dc280cf136f5eddff38ba340cd85c383d6a217d8e27d3d57d")

    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    conflicts("+asan", when="os=rhel9")
    conflicts("+asan", when="os=centos7")
    conflicts("+asan", when="os=centos8")

    depends_on("cxx", type="build")  # generated

    for ver in ["6.1.0", "6.1.1", "6.1.2", "6.2.0", "6.2.1"]:
        depends_on("llvm-amdgpu", when=f"@{ver}+asan")

    def setup_build_environment(self, env):
        if self.spec.satisfies("+asan"):
            env.set("CC", self.spec["llvm-amdgpu"].prefix + "/bin/clang")
            env.set("CXX", self.spec["llvm-amdgpu"].prefix + "/bin/clang++")
            env.set("ASAN_OPTIONS", "detect_leaks=0")
            env.set("CFLAGS", "-fsanitize=address -shared-libasan")
            env.set("CXXFLAGS", "-fsanitize=address -shared-libasan")
            env.set("LDFLAGS", "-fuse-ld=lld")

    def cmake_args(self):
        args = [self.define("ROCM_VERSION", self.spec.version)]
        return args
