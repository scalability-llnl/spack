# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RFansi(RPackage):
    """ANSI Control Sequence Aware String Functions.

    Counterparts to R string manipulation functions that account for the
    effects of ANSI text formatting control sequences."""

    cran = "fansi"

    license("GPL-2.0-only OR GPL-3.0-only")

    version("1.0.6", sha256="ea9dc690dfe50a7fad7c5eb863c157d70385512173574c56f4253b6dfe431863")
    version("1.0.4", sha256="3163214e6c40922bbb495229259ed8ce1bebd98b77098a6936d234e43da9c49f")
    version("1.0.3", sha256="86a7b83d8c9d28baebbde310cd0b459d0950a9c7ff1a6276ce5858f6a89bc06a")
    version("1.0.2", sha256="d1e2cf2e10613abe19071e3dab7c564ebcf85ad13cbee25fa1999267af01b557")
    version("0.5.0", sha256="9d1bf8c316969c163abd3dd41cc1425b2671df9471fe806bf8783794a19ca54f")
    version("0.4.1", sha256="3c69eec803a3827e5227f9cf084976eeb738b22c7eb7665bb5faa251bce41e09")
    version("0.4.0", sha256="e104e9d01c7ff8a847f6b332ef544c0ef912859f9c6a514fe2e6f3b34fcfc209")
    version("0.3.0", sha256="dd6401d5c91ff4c45d752cceddd5379d1ae39a8a1196f236b0bc0ec6d691b88c")
    version("0.2.3", sha256="db6dfef8bfe6682d58b654b6a6a1d59cb07225ca41755176b465ab8611fd96c9")
    version("0.2.2", sha256="71dfdda467985a4d630ecf93d4bc60446a8a78d69dbd7ac24cc45822329d4bce")
    version("0.2.1", sha256="abe709d69ddd6610aaa24e049c7a97c16a2c2dbe0873d4e3b8af57e486ef05c5")

    depends_on("r@3.1.0:", type=("build", "run"))
