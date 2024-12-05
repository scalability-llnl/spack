# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class VectorclassVersion2(Package):
    """This is a C++ class library for using the Single Instruction Multiple
    Data (SIMD) instructions to improve performance on modern microprocessors
    with the x86 or x86/64 instruction set on Windows, Linux, and Mac platforms."""

    homepage = "https://www.agner.org/optimize/#vectorclass"
    url = "https://github.com/vectorclass/version2/archive/refs/tags/v2.01.04.tar.gz"

    maintainers("haralmha")

    license("Apache-2.0")

    version("2.01.04", sha256="7885c343b1af9eb940f4debdd7cd19544130a06ed70e0000e1a8471fb9c15118")

    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        # Put all cpp files to an include folder
        # (makes a filesystem view with this
        # package in it less noisy)
        install_tree(".", prefix.include)
