# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Imgui(Package):
    """Dear ImGui is a bloat-free graphical user interface library for C++.

    It outputs optimized vertex buffers that you can render anytime in your 3D-pipeline
    enabled application. It is fast, portable, renderer agnostic and self-contained
    (no external dependencies)."""

    homepage = "https://github.com/ocornut/imgui"
    url = "https://github.com/ocornut/imgui/archive/refs/tags/v1.85.tar.gz"

    license("MIT")

    version("1.90.6", sha256="70b4b05ac0938e82b4d5b8d59480d3e2ca63ca570dfb88c55023831f387237ad")
    version("1.85", sha256="7ed49d1f4573004fa725a70642aaddd3e06bb57fcfe1c1a49ac6574a3e895a77")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        # No specific build process is required.
        # You can add the .cpp files to your existing project.
        install_tree(".", prefix)
