# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Prometheus(MakefilePackage):
    """Prometheus, a Cloud Native Computing Foundation project, is a
    systems and service monitoring system."""

    homepage = "https://prometheus.io/"
    url = "https://github.com/prometheus/prometheus/archive/v2.19.2.tar.gz"

    license("Apache-2.0")

    version("2.19.2", sha256="d4e84cae2fed6761bb8a80fcc69b6e0e9f274d19dffc0f38fb5845f11da1bbc3")
    version("2.19.1", sha256="b72b9b6bdbae246dcc29ef354d429425eb3c0a6e1596fc8b29b502578a4ce045")
    version("2.18.2", sha256="a26c106c97d81506e3a20699145c11ea2cce936427a0e96eb2fd0dc7cd1945ba")
    version("2.17.1", sha256="d0b53411ea0295c608634ca7ef1d43fa0f5559e7ad50705bf4d64d052e33ddaf")
    version("2.17.0", sha256="b5e508f1c747aaf50dd90a48e5e2a3117fec2e9702d0b1c7f97408b87a073009")

    depends_on("c", type="build")  # generated

    depends_on("go", type="build")
    depends_on("node-js@11.10.1:", type="build")
    depends_on("yarn", type="build")

    def build(self, spec, prefix):
        make("build", parallel=False)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("prometheus", prefix.bin)
        install("promtool", prefix.bin)
        install("tsdb/tsdb", prefix.bin)
        install_tree("documentation", prefix.documentation)
