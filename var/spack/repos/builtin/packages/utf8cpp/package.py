# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Utf8cpp(CMakePackage):
    """A simple, portable and lightweight generic library for handling UTF-8
    encoded strings."""

    homepage = "https://github.com/nemtrif/utfcpp"
    url = "https://github.com/nemtrif/utfcpp/archive/refs/tags/v2.3.4.tar.gz"

    version("4.0.6", sha256="6920a6a5d6a04b9a89b2a89af7132f8acefd46e0c2a7b190350539e9213816c0")
    version("3.2.4", sha256="fde21a4c519eed25f095a1cd8490167409cc70d7b5e9c38756142e588ccb7c7e")
    version("2.3.4", sha256="1a26d07f88d173dbd26a45f645009d0c6f6ceeb5f0fc391b9f3a769d090a66f4")

    depends_on("c", type="build")
    depends_on("cxx", type="build")
