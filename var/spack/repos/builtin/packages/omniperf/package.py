# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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

    version("6.2.4", sha256="2230260fce0838583899f4969b936ca047b30985a0fffad276ea353232538770")
    version("6.2.1", sha256="56b795d471adad8ee9d7025544269e23929da31524d73db6f54396d3aca1445a")
    version("6.2.0", sha256="febe9011e0628ad62367fdc6c81bdb0ad4ed45803f79c794757ecea8bcfab58c")

    depends_on("python@3.8:")
    depends_on("py-pip", type="run")
    depends_on("py-astunparse@1.6.2", type=("build", "run"))  # wants exact version
    depends_on("py-colorlover", type=("build", "run"))
    depends_on("py-pyyaml")
    depends_on("py-matplotlib")
    depends_on("py-pandas")
    depends_on("py-pymongo")
    depends_on("py-tabulate")
    depends_on("py-tqdm")
    depends_on("py-kaleido")
    depends_on("py-plotille")
    depends_on("py-dash-svg", type=("build", "run"))
    depends_on("py-dash", type=("build", "run"))
    depends_on("py-dash-bootstrap-components", type=("build", "run"))

    # VERSION.sha is not in the auto-generated ROCm release tarball
    patch("0001-remove-VERSION.sha-install.patch")

    def cmake_args(self):
        args = [self.define("ENABLE_TESTS", self.run_tests)]
        return args

    @run_after("install")
    def after_install(self):
        touch(join_path(self.spec.prefix.libexec.omniperf, "VERSION.sha"))
