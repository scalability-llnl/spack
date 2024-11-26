# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import re
import shutil

from spack.package import *


class RocmSmiLib(CMakePackage):
    """It is a C library for Linux that provides a user space interface
    for applications to monitor and control GPU applications."""

    homepage = "https://github.com/ROCm/rocm_smi_lib"
    git = "https://github.com/ROCm/rocm_smi_lib.git"
    url = "https://github.com/ROCm/rocm_smi_lib/archive/rocm-6.1.2.tar.gz"
    tags = ["rocm"]

    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["librocm_smi64"]

    version("master", branch="master")
    version("6.2.1", sha256="28543d099fa44b4b79644533644aba4b67fa48d477628dd5802c3b50cc78583a")
    version("6.2.0", sha256="95010dfc9de9c608b9ce159107585ff4adce82a52a38daab2a37870aca2428bf")
    version("6.1.2", sha256="01f46fb1cb8c7a16a4c4db61871ee710ed37c0f8bd3a2dbe3415d3de2dffb4ef")
    version("6.1.1", sha256="7fd2234b05eb6b9397c5508bb37e81fb16ce2cadc2c97298b2124b46c3687880")
    version("6.1.0", sha256="d1a1b372489b27cb7eb8c91d74a71370ad9668dd5aaf89c0267172534e417e41")
    version("6.0.2", sha256="61e755d710ff38425df3d262d1ad4c510d52d3c64e3fe15140c2575eba316949")
    version("6.0.0", sha256="0053b42402fd007e5ca9b3186c70f2c6f1b3026558f328722adadc2838c51309")
    version("5.7.1", sha256="4d79cb0482b2f801cc7824172743e3dd2b44b9f6784d1ca2e5067f2fbb4ef803")
    version("5.7.0", sha256="a399db3d9fc113ce2dd1ab5608a1cf9129ec4b6a2a79ab7922b1d9f43c454640")
    version("5.6.1", sha256="9e94f9a941202c3d7ce917fd1cd78c4e0f06f48d6c929f3aa916378ccef1e02c")
    version("5.6.0", sha256="88be875948a29454b8aacced8bb8ad967502a7a074ecbc579ed673c1650a2f7e")
    version("5.5.1", sha256="37f32350bfaf6c697312628696d1b1d5fd9165f183882759bc6cb9a5d65b9430")
    version("5.5.0", sha256="0703f49b1c2924cc1d3f613258eabdff1925cb5bcf7cf22bb6b955dd065e4ce8")
    with default_args(deprecated=True):
        version("5.4.3", sha256="34d550272e420684230ceb7845aefcef79b155e51cf9ec55e31fdba2a4ed177b")
        version("5.4.0", sha256="4b110c9ec104ec39fc458b1b6f693662ab75395b75ed402b671d8e58c7ae63fe")
        version("5.3.3", sha256="c2c2a377c2e84f0c40297a97b6060dddc49183c2771b833ebe91ed98a98e4119")
        version("5.3.0", sha256="8f72ad825a021d5199fb73726b4975f20682beb966e0ec31b53132bcd56c5408")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build shared or static library")
    variant("asan", default=False, description="Build with address-sanitizer enabled or disabled")

    depends_on("cmake@3:", type="build")
    depends_on("python@3:", type=("build", "run"))

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

    patch(
        "https://github.com/ROCm/rocm_smi_lib/commit/11f12b86517d0e9868f4d16d74d4e8504c3ba7da.patch?full_index=1",
        sha256="62be7262f6e1e71bf82a03f500a424a536638f04e913d0f4b477f60e8e1190fd",
        when="@6.1.1:",
    )

    patch("disable_pdf_generation_with_doxygen_and_latex.patch", when="@:5.6")

    def cmake_args(self):
        args = [
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define("CMAKE_INSTALL_LIBDIR", "lib"),
            self.define("BUILD_TESTS", self.run_tests),
        ]
        if self.spec.satisfies("@5.7.0:"):
            args.append(self.define_from_variant("ADDRESS_SANITIZER", "asan"))
        return args

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            return "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        return None

    @run_after("install")
    def post_install(self):
        if self.spec.satisfies("@:5.1"):
            shutil.rmtree(self.prefix.lib)
            install_tree(self.prefix.rocm_smi, self.prefix)
            shutil.rmtree(self.prefix.rocm_smi)
            os.remove(join_path(self.prefix.bin, "rsmiBindings.py"))
            symlink("../bindings/rsmiBindings.py", join_path(self.prefix.bin, "rsmiBindings.py"))

    @run_after("build")
    @on_package_attributes(run_tests=True)
    def check_build(self):
        exe = which(join_path(self.build_directory, "tests", "rocm_smi_test", "rsmitst"))
        exe()
