# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RLifecycle(RPackage):
    """Manage the Life Cycle of your Package Functions.

    Manage the life cycle of your exported functions with shared conventions,
    documentation badges, and non-invasive deprecation warnings. The
    'lifecycle' package defines four development stages (experimental,
    maturing, stable, and questioning) and three deprecation stages
    (soft-deprecated, deprecated, and defunct). It makes it easy to insert
    badges corresponding to these stages in your documentation. Usage of
    deprecated functions are signalled with increasing levels of non-invasive
    verbosity."""

    cran = "lifecycle"

    license("MIT")

    version("1.0.4", sha256="ada4d3c7e84b0c93105e888647c5754219a8334f6e1f82d5afaf83d4855b91cc")
    version("1.0.3", sha256="6459fdc3211585c0cdf120427579c12149b02161efe273a64b825c05e9aa69c2")
    version("1.0.1", sha256="1da76e1c00f1be96ca34e122ae611259430bf99d6a1b999fdef70c00c30f7ba0")
    version("0.2.0", sha256="29746e8dee05d4e36f9c612e8c7a903a4f648a36b3b94c9776e518c38a412224")

    depends_on("r@3.2:", type=("build", "run"))
    depends_on("r@3.3:", type=("build", "run"), when="@1:")
    depends_on("r@3.4:", type=("build", "run"), when="@1.0.3:")
    depends_on("r@3.6:", type=("build", "run"), when="@1.0.4:")
    depends_on("r-cli@3.4.0:", type=("build", "run"), when="@1.0.3:")
    depends_on("r-glue", type=("build", "run"))
    depends_on("r-rlang@0.4.0:", type=("build", "run"))
    depends_on("r-rlang@1.0.6:", type=("build", "run"), when="@1.0.3:")
    depends_on("r-rlang@1.1.0:", type=("build", "run"), when="@1.0.4:")
