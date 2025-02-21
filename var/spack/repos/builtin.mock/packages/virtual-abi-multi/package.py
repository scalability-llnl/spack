# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class VirtualAbiMulti(Package):
    """
    This package provides `virtual-with-abi` is ABI compatible with either
    `virtual-abi-1` or `virtual-abi-2` depending on the value of its `abi`
    variant
    """

    homepage = "https://www.example.com"
    has_code = False

    version("1.0")

    variant("abi", default="custom", multi=False, values=("one", "two", "custom"))

    provides("virtual-with-abi")

    can_splice("virtual-abi-1@1.0", when="@1.0 abi=one")
    can_splice("virtual-abi-2@1.0", when="@1.0 abi=two")

    def install(self, spec, prefix):
        touch(prefix.foo)
