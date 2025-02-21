# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBlockmodeling(RPackage):
    """Generalized and Classical Blockmodeling of Valued Networks.

    This is primarily meant as an implementation of generalized blockmodeling
    for valued networks."""

    cran = "blockmodeling"

    license("GPL-2.0-or-later")

    version("1.1.5", sha256="3b6f910078c29b801651e3a686112e41e456c517e1b99fcda11bb12681bb1503")
    version("1.1.4", sha256="69ce17ed96ca754a6308edb62188e0040e357568b975ce8986f68ecb2fead2b8")
    version("1.1.3", sha256="5f705f92c9b96dcbdd6f109c6a99f88d70c576485369700b82391b6a75afbda6")
    version("1.0.5", sha256="18c227bb52f28aff4dae8929563474e3e006e238438c823b67dc6baa897f88ed")
    version("1.0.0", sha256="f10c41fff56dc7dc46dffbceacb8ff905eca06578d610a5a590fb408f0149cfc")
    version("0.3.4", sha256="a269c83669dd5294cff0adddab36bc023db6a276a06b74b1fa94b7e407486987")
    version("0.3.1", sha256="39e8360400cec6baa920d5589d4e779568bdf2954f7331be0e3cadf22a217d31")

    depends_on("r@2.10:", type=("build", "run"))
    depends_on("r-matrix", type=("build", "run"))

    depends_on("r-doparallel", type=("build", "run"), when="@:0.3.4")
    depends_on("r-dorng", type=("build", "run"), when="@:0.3.4")
    depends_on("r-foreach", type=("build", "run"), when="@:0.3.4")
