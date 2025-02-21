# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class DependsOnVirtualWithAbi(Package):
    """
    This has a virtual dependency on `virtual-with-abi`, mostly for testing
    automatic splicing of providers.
    """

    homepage = "https://www.example.com"
    has_code = False

    version("1.0")
    depends_on("virtual-with-abi")
