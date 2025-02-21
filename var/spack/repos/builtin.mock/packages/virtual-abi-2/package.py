# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class VirtualAbi2(Package):
    """
    This package provides `virtual-with-abi` and is conditionally ABI
    compatible with `virtual-abi-multi`
    """

    homepage = "https://www.example.com"
    has_code = False

    version("1.0")

    provides("virtual-with-abi")

    can_splice("virtual-abi-multi@1.0 abi=two", when="@1.0")

    def install(self, spec, prefix):
        touch(prefix.foo)
