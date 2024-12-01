# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Countdown(CMakePackage, CudaPackage):
    """COUNTDOWN is a tool for identifying and automatically reducing the power
    consumption of the computing elements, during communication and
    synchronization primitives, filtering out phases which would detriment the
    time to solution of the application."""

    homepage = "https://github.com/EEESlab/countdown"
    url = "https://github.com/EEESlab/countdown/archive/refs/tags/v1.1.1.tar.gz"

    license("BSD-3-Clause")

    maintainers("f-tesser", "danielecesarini")

    version("1.1.1", sha256="ee7f00ffc047f000a21a7a71f6ea6f4049afb1a8407608adc04993929ceba917")

    depends_on("c", type="build")  # generated

    variant(
        "acc_mpi",
        default=True,
        description="Enable the instrumentation of all accessory MPI functions",
    )
    variant(
        "coll_mpi",
        default=True,
        description="Enable the instrumentation of all collective MPI functions",
    )
    variant("debug_mpi", default=False, description="Enable the debug prints on MPI functions")
    variant(
        "excl_all_mpi",
        default=False,
        description="Disable the instrumentation of all MPI functions, "
        "except for initialization and finalization",
    )
    variant("hwp_auto_discovery", default=True, description="Autodiscovery of hwp-states")
    variant("mosquitto", default=False, description="Enable MQTT message passing")
    variant("no_profiling", default=False, description="Disable MPI profiling")
    variant("use_cpufreq", default=True, description="Manual set of cpufreq interface")
    variant("use_hwp", default=False, description="Manual set if hwp-states are available")
    variant(
        "p2p_mpi",
        default=True,
        description="Enable the instrumentation of all point-to-point MPI functions",
    )
    variant("shared", default=True, description="Build shared libraries")

    conflicts("+acc_mpi", when="+excl_all_mpi")
    conflicts("+coll_mpi", when="+excl_all_mpi")
    conflicts("+p2p_mpi", when="+excl_all_mpi")
    conflicts("+excl_all_mpi", when="+acc_mpi")
    conflicts("+excl_all_mpi", when="+coll_mpi")
    conflicts("+excl_all_mpi", when="+p2p_mpi")
    conflicts("+hwp_auto_discovery", when="+use_cpufreq")
    conflicts("+hwp_auto_discovery", when="+use_hwp")
    conflicts("+use_cpufreq", when="+hwp_auto_discovery")
    conflicts("+use_cpufreq", when="+use_hwp")
    conflicts("+use_hwp", when="+hwp_auto_discovery")
    conflicts("+use_hwp", when="+use_cpufreq")

    depends_on("cmake@3.0.0:", type="build")
    depends_on("hwloc", type="link")
    depends_on("mpi@3.0.0:", type="link")
    depends_on("mosquitto", when="+mosquitto", type="link")

    def cmake_args(self):
        args = [
            self.define_from_variant("CNTD_ENABLE_CUDA", "cuda"),
            self.define_from_variant("CNTD_DISABLE_ACCESSORY_MPI", "acc_mpi"),
            self.define_from_variant("CNTD_ENABLE_COLLECTIVE_MPI", "coll_mpi"),
            self.define_from_variant("CNTD_ENABLE_DEBUG_MPI", "debug_mpi"),
            self.define_from_variant("CNTD_DISABLE_ALL_MPI_EXCEPT_INI_FIN", "excl_all_mpi"),
            self.define_from_variant("CNTD_HWP_AUTO_DISCOVER", "hwp_auto_discovery"),
            self.define_from_variant("CNTD_ENABLE_MOSQUITTO", "mosquitto"),
            self.define_from_variant("CNTD_DISABLE_PROFILING_MPI", "no_profiling"),
            self.define_from_variant("CNTD_USE_CPUFREQ", "use_cpufreq"),
            self.define_from_variant("CNTD_HWP_DISCOVERED", "use_hwp"),
            self.define_from_variant("CNTD_ENABLE_P2P_MPI", "p2p_mpi"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]

        return args
