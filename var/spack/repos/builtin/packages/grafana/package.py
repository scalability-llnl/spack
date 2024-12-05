# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Grafana(Package):
    """The tool for beautiful monitoring and metric analytics & dashboards
    for Graphite, InfluxDB & Prometheus & More"""

    homepage = "https://grafana.com"
    url = "https://github.com/grafana/grafana/archive/v6.7.3.tar.gz"

    license("AGPL-3.0-only")

    version("6.7.3", sha256="2477b70bfc8770ab844ee683f72b5efe8a47324b9779663d8e5259ffb9ddb8d8")
    version("6.7.2", sha256="dc81cdb77c1c0ae99ae3302a0ef8b3d577f4a717208a90df65da8fcb282122fc")
    version("6.7.1", sha256="5750d286273069a195679d5586e810b0ca8cdd08ee07dcdd9b52cfaac8c62b89")
    version("6.7.0", sha256="7f4e3f0d42b8188a334e97062c3bf63ff43af273095ba10147b299e3c1c5a7b7")
    version("6.6.2", sha256="e11e5971d08e45e277b55e060c0ce3cf25ca0ba144367c53b4836f2d133ed9b8")

    depends_on("c", type="build")  # generated

    depends_on("go", type="build")

    def install(self, spec, prefix):
        go = which("go")
        go("run", "build.go", "build")
        install_tree("bin", prefix.bin)
