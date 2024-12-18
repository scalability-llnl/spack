# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RocmClangOcl(CMakePackage):
    """OpenCL compilation with clang compiler"""

    homepage = "https://github.com/ROCm/clang-ocl"
    git = "https://github.com/ROCm/clang-ocl.git"
    url = "https://github.com/ROCm/clang-ocl/archive/rocm-6.1.2.tar.gz"
    tags = ["rocm"]

    test_requires_compiler = True

    license("MIT")

    maintainers("srekolam", "renjithravindrankannath")
    version("master", branch="master")
    version("6.1.2", sha256="cc9942539b5e50b97fa0d2425ba93aae7223635fecba869d8f43b2c26f9482ae")
    version("6.1.1", sha256="21b8a6d521a8e584e18851d27b5ef328a63ea7ee9eb3cc52508b9bfcf975e119")
    version("6.1.0", sha256="c983adad49ab5850307db1282f8bc957b9870d4ce37db8fbb43c52db6c90d0ed")
    version("6.0.2", sha256="a2f2fcb203737b1f436b4c2b78bbd696552f6de619ba0e7e8faf95a888869866")
    version("6.0.0", sha256="74b5a64c32f3c57e7e4de638fffabbf448ecdb3dd8e65678b7ba0633352b4ca3")
    version("5.7.1", sha256="32e4430d009cbbf5404ca9cbbb549b36897fa1826bc2285372e293cfe7531bf8")
    version("5.7.0", sha256="c9ca80bfee674e740039256a846107373f1cf6554dc28398599976d8646a0392")
    version("5.6.1", sha256="c41deb1b564d939fc897b2bbdb13570b2234fa4c052a39783f5ad2dd1052f901")
    version("5.6.0", sha256="1afc47dee02d73c10de422f254067f4ef3ff921c4a1204d54ecc40e61fc63497")
    version("5.5.1", sha256="bfa62ad14830e2bd5afbc346685216c69f8cbef0eb449954f793178e10b19a38")
    version("5.5.0", sha256="43a5459165693301ba2ebcc41b2b0705df9a3a47571d43bdc2cc49cfdd0833a7")
    with default_args(deprecated=True):
        version("5.4.3", sha256="689e0354ea685bd488116de8eb902b902492e9ace184c3109b97b9a43f8b2d59")
        version("5.4.0", sha256="602f8fb1f36587543cc0ee95fd1938f8eeb03de79119101e128150332cc8d89c")
        version("5.3.3", sha256="549d5bf37507f67c5277abdeed4ec40b5d0edbfbb72907c685444c26b9ce6f8a")
        version("5.3.0", sha256="66b80ba050848ad921496bd894e740e66afad0ba1923b385f01f2eeae97999ad")

    depends_on("cmake@3.5:", type="build")

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
        "master",
    ]:
        depends_on(f"rocm-cmake@{ver}:", type="build", when=f"@{ver}")
        depends_on(f"llvm-amdgpu@{ver}", when=f"@{ver}")
        # support both builtin and standalone device libs
        depends_on(f"rocm-device-libs@{ver}", when=f"@{ver} ^llvm-amdgpu ~rocm-device-libs")

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
    ]:
        depends_on(f"rocm-core@{ver}", when=f"@{ver}")

    test_src_dir = "test"

    @run_after("install")
    def cache_test_sources(self):
        """Copy the tests source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(self, [self.test_src_dir])

    def test_make(self):
        """Test make"""
        test_dir = join_path(self.test_suite.current_test_cache_dir, self.test_src_dir)
        with working_dir(test_dir):
            cmake = self.spec["cmake"].command
            cmake("-DCMAKE_PREFIX_PATH=" + self.spec["rocm-clang-ocl"].prefix, ".")
            make = which("make")
            make()
