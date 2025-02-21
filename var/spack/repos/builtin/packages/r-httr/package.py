# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RHttr(RPackage):
    """Tools for Working with URLs and HTTP.

    Useful tools for working with HTTP organised by HTTP verbs (GET(), POST(),
    etc). Configuration functions make it easy to control additional request
    components (authenticate(), add_headers() and so on)."""

    cran = "httr"

    license("MIT")

    version("1.4.7", sha256="1555e6c2fb67bd38ff11b479f74aa287b2d93f4add487aec53b836ff07de3a3a")
    version("1.4.5", sha256="f93bac7f882b0df099abca47dd5aae3686fb3cd2d3e9926fcd639bcddff76f6c")
    version("1.4.4", sha256="41d82523f3ee260d409a7b5ae4136190cbc5aecbc270b40ed7064f83e7f5435d")
    version("1.4.3", sha256="9a8613fa96173ac910c021391af1ced4d0609169049c802cf7cdfe1c40897c6a")
    version("1.4.2", sha256="462bed6ed0d92f811d5df4d294336025f1dbff357286999d9269bfd9c20b1ef9")
    version("1.4.1", sha256="675c7e07bbe82c48284ee1ab929bb14a6e653abae2860d854dc41a3c028de156")
    version("1.4.0", sha256="d633f1425da514f65f3b8c034ae0a8b6911995009840c6bb9657ceedb99ddb48")
    version("1.3.1", sha256="22134d7426b2eba37f0cc34b99285499b8bac9fe75a7bc3222fbad179bf8f258")
    version("1.2.1", sha256="e7b90b90ee52c826e152efcfadf98e078fa75b65a6baaeb8fd25eeed2195730e")
    version("1.1.0", sha256="d7c0cdc11b2ded3132544580f52ebe5dad2a426cde1a5029f2cc693b2f195823")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.1:", type=("build", "run"), when="@1.4.0:")
    depends_on("r@3.2:", type=("build", "run"), when="@1.4.1:")
    depends_on("r@3.5:", type=("build", "run"), when="@1.4.5:")
    depends_on("r-curl@3.0.0:", type=("build", "run"))
    depends_on("r-curl@5.0.2:", type=("build", "run"), when="@1.4.7:")
    depends_on("r-jsonlite", type=("build", "run"))
    depends_on("r-mime", type=("build", "run"))
    depends_on("r-openssl@0.8:", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))
