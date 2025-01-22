# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Omniperf(CMakePackage):
    """Advanced Profiling and Analytics for AMD Hardware"""

    homepage = "https://github.com/ROCm/omniperf"
    git = "https://github.com/ROCm/omniperf.git"
    url = "https://github.com/ROCm/omniperf/archive/refs/tags/rocm-6.2.1.tar.gz"

    tags = ["rocm"]

    maintainers("afzpatel", "srekolam", "renjithravindrankannath")

    license("MIT")

    version("6.3.0", sha256="f8e9703b5f78abba6f4a61f69ffc73225d1bb47b591cf33a26ed98060efd65d1")
    version("6.2.4", sha256="2230260fce0838583899f4969b936ca047b30985a0fffad276ea353232538770")
    version("6.2.1", sha256="56b795d471adad8ee9d7025544269e23929da31524d73db6f54396d3aca1445a")
    version("6.2.0", sha256="febe9011e0628ad62367fdc6c81bdb0ad4ed45803f79c794757ecea8bcfab58c")

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
