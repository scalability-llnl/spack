# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *
from spack.package_test import compare_output_file, compile_c_and_execute


class Pocl(CMakePackage):
    """Portable Computing Language (pocl) is an open source implementation
    of the OpenCL standard which can be easily adapted for new targets
    and devices, both for homogeneous CPU and heterogeneous
    GPUs/accelerators."""

    homepage = "https://portablecl.org"
    url = "https://github.com/pocl/pocl/archive/v1.1.tar.gz"
    git = "https://github.com/pocl/pocl.git"

    license("MIT")

    version("main", branch="main")
    version("3.0", sha256="a3fd3889ef7854b90b8e4c7899c5de48b7494bf770e39fba5ad268a5cbcc719d")
    version("1.8", sha256="0f63377ae1826e16e90038fc8e7f65029be4ff6f9b059f6907174b5c0d1f8ab2")
    version("1.7", sha256="5f6bbc391ba144bc7becc3b90888b25468460d5aa6830f63a3b066137e7bfac3")
    version("1.6", sha256="b0a4c0c056371b6f0db726b88fbb76bbee94948fb2abd4dbc8d958f7c42f766c")
    version("1.5", sha256="4fcf4618171727d165fc044d465a66e3119217bb4577a97374f94fcd8aed330e")
    version("1.4", sha256="ec237faa83bb1c803fbdf7c6e83d8a2ad68b6f0ed1879c3aa16c0e1dcc478742")
    version("1.3", sha256="6527e3f47fab7c21e96bc757c4ae3303901f35e23f64642d6da5cc4c4fcc915a")
    version("1.2", sha256="0c43e68f336892f3a64cba19beb99d9212f529bedb77f7879c0331450b982d46")
    version("1.1", sha256="1e8dd0693a88c84937754df947b202871a40545b1b0a97ebefa370b0281c3c53")
    version("1.0", sha256="94bd86a2f9847c03e6c3bf8dca12af3734f8b272ffeacbc3fa8fcca58844b1d4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    conflicts("@:1.5", when="target=a64fx", msg="a64fx is supported by pocl v1.6 and above.")

    # < 3.0 provided full OpenCL 1.2 support and some intermediate level of
    # OpenCL 2.0 support.  >= 3.0 provides full OpenCL 3.0 support when using
    # llvm >= 14.
    provides("opencl@2.0", when="^llvm@:13")
    provides("opencl@3.0", when="@3: ^llvm@14:")

    depends_on("cmake @2.8.12:", type="build")
    depends_on("hwloc")
    depends_on("hwloc@:1", when="@:1.1")
    depends_on("libtool", type="link", when="@:1.3")  # links against libltdl
    depends_on("pkgconfig", type="build")

    depends_on("llvm +clang")
    depends_on("llvm @14:15", when="@master")
    depends_on("llvm @13:14", when="@3.0")
    depends_on("llvm @12:13", when="@1.8")
    depends_on("llvm @11:12", when="@1.7")
    depends_on("llvm @10:11", when="@1.6")
    depends_on("llvm @9:10", when="@1.5")
    depends_on("llvm @8:9", when="@1.4")
    depends_on("llvm @7:8", when="@1.3")
    depends_on("llvm @6:7", when="@1.2")
    depends_on("llvm @5:6", when="@1.1")
    depends_on("llvm @4:5", when="@1.0")

    variant(
        "distro",
        default=False,
        description=(
            "Support several CPU architectures, "
            "suitable e.g. in a build "
            "that will be made available for download"
        ),
    )
    variant("icd", default=False, description="Support a system-wide ICD loader")

    depends_on("ocl-icd", when="+icd")

    def url_for_version(self, version):
        if version >= Version("1.0"):
            url = "https://github.com/pocl/pocl/archive/v{0}.tar.gz"
        else:
            url = "https://portablecl.org/downloads/pocl-{0}.tar.gz"

        return url.format(version.up_to(2))

    def cmake_args(self):
        args = [
            self.define("INSTALL_OPENCL_HEADERS", True),
            self.define("ENABLE_LLVM", True),
            self.define("STATIC_LLVM", True),
            self.define_from_variant("ENABLE_ICD", "icd"),
        ]
        if "+distro" in self.spec:
            args.append(self.define("KERNELLIB_HOST_CPU_VARIANTS", "distro"))
        return args

    @run_after("install")
    def symlink_opencl(self):
        os.symlink("CL", self.prefix.include.OpenCL)

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        # Build and run a small program to test the installed OpenCL library
        spec = self.spec
        print("Checking pocl installation...")
        checkdir = "spack-check"
        with working_dir(checkdir, create=True):
            source = join_path(os.path.dirname(self.module.__file__), "example1.c")
            cflags = spec["pocl"].headers.cpp_flags.split()
            # ldflags = spec["pocl"].libs.ld_flags.split()
            ldflags = ["-L%s" % spec["pocl"].prefix.lib, "-lOpenCL", "-lpoclu"]
            output = compile_c_and_execute(source, cflags, ldflags)
            compare_output_file(
                output, join_path(os.path.dirname(self.module.__file__), "example1.out")
            )
