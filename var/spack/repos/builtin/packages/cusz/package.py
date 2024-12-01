# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cusz(CMakePackage, CudaPackage):
    """A GPU accelerated error-bounded lossy compression for scientific data"""

    homepage = "https://szcompressor.org/"
    git = "https://github.com/szcompressor/cusz"
    url = "https://github.com/szcompressor/cuSZ/archive/refs/tags/v0.3.tar.gz"

    maintainers("jtian0", "dingwentao")
    tags = ["e4s"]

    conflicts("~cuda")
    conflicts("cuda_arch=none", when="+cuda")

    version("develop", branch="develop")
    version("0.6.0", commit="cafed521dc338fe2159ebb5b09a36fc318524bf7")
    version("0.3.1", commit="02be3cbd07db467decaf45ec9eb593ba6173c809")
    version("0.3", sha256="0feb4f7fd64879fe147624dd5ad164adf3983f79b2e0383d35724f8d185dcb11")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # these version of Cuda provide the CUB headers, but not CUB cmake configuration that we use.
    conflicts("^cuda@11.0.2:11.2.2")

    depends_on("cub", when="^cuda@:10.2.89")

    def cmake_args(self):
        cuda_arch = self.spec.variants["cuda_arch"].value
        args = ["-DBUILD_TESTING=OFF", ("-DCMAKE_CUDA_ARCHITECTURES=%s" % cuda_arch)]
        return args
