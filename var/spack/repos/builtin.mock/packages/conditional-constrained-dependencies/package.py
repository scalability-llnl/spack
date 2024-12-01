# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class ConditionalConstrainedDependencies(Package):
    """Package that has a variant which adds a dependency forced to
    use non default values.
    """

    homepage = "https://dev.null"

    version("1.0")

    # This variant is on by default and attaches a dependency
    # with a lot of variants set at their non-default values
    variant("dep", default=True, description="nope")
    depends_on("dep-with-variants+foo+bar+baz", when="+dep")
