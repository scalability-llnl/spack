# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Memaxes(CMakePackage):
    """MemAxes is a visualizer for sampled memory trace data."""

    homepage = "https://github.com/llnl/MemAxes"

    license("LGPL-2.1-or-later")

    version(
        "0.5",
        sha256="9858f0f675b50e347d0b88545558e5d6b4333347c762b15d399b8d8004d7b68b",
        url="https://github.com/llnl/MemAxes/archive/v0.5.tar.gz",
    )

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@2.8.9:", type="build")
    depends_on("qt@5:")
