# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RocprofilerRegister(CMakePackage):
    """The rocprofiler-register library is a helper library that coordinates
    the modification of the intercept API table(s) of the HSA/HIP/ROCTx runtime
    libraries by the ROCprofiler (v2) library"""

    homepage = "https://github.com/ROCm/rocprofiler-register"
    git = "https://github.com/ROCm/rocprofiler-register.git"
    url = "https://github.com/ROCm/rocprofiler-register/archive/refs/tags/rocm-6.2.0.tar.gz"

    tags = ["rocm"]

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    license("MIT")
    version("6.2.1", sha256="161d3502863147df4daeadc538d0eb156c314c94634f8c34ee5994f046f8753f")
    version("6.2.0", sha256="5cdfdfc621da9ef5a6b828d1a3a342db222b648c91359f71651b9404bf7ba62c")
    version("6.1.2", sha256="aa57b234cc1db5ae32c7494f4a9120b95a1845b95469dad447f470a6aa5e3cc9")
    version("6.1.1", sha256="38242443d9147a04d61374de4cecee686578a3140fed17e88480f564a1f67cc7")
    version("6.1.0", sha256="c6e60447ea2ccca8d6acd8758ac00037347892b16b450e1f99ddd04cc4b6cac1")

    depends_on("cxx", type="build")
    depends_on("fmt")
    depends_on("glog")

    patch("001-add-cpack-fmt-glog.patch")

    def cmake_args(self):
        args = ["-DROCPROFILER_REGISTER_BUILD_FMT=OFF", "-DROCPROFILER_REGISTER_BUILD_GLOG=OFF"]
        args.append(self.define("ROCPROFILER_REGISTER_BUILD_TESTS", self.run_tests))
        return args
