# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class RocmDeviceLibs(CMakePackage):
    """set of AMD specific device-side language runtime libraries"""

    homepage = "https://github.com/ROCm/ROCm-Device-Libs"
    git = "https://github.com/ROCm/ROCm-Device-Libs.git"

    def url_for_version(self, version):
        if version <= Version("6.0.2"):
            url = "https://github.com/ROCm/ROCm-Device-Libs/archive/rocm-{0}.tar.gz"
        else:
            url = "https://github.com/ROCm/llvm-project/archive/rocm-{0}.tar.gz"
        return url.format(version)

    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath", "haampie")

    version("master", branch="amd-stg-open")
    version("6.2.1", sha256="4840f109d8f267c28597e936c869c358de56b8ad6c3ed4881387cf531846e5a7")
    version("6.2.0", sha256="12ce17dc920ec6dac0c5484159b3eec00276e4a5b301ab1250488db3b2852200")
    version("6.1.2", sha256="300e9d6a137dcd91b18d5809a316fddb615e0e7f982dc7ef1bb56876dff6e097")
    version("6.1.1", sha256="f1a67efb49f76a9b262e9735d3f75ad21e3bd6a05338c9b15c01e6c625c4460d")
    version("6.1.0", sha256="6bd9912441de6caf6b26d1323e1c899ecd14ff2431874a2f5883d3bc5212db34")
    version("6.0.2", sha256="c6d88b9b46e39d5d21bd5a0c1eba887ec473a370b1ed0cebd1d2e910eedc5837")
    version("6.0.0", sha256="198df4550d4560537ba60ac7af9bde31d59779c8ec5d6309627f77a43ab6ef6f")
    version("5.7.1", sha256="703de8403c0bd0d80f37c970a698f10f148daf144d34f982e4484d04f7c7bbef")
    version("5.7.0", sha256="0f8780b9098573f1c456bdc84358de924dcf00604330770a383983e1775bf61e")
    version("5.6.1", sha256="f0dfab272ff936225bfa1e9dabeb3c5d12ce08b812bf53ffbddd2ddfac49761c")
    version("5.6.0", sha256="efb5dcdca9b3a9fbe408d494fb4a23e0b78417eb5fa8eebd4a5d226088f28921")
    version("5.5.1", sha256="3b5f6dd85f0e3371f6078da7b59bf77d5b210e30f1cc66ef1e2de6bbcb775833")
    version("5.5.0", sha256="5ab95aeb9c8bed0514f96f7847e21e165ed901ed826cdc9382c14d199cbadbd3")
    with default_args(deprecated=True):
        version("5.4.3", sha256="f4f7281f2cea6d268fcc3662b37410957d4f0bc23e0df9f60b12eb0fcdf9e26e")
        version("5.4.0", sha256="d68813ded47179c39914c8d1b76af3dad8c714b10229d1e2246af67609473951")
        version("5.3.3", sha256="963c9a0561111788b55a8c3b492e2a5737047914752376226c97a28122a4d768")
        version("5.3.0", sha256="f7e1665a1650d3d0481bec68252e8a5e68adc2c867c63c570f6190a1d2fe735c")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    depends_on("cmake@3.13.4:", type="build")

    depends_on("zlib-api", type="link")
    depends_on("texinfo", type="link")

    depends_on("rocm-cmake@3.5.0:", type="build")

    # Make sure llvm is not built with rocm-device-libs (that is, it's already
    # built with rocm-device-libs as an external project).
    depends_on("llvm-amdgpu ~rocm-device-libs")

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
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")

    for ver in [
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
    ]:
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")

    @property
    def root_cmakelists_dir(self):
        if self.spec.satisfies("@:6.0"):
            return "."
        else:
            return join_path("amd", "device-libs")

    def cmake_args(self):
        spec = self.spec
        return [
            self.define("LLVM_DIR", spec["llvm-amdgpu"].prefix),
            self.define("CMAKE_C_COMPILER", spec["llvm-amdgpu"].prefix.bin.clang),
        ]
