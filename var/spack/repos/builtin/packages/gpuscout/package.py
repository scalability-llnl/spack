# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gpuscout(CMakePackage, CudaPackage):
    """GPUscout: A tool for discovering data movement-related bottlenecks on NVidia GPUs."""

    homepage = "https://github.com/caps-tum/GPUscout"
    url = "https://github.com/caps-tum/GPUscout/archive/refs/tags/v0.2.1.tar.gz"
    git = "https://github.com/caps-tum/GPUscout.git"

    maintainers("stepanvanecek")

    license("Apache-2.0")

    version(
        "0.2.1",
        sha256="78db030c443b971358905460c53c514134c18ebca9cafc26bfcfa297ff17683b",
        extension="tar.gz",
    )
    version("master", branch="master")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.27:", type="build")
    depends_on("cuda@12:")
