# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import path

from spack.package import *


class BeastTracer(Package):
    """Tracer is a graphical tool for visualization and diagnostics of MCMC
    output."""

    homepage = "https://beast.community/tracer"
    url = "https://github.com/beast-dev/tracer/archive/v1.7.1.tar.gz"

    version("1.7.2", sha256="fd891e2244445fef71ab8010d8fab924abff2e5436e035bb335834e7c2e6d83b")
    version("1.7.1", sha256="947d51c5afa52354099b9b182ba6036e352356bd62df94031f33cdcb7e8effd3")

    depends_on("c", type="build")  # generated

    depends_on("ant", type="build")
    depends_on("java", type=("build", "run"))

    def install(self, spec, prefix):
        ant = which("ant")
        ant("dist")

        mkdirp(prefix.bin)
        install(join_path(path.dirname(__file__), "tracer"), prefix.bin)
        install("build/dist/tracer.jar", prefix.bin)
