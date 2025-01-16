# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RArrow(RPackage):
    """'Apache' 'Arrow' <https://arrow.apache.org/> is a cross-language
    development platform for in-memory data. It specifies a standardized
    language-independent columnar memory format for flat and hierarchical
    data, organized for efficient analytic operations on modern
    hardware. This package provides an interface to the 'Arrow C++'
    library."""

    cran = "arrow"

    maintainers("viniciusvgp")

    version("11.0.0.2", sha256="6b179a2fceb62b676a032d19f9b880a1b6aecb92a5b39669f397385d82201a74")

    variant("notcran", description="Enable full-featured build.", default=False)

    depends_on("r-purrr", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))
    depends_on("r-tidyselect", type=("build", "run"))
    depends_on("r-bit64", type=("build", "run"))
    depends_on("r-assertthat", type=("build", "run"))
    depends_on("r-bit64", type=("build", "run"))
    depends_on("r-vctrs", type=("build", "run"))
    depends_on("r-cpp11", type=("build", "run"))

    def setup_build_environment(self, env):
        if self.spec.satisfies("+notcran"):
            env.set("NOT_CRAN", True)
