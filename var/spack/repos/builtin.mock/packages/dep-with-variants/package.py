# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class DepWithVariants(Package):
    """Package that has a variant which adds a dependency forced to
    use non default values.
    """

    homepage = "https://dev.null"

    version("1.0")

    variant("foo", default=False, description="nope")
    variant("bar", default=False, description="nope")
    variant("baz", default=False, description="nope")
