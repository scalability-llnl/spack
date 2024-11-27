# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ftxui(CMakePackage):
    """Functional Terminal (X) User interface.
    A simple C++ library for terminal based user interfaces."""

    homepage = "https://arthursonzogni.github.io"
    url = "https://github.com/ArthurSonzogni/FTXUI/archive/refs/tags/v2.0.0.tar.gz"

    license("MIT")

    version("5.0.0", sha256="a2991cb222c944aee14397965d9f6b050245da849d8c5da7c72d112de2786b5b")
    version("4.1.1", sha256="9009d093e48b3189487d67fc3e375a57c7b354c0e43fc554ad31bec74a4bc2dd")
    version("4.0.0", sha256="7276e4117429ebf8e34ea371c3ea4e66eb99e0f234cb4c5c85fca17174a53dfa")
    version("2.0.0", sha256="d891695ef22176f0c09f8261a37af9ad5b262dd670a81e6b83661a23abc2c54f")

    depends_on("cxx", type="build")  # generated
