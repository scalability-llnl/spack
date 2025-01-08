# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGtable(RPackage):
    """Arrange 'Grobs' in Tables.

    Tools to make it easier to work with "tables" of 'grobs'. The 'gtable'
    package defines a 'gtable' grob class that specifies a grid along with a
    list of grobs and their placement in the grid. Further the package makes it
    easy to manipulate and combine 'gtable' objects so that complex
    compositions can be build up sequentially."""

    cran = "gtable"

    license("MIT")

    version("0.3.5", sha256="b19fc1a30359945adbab7d4e915fe95523a839c380e34ae705d70b7ebddeea72")
    version("0.3.3", sha256="2f9a58d978e2a487b7fd8841539ea33cf948e55ddf6f7a9bd2dd3362600a7b3a")
    version("0.3.1", sha256="8bd62c5722d5188914d667cabab12991c555f657f4f5ce7b547571ae3aec7cb5")
    version("0.3.0", sha256="fd386cc4610b1cc7627dac34dba8367f7efe114b968503027fb2e1265c67d6d3")
    version("0.2.0", sha256="801e4869830ff3da1d38e41f5a2296a54fc10a7419c6ffb108582850c701e76f")

    depends_on("r@3.0:", type=("build", "run"))
    depends_on("r@3.5:", type=("build", "run"), when="@0.3.3:")
    depends_on("r-rlang@1.1.0:", type=("build", "run"), when="@0.3.3:")
    depends_on("r-lifecycle", type=("build", "run"), when="@0.3.3:")
    depends_on("r-glue", type=("build", "run"), when="@0.3.3:")
    depends_on("r-cli", type=("build", "run"), when="@0.3.3:")
