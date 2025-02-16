# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSets(RPackage):
    """Sets, Generalized Sets, Customizable Sets and Intervals

    Data structures and basic operations for ordinary sets, generalizations such
    as fuzzy sets, multisets, and fuzzy multisets, customizable sets, and
    intervals."""

    cran = "sets"

    maintainers("jgaeb")

    license("GPL-2.0-only")

    version("1.0-25", sha256="5ca469218f9679f2372e33e56f781b52947ccbedf730b91a2d3a572993c024f4")
    version("1.0-24", sha256="e75733f5c9418eb09fb950a4a94ccf84ddd88231c61ee80d02b7f0917debcac9")
    version("1.0-23", sha256="e5b6bc52060421c572d7f2d99b25909a38eacabd5344a47e1cdb2662c62d690b")
    version("1.0-22", sha256="6fbf9aa6b0113a58e04f803ab35593feabb0fb55d486d54afb59e027008f9ec6")
    version("1.0-21", sha256="5733f0be59189c058c069583f5c4dc1d772bfad5abbfd16081131414d6002ac0")
    version("1.0-20", sha256="234b724d40afcabc57eaf42dd34c6cb846e26803796e7fc80c00d26047c475d6")
    version("1.0-19", sha256="ae93e56bb0b4fd361349faf962772bb5eab965966e9c9bbf8bd4a2426a2e28a0")
    version("1.0-18", sha256="74d1e057e5b84197edb120665831d7b0565e2945e903be56c6701e724131679b")
    version("1.0-17", sha256="17817a386d725a458d95368795e4c31ef5dbc00439df24daf9bda996bfe767c5")
    version("1.0-16", sha256="5d36bc40937283112287d543f86a8fd470ce587420f5690f6a82f9ffa8e5805e")
    version("1.0-15", sha256="6f65ebfda2a94707b98cecdb1d3dcd0c0d1fd2f6a5c36eb128de7c2d5f7c1f8b")
    version("1.0-14", sha256="8fe81fc8d296484ffe9d796820dc259c0e6ab69d65d1f18564f89f3b9827cff1")
    version("1.0-13", sha256="5ffdc1a0e59c2a9e314b652ad72e0af5d138bad3e69190c6b56eca277c3c41fb")
    version("1.0-12", sha256="b1d1868bfba7c22e4bd726d534b1afbe593bde1f8e209ddb76613d1dd9c9954a")
    version("1.0-11", sha256="133d36b6fc3cb75097a829edbc15542f4817e2b6edf2a4d4830004a74308449f")
    version("1.0-10", sha256="5a631056ceb192ca35ecfc1cf10a0cf5a1671a3d5e50f942b0ac2e2098c909d0")
    version("1.0-9", sha256="748b254fedfe710bd295eb99168799c711f6a563b986b4f98e32f6ecc0c6de54")
    version("1.0-8", sha256="fa93e8e44b12cba33e9e1ca71e0d5ea84f3beb5656de9031c78e87ebfc2ee799")
    version("1.0-7", sha256="29f717a4b71fb2e72f3ce04f4cd703cc860c28c0f58a0e3b2adc1bcaa3b742ba")
    version("1.0", sha256="02b85933d9cd55e281c3a87889d827021394b51ba714e87359a36cbf60b50980")
    version("0.7", sha256="f450feaa2df5071c2029367edac867d7dbe435d202e5b1475e48827bc10bdf06")
    version("0.6", sha256="d682e5fe37d7fb2ded11ca702f9af2bf744cc56b3d5b310dba20dda2df6b1dc6")
    version("0.5", sha256="b4d8298e6f169d70b969ef6a49ed0583e2efecbdaa883c45142156bc97263149")
    version("0.4", sha256="f013228cbc3e63eb0a5b6ad8e217099482f275316f78f9bad380da6faa0defc6")
    version("0.3-2", sha256="c971cf712de2503f6605b883e36e1e1639ab8534d7c78ebc5a6a347e09771d37")
    version("0.3-1", sha256="0e6d4cd4eaf29edafbe4dbf4b71bfa3ada0f4ffb4a3becb144c023ef4478c944")
    version("0.3", sha256="a10c390d0571ab50a3c6e128d9157a9afc7c87b7befdc61cf86fa4cc9ef9c36d")
    version("0.2-1", sha256="f59ea29e7d87ba195909ab11102d14bb9b89c8fd76b25d273e79cd9227753aa2")
    version("0.2", sha256="987ff3ec1597a3d25d39ac62853443e43e77d3fdc450bed43f5ed72a30b142cb")
    version("0.1-3", sha256="e91d5b70ddd74ab50c944722b5dab2032cccd5cbfa740dd2b5a744ff0a89ce90")
    version("0.1-2", sha256="87fa3292eca69d358ea615c39240bb2151afc3a64f004b975f1918602ff9c694")
    version("0.1-1", sha256="4e41480757e33897a26974e5234801ff1c15f1a3952c96071787b43141a130de")
    version("0.1", sha256="18dda6c9d526a2f41f2b49a472fb27a7f1bb9ce6ea137b8963e8ad6c378825d0")

    depends_on("r@2.6:", type=("build", "run"), when="@0.1:")
    depends_on("r@2.7.0:", type=("build", "run"), when="@0.1-2:")
