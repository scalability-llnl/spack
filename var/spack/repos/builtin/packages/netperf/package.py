# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Netperf(AutotoolsPackage):
    """Netperf is a benchmark that can be used to measure the performance
    of many different types of networking. It provides tests for both
    unidirectional throughput, and end-to-end latency."""

    homepage = "https://github.com/HewlettPackard/netperf"
    url = "https://github.com/HewlettPackard/netperf/archive/netperf-2.7.0.tar.gz"

    version("2.7.0", sha256="4569bafa4cca3d548eb96a486755af40bd9ceb6ab7c6abd81cc6aa4875007c4e")
    version("2.6.0", sha256="560b9c0ef0eed826941f74708b3ac53d91ec13b0b8c565fb107a1b5e6d99ded4")
    version("2.5.0", sha256="bebc94102fb74071cf289e0c116f83920dbd982f9e6c913ec0f1c7f6fcffbf77")

    depends_on("c", type="build")  # generated
