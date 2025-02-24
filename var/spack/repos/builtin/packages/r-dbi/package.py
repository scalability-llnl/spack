# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDbi(RPackage):
    """R Database Interface.

    A database interface definition for communication between R and relational
    database management systems. All classes in this package are virtual and
    need to be extended by the various R/DBMS implementations."""

    cran = "DBI"

    version("1.2.3", sha256="cf6708a7566a80929f06575aa345fae354714159ed5fab5db14306fc5d0d2dbe")
    version("1.1.3", sha256="38bb33753da5bddb78893a5228a5d269dae3bf16f21dc5d9853ac9c24d31428d")
    version("1.1.2", sha256="56ec377d471c76ac234ddfd313bd01a050c99fb6fa5f704f5333b34a5d714f58")
    version("1.1.1", sha256="572ab3b8a6421d0ac3e7665c4c842826f1723af98fca25d4f43edb419e771344")
    version("1.1.0", sha256="a96db7fa39a58f1ed34c6e78d8f5f7e4cf0882afb301323b5c6975d6729203e4")
    version("1.0.0", sha256="ff16f118eb3f759183441835e932b87358dd80ab9800ce576a8f3df1b6f01cf5")
    version("0.4-1", sha256="eff14a9af4975f23f8e1f4347d82c33c32c0b4f4f3e11370c582a89aeb8ac68e")
    version("0.7", sha256="2557d5d59a45620ec9de340c2c25eec4cc478d3fc3f8b87979cf337c5bcfde11")

    depends_on("r@3.0.0:", type=("build", "run"))
