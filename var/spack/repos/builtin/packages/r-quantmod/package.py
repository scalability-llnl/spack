# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RQuantmod(RPackage):
    """Quantitative Financial Modelling Framework.

    Specify, build, trade, and analyse quantitative financial trading
    strategies."""

    cran = "quantmod"

    license("GPL-3.0-only")

    version("0.4.26", sha256="396c5d3241f77911d9f7738a60a9d728ed25b3dbce2fd92f5b11f9fcbcb8bb98")
    version("0.4.22", sha256="f29496f1ca9a9faf91aba70ac50bfe79303197ca8f1e369c96300005b5e6765e")
    version("0.4.20", sha256="f757df41595d885f7927e18f4835bc233d78d2d3ae48fd11c8874d4338c48e94")
    version("0.4.18", sha256="aa40448e93a1facf399213ac691784007731e869ad243fe762381ab099cd6c35")
    version("0.4-15", sha256="7ef2e798d4d8e4d2af0a5b2b9fecebec30568087afbd24bfd923cdeb8b53df53")
    version("0.4-14", sha256="d95b1acf73328d675bbad18a93fa3c40faf58959e0401458ad21cf6b9f9254b3")
    version("0.4-10", sha256="030040aa567adaba1ea4a1f05eb45712dbdaabbabca72733e7fb2984051f688b")
    version("0.4-5", sha256="c7889eb55a21296e7bda1242c46e734a0a8bd6dcbf5726aafae5313354eec893")

    depends_on("r@3.2.0:", type=("build", "run"), when="@0.4-11:")
    depends_on("r-xts@0.9-0:", type=("build", "run"))
    depends_on("r-zoo", type=("build", "run"))
    depends_on("r-ttr@0.2:", type=("build", "run"))
    depends_on("r-curl", type=("build", "run"))
    depends_on("r-jsonlite@1.1:", type=("build", "run"), when="@0.4.22:")
