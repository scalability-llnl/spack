# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


class PyGurobipy(PythonPackage):
    """Python interface to the Gurobi Optimizer"""

    homepage = "https://www.gurobi.com"
    pypi = "https://pypi.org/project/gurobipy/"
    list_url = "https://pypi.org/simple/gurobipy/"

    def url_for_version(self, version):
        url = "https://pypi.io/packages/cp{1}/g/gurobipy/gurobipy-{0}-cp{1}-cp{1}-{2}.whl"

        arch = platform.machine()

        platform_string = ""

        if arch == "x86_64":
            platform_string = "manylinux2014_x86_64.manylinux_2_17_x86_64"
        elif arch == "aarch64":
            platform_string = "manylinux2014_aarch64.manylinux_2_17_aarch64"

        py_ver = Version(version.string.split("y")[1])

        final_url = url.format(version.string.split("-")[0], py_ver.joined, platform_string)

        return final_url

    arch = platform.machine()

    if arch == "x86_64":
        version(
            "12.0.0-py3.12",
            sha256=("90bba495efb25cff5a3826158aff7be29637d2e80accc3a89a98cb8630856106"),
            expand=False,
        )
        version(
            "12.0.0-py3.11",
            sha256=("a08fb42a5e7cb02cdb993c1381c8b8c5a3baeedcadd56e7288d8458a57b81442"),
            expand=False,
        )
        version(
            "12.0.0-py3.10",
            sha256=("71ea7c653a92377991291a7e81b456fdfd06f8e3fc36b74a54444c2bab5225a8"),
            expand=False,
        )
        version(
            "12.0.0-py3.9",
            sha256=("5e0b0ea5ce2eaf4bd940821860fe37dcc8fd3fe7215ab0d97cceaedfa5eeb15d"),
            expand=False,
        )
    elif arch == "aarch64":
        version(
            "12.0.0-py3.12",
            sha256=("f8287de7535c3b9c97f4aa8716969d70302a972bd09e9d3b6fbd7266ca0eab72"),
            expand=False,
        )
        version(
            "12.0.0-py3.11",
            sha256=("fc3892e3d88d0f8a01da75f12f74023d398ef599a9e1add66ed76313733e30fb"),
            expand=False,
        )
        version(
            "12.0.0-py3.10",
            sha256=("d4803e659fefc2102e9dc3d84f3d7f54a3918127c362cbebae6103b7e13849c6"),
            expand=False,
        )
        version(
            "12.0.0-py3.9",
            sha256=("68c0ffe4ac8c4d87662307f96f50f40ddc3867d71c6ebabce4bda52f4688ecbd"),
            expand=False,
        )
    else:
        conflicts(f"target={arch}:", msg=f"py-gurobi is not available for {arch}")

    conflicts("target=ppc64:", msg="gurobipy wheels are not available for powerpc")
    conflicts("target=ppc64le:", msg="gurobipy wheels are not available for powerpc")

    depends_on("python@3.9.0:3.9", type=("build", "run"), when="@12.0.0-py3.9")
    depends_on("python@3.10.0:3.10", type=("build", "run"), when="@12.0.0-py3.10")
    depends_on("python@3.11.0:3.11", type=("build", "run"), when="@12.0.0-py3.11")
    depends_on("python@3.12.0:3.12", type=("build", "run"), when="@12.0.0-py3.12")

    depends_on("py-pip", type="build")

    def install(self, spec, prefix):
        """Install using pip with the downloaded wheel"""
        pip = which("pip")
        pip("install", self.stage.archive_file, "--prefix=" + prefix)
