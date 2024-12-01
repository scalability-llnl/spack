# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVctrs(RPackage):
    """Vector Helpers.

    Defines new notions of prototype and size that are used to provide tools
    for consistent and well-founded type-coercion and size-recycling, and are
    in turn connected to ideas of type- and size-stability useful for analyzing
    function interfaces."""

    cran = "vctrs"

    license("MIT")

    version("0.6.5", sha256="43167d2248fd699594044b5c8f1dbb7ed163f2d64761e08ba805b04e7ec8e402")
    version("0.6.4", sha256="8a80192356e724d21bd89a0ce3e5835856fd5bb1651e7fc205c6fee58fd001c8")
    version("0.6.3", sha256="93dc220dcde8b440586b2260460ef354e827a17dfec1ea6a9815585a10cfa5c2")
    version("0.6.2", sha256="feecabe11f6c55e04377d36fa59842187f0a6fe52aaf867c08289a948781ee84")
    version("0.6.1", sha256="77552463bd7c40af2618d635de6bb9ad1614d161a5e34d90167601dc5e8e1283")
    version("0.6.0", sha256="be0b712c4e6aae353120a60ded6a4301eb9631c8d256927b79b9ad83b4299757")
    version("0.5.2", sha256="76bf10243b9b31e23f56ffdaa1677a01767699e2098487f86bd42cb801d8c047")
    version("0.5.1", sha256="497982f717f21e7612b84940e95c282e2a96b942e6d47108f92cd92b7341db07")
    version("0.5.0", sha256="7c372e13c39ddace9c9bb9f33238de6dd2cd0f37dcc7054ba6435d271e5df686")
    version("0.4.2", sha256="5414d1d6977163b4e85efa40d6facdd98089d6ffd460daaba729d4200942d815")
    version("0.4.1", sha256="9676881e009aa1217818f326338e8b35dd9a9438918f8b1ac249f4c8afe460dd")
    version("0.3.8", sha256="7f4e8b75eda115e69dddf714f0643eb889ad61017cdc13af24389aab2a2d1bb1")
    version("0.3.6", sha256="df7d368c9f2d2ad14872ba2a09821ec4f5a8ad77c81a0b05e1f440e5ffebad25")
    version("0.3.5", sha256="11605d98106e294dae1a9b205462dd3906a6159a647150752b85dd290f6635cc")
    version("0.2.0", sha256="5bce8f228182ecaa51230d00ad8a018de9cf2579703e82244e0931fe31f20016")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("r@3.2:", type=("build", "run"))
    depends_on("r@3.3:", type=("build", "run"), when="@0.3.5:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@0.6.2:")
    depends_on("r-cli@3.2.0:", type=("build", "run"), when="@0.4.1:")
    depends_on("r-cli@3.4.0:", type=("build", "run"), when="@0.5.0:")
    depends_on("r-glue", type=("build", "run"))
    depends_on("r-lifecycle@1.0.3:", type=("build", "run"), when="@0.5.0:")
    depends_on("r-rlang@0.4.0:", type=("build", "run"))
    depends_on("r-rlang@0.4.7:", type=("build", "run"), when="@0.3.5:")
    depends_on("r-rlang@0.4.10:", type=("build", "run"), when="@0.3.7:")
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@0.4.1:")
    depends_on("r-rlang@1.0.2:", type=("build", "run"), when="@0.4.2:")
    depends_on("r-rlang@1.0.6:", type=("build", "run"), when="@0.5.0:")
    depends_on("r-rlang@1.1.0:", type=("build", "run"), when="@0.6.2:")

    depends_on("r-digest", type=("build", "run"), when="@:0.3.6")
    depends_on("r-zeallot", type=("build", "run"), when="@:0.2.0")
    depends_on("r-ellipsis@0.2.0:", type=("build", "run"), when="@:0.3.8")
