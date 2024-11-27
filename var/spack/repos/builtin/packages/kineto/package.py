# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kineto(CMakePackage):
    """A CPU+GPU Profiling library that provides access to timeline traces
    and hardware performance counters."""

    homepage = "https://github.com/pytorch/kineto"
    git = "https://github.com/pytorch/kineto.git"

    license("BSD-3-Clause")

    version("master", branch="master", submodules=True)
    version(
        "2021-05-12", commit="a631215ac294805d5360e0ecceceb34de6557ba8", submodules=True
    )  # py-torch@1.9
    version(
        "2021-03-16", commit="ce98f8b95b2ee5ffed257ca90090cd8adcf15b53", submodules=True
    )  # py-torch@1.8.1
    version(
        "2021-02-04", commit="258d9a471f8d3a50a0f52b85c3fe0902f65489df", submodules=True
    )  # py-torch@1.8.0

    depends_on("cxx", type="build")  # generated

    root_cmakelists_dir = "libkineto"

    generator("ninja")
    depends_on("cmake@3.5:", type="build")
    depends_on("python", type="build")
    depends_on("cuda")
