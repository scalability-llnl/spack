# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RocprofilerCompute(CMakePackage):
    """Advanced Profiling and Analytics for AMD Hardware"""

    homepage = "https://github.com/ROCm/rocprofiler-compute"
    git = "https://github.com/ROCm/rocprofiler-compute.git"
    url = "https://github.com/ROCm/rocprofiler-compute/archive/refs/tags/rocm-6.3.2.tar.gz"

    tags = ["rocm"]

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    license("MIT")
    version("6.3.2", sha256="317f19acfa6e6780923e6c8144c3c223b523c382588df528b6df001fae38d13d")

    depends_on("python@3.8:")
    depends_on("py-pip", type="run")
    depends_on("py-astunparse@1.6.2", type=("build", "run"))  # wants exact version
    depends_on("py-colorlover", type=("build", "run"))
    depends_on("py-pyyaml")
    depends_on("py-matplotlib")
    depends_on("py-pandas@1.4.3:")
    depends_on("py-numpy@1.17.5:")
    depends_on("py-pymongo")
    depends_on("py-tabulate")
    depends_on("py-tqdm")
    depends_on("py-kaleido")
    depends_on("py-plotille")
    depends_on("py-dash-svg", type=("build", "run"))
    depends_on("py-dash", type=("build", "run"))
    depends_on("py-dash-bootstrap-components", type=("build", "run"))

    def cmake_args(self):
        args = [self.define("ENABLE_TESTS", self.run_tests)]
        return args

    @run_before("cmake")
    def before_cmake(self):
        touch(join_path(self.stage.source_path, "VERSION.sha"))
