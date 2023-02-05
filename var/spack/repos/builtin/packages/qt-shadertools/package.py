# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import os
import shutil

from spack.package import *
from spack.pkg.builtin.qt_base import QtBase


class QtShadertools(CMakePackage):
    """APIs and tools in this module provide the producer functionality for the
    shader pipeline that allows Qt Quick to operate on Vulkan, Metal, and
    Direct3D, in addition to OpenGL."""

    homepage = "https://www.qt.io"
    url = "https://github.com/qt/qtshadertools/archive/refs/tags/v6.2.3.tar.gz"
    list_url = "https://github.com/qt/qtshadertools/tags"

    maintainers = ["wdconinc", "sethrj"]

    version("6.4.2", sha256="7f29a78769f454fe529595acb693aa67812e80d894162ddad3f0444f65a22268")
    version("6.4.1", sha256="d325724c4ed79c759ac8cbbca5f9fd4b0e6e8d61a9ac58921cb1dac75c104687")
    version("6.4.0", sha256="51bf312965bd673193221cd49019f504feb79c0bf0ff01d6a6ca5c8d15f9d7c1")
    version("6.3.2", sha256="ec73303e6c91cddae402b1ac0d18a0d35619f348785514be30cec2791cd63faa")
    version("6.3.1", sha256="1b8b18b6ece4d92d0bf60a3b2a9924b45c369968cc77217796434ac7c5c6628f")
    version("6.3.0", sha256="3c36d83fc036a144722ce056b2840260005dcbd338e11b9c527d7266a54afd45")
    version("6.2.4", sha256="c3332d91e0894086634d5f8d40638439e6e3653a3a185e1b5f5d23ae3b9f51a1")
    version("6.2.3", sha256="658c4acc2925e57d35bbd38cdf49c08297555ed7d632f9e86bfef76e6d861562")

    generator = "Ninja"

    # Changing default to Release for typical use in HPC contexts
    variant(
        "build_type",
        default="Release",
        values=("Release", "Debug", "RelWithDebInfo", "MinSizeRel"),
        description="CMake build type",
    )

    depends_on("cmake@3.16:", type="build")
    depends_on("ninja", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("python", when="@5.7.0:", type="build")

    for _v in QtBase.versions:
        v = str(_v)
        depends_on("qt-base@" + v, when="@" + v)

    def patch(self):
        vendor_dir = join_path(self.stage.source_path, "src", "3rdparty")
        vendor_deps_to_remove = []
        QtBase.remove_verdor_deps(vendor_dir, vendor_deps_to_remove)
