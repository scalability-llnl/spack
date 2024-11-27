# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class SysSage(CMakePackage):
    """A library for capturing hardware topology and attributes of compute systems."""

    homepage = "https://github.com/caps-tum/sys-sage"
    url = "https://github.com/caps-tum/sys-sage/archive/refs/tags/v0.4.3.tar.gz"
    git = "https://github.com/caps-tum/sys-sage.git"

    maintainers("stepanvanecek")

    license("Apache-2.0")

    version("0.5.0", sha256="044e53bf0f3873325fa4dedb510849d58b23b5a2c654d41b1389a318b2cb7ee1")
    version("0.4.3", sha256="e24313c4274576c1511a62e1b27c86a78cea7e4c123b8a53303cfc70de978faa")
    version("master", branch="master")
    version("develop", branch="develop")

    depends_on("cxx", type="build")  # generated

    conflicts("%gcc@:7", msg="gcc can be used from version 8 and above")

    variant(
        "nvidia_mig",
        default=False,
        description="Build and install functionality regarding NVidia MIG(multi-instance GPU, "
        "ampere or newer).",
    )
    variant(
        "cpuinfo",
        default=True,
        description="Build and install functionality regarding Linux cpuinfo (only x86) -- "
        "default ON.",
    )
    variant(
        "build_data_sources",
        default=False,
        when="platform=linux",
        description="Build all data sources (programs to collect data about the machine sys-sage "
        "runs on).",
    )
    variant(
        "ds_hwloc",
        default=False,
        description="Builds the hwloc data source for retrieving the CPU topology",
    )
    variant(
        "ds_numa",
        default=False,
        when="platform=linux",
        description="builds the caps-numa-benchmark. If turned on, includes Linux-specific "
        "libraries.",
    )

    depends_on("cmake@3.22:", type="build")
    depends_on("libxml2@2.9.13:")

    depends_on("numactl", when="+build_data_sources platform=linux")
    depends_on("numactl", when="+ds_numa platform=linux")
    depends_on("hwloc@2.9:", when="+build_data_sources")
    depends_on("hwloc@2.9:", when="+ds_hwloc")
    depends_on("cuda", when="+nvidia_mig platform=linux")
    depends_on("cuda", when="+build_data_sources platform=linux")

    def cmake_args(self):
        spec = self.spec
        args = []
        args.append(self.define_from_variant("NVIDIA_MIG", "nvidia_mig"))
        if "+cpuinfo" in spec and spec.target == "x86_64" and spec.platform == "linux":
            args.append(self.define("CPUINFO", True))
        else:
            args.append(self.define("CPUINFO", False))
        if "+ds_hwloc" in spec or "+build_data_sources" in spec:
            args.append(self.define("DS_HWLOC", True))
        if "+ds_numa" in spec or "+build_data_sources" in spec:
            args.append(self.define("DS_NUMA", True))
        return args
