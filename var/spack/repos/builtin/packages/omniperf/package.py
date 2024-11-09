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

    version("6.2.1", sha256="c14cb73b9fe17a3cca31489a73e8ea49cb278093f8d64c433b1bac387445074a")
    version("6.2.0", sha256="b2ad49324a07aef977833d62741509a5d799b92758db56a16b4ab5636b6e231e")

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
