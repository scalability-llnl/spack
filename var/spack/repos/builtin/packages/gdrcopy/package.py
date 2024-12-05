# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gdrcopy(MakefilePackage, CudaPackage):
    """A fast GPU memory copy library based on NVIDIA GPUDirect
    RDMA technology."""

    homepage = "https://github.com/NVIDIA/gdrcopy"
    url = "https://github.com/NVIDIA/gdrcopy/archive/v2.1.tar.gz"
    git = "https://github.com/NVIDIA/gdrcopy"
    maintainers("scothalverson")

    license("MIT")

    version("master", branch="master")
    version("2.4.1", sha256="faa7e816e9bad3301e53d6721457f7ef5ab42b7aa3b01ffda51f8e5620bb20ed")
    version("2.3", sha256="b85d15901889aa42de6c4a9233792af40dd94543e82abe0439e544c87fd79475")
    version("2.2", sha256="e4be119809391b18c735346d24b3b398dd9421cbff47ef12befbae40d61da45f")
    version("2.1", sha256="cecc7dcc071107f77396f5553c9109790b6d2298ae29eb2dbbdd52b2a213e4ea")
    version("2.0", sha256="98320e6e980a7134ebc4eedd6cf23647104f2b3c557f2eaf0d31a02609f5f2b0")
    version("1.3", sha256="f11cdfe389b685f6636b80b4a3312dc014a385ad7220179c1318c60e2e28af3a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Don't call ldconfig: https://github.com/NVIDIA/gdrcopy/pull/229
    patch("ldconfig.patch", when="@2.0:2.3")
    # Allow tests to build against libcuda.so stub
    patch(
        "https://github.com/NVIDIA/gdrcopy/commit/508dd6179dcb04ba7720e2da5124b77bbdb615b0.patch?full_index=1",
        sha256="cc18b13b6ea5512959464a85a43cdfda0bee5522a471e98ca76ba379bf582b5a",
        when="@2.0:2.3",
    )

    depends_on("pkgconfig", type="build", when="@2.0:2.3")
    depends_on("check")
    requires("+cuda")

    def setup_build_environment(self, env):
        env.set("CUDA", self.spec["cuda"].prefix)

    def build(self, spec, prefix):
        make("lib")
        make("exes")

    def install(self, spec, prefix):
        mkdir(prefix.include)
        mkdir(prefix.lib64)
        if spec.satisfies("@2.2:"):
            make("lib_install", "prefix={0}".format(self.prefix))
            make("exes_install", "prefix={0}".format(self.prefix))
        else:
            make("lib_install", "PREFIX={0}".format(self.prefix))
            make("exes_install", "PREFIX={0}".format(self.prefix))
