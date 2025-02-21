# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGh(RPackage):
    """'GitHub' 'API'.

    Minimal client to access the 'GitHub' 'API'."""

    cran = "gh"

    license("MIT")

    version("1.4.1", sha256="76bd3f2a31eeaf76a633362899a20b0f7e8fb6159d4777baf3da2a47854292af")
    version("1.4.0", sha256="68c69fcd18429b378e639a09652465a4e92b7b5b5704804d0c5b1ca2b9b58b71")
    version("1.3.1", sha256="fbaea2abdeceb03d28839fd0e58c2eea01092f9ef92dcc044718ef0d298612ef")
    version("1.3.0", sha256="a44039054e8ca56496f2d9c7a10cdadf4a7383bc91086e768ba7e7f1fbcaed1c")
    version("1.2.0", sha256="2988440ed2ba4b241c8ffbafbfdad29493574980a9aeba210521dadda91f7eff")
    version("1.1.0", sha256="de9faf383c3fe5e87a75391d82cf71b1331b3c80cd00c4203146a303825d89ad")
    version("1.0.1", sha256="f3c02b16637ae390c3599265852d94b3de3ef585818b260d00e7812595b391d2")

    depends_on("r@3.4:", type=("build", "run"), when="@1.3.1:")
    depends_on("r@3.6:", type=("build", "run"), when="@1.4.1:")

    depends_on("r-cli", type=("build", "run"), when="@1.1.0:")
    depends_on("r-cli@2.0.1:", type=("build", "run"), when="@1.2.0:")
    depends_on("r-cli@3.0.1:", type=("build", "run"), when="@1.3.1:")
    depends_on("r-gitcreds", type=("build", "run"), when="@1.2.0:")
    depends_on("r-glue", type=("build", "run"), when="@1.4.1:")
    depends_on("r-httr2", type=("build", "run"), when="@1.4.0:")
    depends_on("r-ini", type=("build", "run"))
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-lifecycle", type=("build", "run"), when="@1.4.1:")
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@1.4.0:")
    depends_on("r-httr@1.2:", type=("build", "run"), when="@1.1.0:1.3.1")
