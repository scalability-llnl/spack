# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Tinygltf(CMakePackage):
    """Header only C++11 tiny glTF 2.0 library."""

    homepage = "https://github.com/syoyo/tinygltf"
    url = "https://github.com/syoyo/tinygltf/archive/refs/tags/v2.5.0.tar.gz"
    git = "https://github.com/syoyo/tinygltf/"

    license("MIT")

    version("release", branch="release")
    version("2.8.21", sha256="e567257d7addde58b0a483832cbaa5dd8f15e5bcaee6f023831e215d1a2c0502")
    version("2.8.14", sha256="63cd43746c9ddfe5777494500422e831a312299e386fbf80922839dc1a5575f8")
    version("2.7.0", sha256="a1bbc0b831719e3a809a1bb01ce299a60e80b4e15221f58e822303ba22a69d45")
    version("2.6.3", sha256="f61e4a501baa7fbf31b18ea0f6815a59204ad0de281f7b04f0168f6bbd17c340")
    version("2.5.0", sha256="5d85bd556b60b1b69527189293cfa4902957d67fabb8582b6532f23a5ef27ec1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.6:", type="build")
