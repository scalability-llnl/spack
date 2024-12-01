# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


def is_positive_int(val):
    try:
        return int(val) > 0
    except ValueError:
        return val == "auto"


class Lci(CMakePackage):
    """LCI: the Lightweight Communication Interface"""

    homepage = "https://github.com/uiuc-hpc/lci"
    url = "https://github.com/uiuc-hpc/lci/archive/refs/tags/v1.7.7.tar.gz"
    git = "https://github.com/uiuc-hpc/lci.git"

    maintainers("omor1", "JiakunYan")

    license("MIT")

    version("master", branch="master")
    version("1.7.7", sha256="c310f699b7b4317a2f5c3557f85c240fe3c85d2d06618dd248434ef807d53779")
    version("1.7.6", sha256="c88ccea2ad277ed38fc23187771b52b6fb212ed4429114717bfa8887ed21665c")
    version("1.7.5", sha256="13e4084c9e7aaf55966ba5aa0423164b8fd21ee7526fc62017b3c9b3db99cb83")
    version("1.7.4", sha256="00c6ef06bf90a02b55c72076dedf912580dcb1fb59fdc0e771d9e1a71283b72f")
    version("1.7.3", sha256="3c47d51d4925e6700294ac060c88a73c26ca6e9df5b4010d0e90b0bf5e505040")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "fabric",
        default="ibv",
        values=("ofi", "ibv", "ucx"),
        multi=False,
        description="Communication fabric",
    )

    variant("examples", default=False, description="Build LCI examples")
    variant("tests", default=False, description="Build LCI tests")
    variant("benchmarks", default=False, description="Build LCI benchmarks")
    variant("docs", default=False, description="Build LCI documentation")

    variant(
        "cache-line",
        default="auto",
        values=is_positive_int,
        description="Cache line size, in bytes",
    )

    variant(
        "multithread-progress",
        default=True,
        description="Enable thread-safe LCI_progress function",
    )
    variant("dreg", default="auto", description="Whether to use registration cache by default")
    variant(
        "packet-size",
        default="auto",
        values=is_positive_int,
        description="Size of packet by default",
    )
    variant(
        "npackets",
        default="auto",
        values=is_positive_int,
        description="Number of packets by default",
    )
    variant(
        "fabric-nsends-max",
        default="auto",
        values=is_positive_int,
        description="Max number of send descriptors that can be posted (send queue length) "
        "at the fabric layer by default",
    )
    variant(
        "fabric-nrecvs-max",
        default="auto",
        values=is_positive_int,
        description="Max number of receive descriptors that can be posted (receive queue length) "
        "at the fabric layer by default",
    )
    variant(
        "fabric-ncqes-max",
        default="auto",
        values=is_positive_int,
        description="Max number of completion queue entries that can be posted "
        "(completion queue length) at the fabric layer by default",
    )

    variant("debug", default=False, description="Enable the debug mode")
    variant("pcounter", default=False, description="Enable the performance counters")
    variant(
        "papi", default=False, description="Enable the PAPI plugin to collect hardware counters"
    )

    variant(
        "enable-pm",
        description="Process management backends to enable",
        values=disjoint_sets(("auto",), ("pmix", "pmi2", "pmi1", "mpi", "local"))
        .prohibit_empty_set()
        .with_default("auto")
        .with_non_feature_values("auto"),
    )
    variant(
        "default-pm",
        description="Order of process management backends to try by default",
        values=disjoint_sets(("auto",), ("pmix", "pmi2", "pmi1", "mpi", "local"), ("cray",))
        .prohibit_empty_set()
        .with_default("auto")
        .with_non_feature_values("auto"),
    )

    generator("ninja", "make", default="ninja")

    depends_on("cmake@3.12:", type="build")
    depends_on("libfabric", when="fabric=ofi")
    depends_on("rdma-core", when="fabric=ibv")
    depends_on("ucx", when="fabric=ucx")
    depends_on("mpi", when="enable-pm=mpi")
    depends_on("papi", when="+papi")
    depends_on("doxygen", when="+docs")
    depends_on("cray-pmi", when="default-pm=cray")

    def cmake_args(self):
        args = [
            self.define_from_variant("LCI_SERVER", "fabric"),
            self.define("LCI_FORCE_SERVER", True),
            self.define_from_variant("LCI_WITH_EXAMPLES", "examples"),
            self.define_from_variant("LCI_WITH_TESTS", "tests"),
            self.define_from_variant("LCI_WITH_BENCHMARKS", "benchmarks"),
            self.define_from_variant("LCI_WITH_DOC", "docs"),
            self.define_from_variant("LCI_ENABLE_MULTITHREAD_PROGRESS", "multithread-progress"),
            self.define_from_variant("LCI_DEBUG", "debug"),
            self.define_from_variant("LCI_USE_PERFORMANCE_COUNTER", "pcounter"),
            self.define_from_variant("LCI_USE_PAPI", "papi"),
        ]

        if not self.spec.satisfies("dreg=auto"):
            args.append(self.define_from_variant("LCI_USE_DREG_DEFAULT", "dreg"))

        if not self.spec.satisfies("enable-pm=auto"):
            args.extend(
                [
                    self.define(
                        "LCT_PMI_BACKEND_ENABLE_PMI1", self.spec.satisfies("enable-pm=pmi1")
                    ),
                    self.define(
                        "LCT_PMI_BACKEND_ENABLE_PMI2", self.spec.satisfies("enable-pm=pmi2")
                    ),
                    self.define(
                        "LCT_PMI_BACKEND_ENABLE_MPI", self.spec.satisfies("enable-pm=mpi")
                    ),
                    self.define(
                        "LCT_PMI_BACKEND_ENABLE_PMIX", self.spec.satisfies("enable-pm=pmix")
                    ),
                ]
            )

        if self.spec.satisfies("default-pm=cray"):
            args.extend(
                [
                    self.define("LCI_PMI_BACKEND_DEFAULT", "pmi1"),
                    self.define("LCT_PMI_BACKEND_ENABLE_PMI1", True),
                ]
            )
        elif not self.spec.satisfies("default-pm=auto"):
            args.append(self.define_from_variant("LCI_PMI_BACKEND_DEFAULT", "default-pm"))

        if not self.spec.satisfies("cache-line=auto"):
            args.append(self.define_from_variant("LCI_CACHE_LINE", "cache-line"))

        if not self.spec.satisfies("packet-size=auto"):
            args.append(self.define_from_variant("LCI_PACKET_SIZE_DEFAULT", "packet-size"))

        if not self.spec.satisfies("npackets=auto"):
            args.append(self.define_from_variant("LCI_SERVER_NUM_PKTS_DEFAULT", "npackets"))

        if not self.spec.satisfies("fabric-nsends-max=auto"):
            args.append(
                self.define_from_variant("LCI_SERVER_MAX_SENDS_DEFAULT", "fabric-nsends-max")
            )

        if not self.spec.satisfies("fabric-nrecvs-max=auto"):
            args.append(
                self.define_from_variant("LCI_SERVER_MAX_RECVS_DEFAULT", "fabric-nrecvs-max")
            )

        if not self.spec.satisfies("fabric-ncqes-max=auto"):
            args.append(
                self.define_from_variant("LCI_SERVER_MAX_CQES_DEFAULT", "fabric-ncqes-max")
            )

        return args
