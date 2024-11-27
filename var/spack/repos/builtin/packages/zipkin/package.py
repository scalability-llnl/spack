# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Zipkin(MavenPackage):
    """Zipkin is a distributed tracing system. It helps gather timing
    data needed to troubleshoot latency problems in service
    architectures. Features include both the collection and lookup
    of this data."""

    homepage = "https://zipkin.io/"
    url = "https://github.com/openzipkin/zipkin/archive/2.21.5.tar.gz"

    license("Apache-2.0")

    version("2.21.5", sha256="e643a810f82f9ea50e2cb6847694c7645507d3deae77685a3a1bb841e0f885a2")
    version("2.21.4", sha256="ee7b0110b3852479c925b6429ff278aa38b1d5da27f4762891b1f863e67bdad5")
    version("2.21.3", sha256="02526e2ba4de85938b510cb2db01865ec46cdad53157862c39fa5e9b6cbd15b6")

    depends_on("maven@1.8:14", type="build")
