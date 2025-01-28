# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRlang(RPackage):
    """Functions for Base Types and Core R and 'Tidyverse' Features.

    A toolbox for working with base types, core R features like the condition
    system, and core 'Tidyverse' features like tidy evaluation."""

    cran = "rlang"

    license("MIT")

    version("1.1.4", sha256="f2d74527508bf3287102470beb27de0d234c3cbba399c28d3312f2c83c64a6e1")
    version("1.1.2", sha256="2a0ee1dc6e5c59b283c32db5e74e869922a336197cb406fe92622b6ec66f8092")
    version("1.1.1", sha256="5e5ec9a7796977216c39d94b1e342e08f0681746657067ba30de11b8fa8ada99")
    version("1.1.0", sha256="f89859d91c9edc05fd7ccf21163fe53ad58da907ee273a93d5ab004a8649335b")
    version("1.0.6", sha256="e6973d98a0ea301c0da1eeaa435e9e65d1c3f0b95ed68bdc2d6cb0c610166760")
    version("1.0.2", sha256="8de87c3e6fb0b3cce2dabc6908186f8e1528cc0c16b54de965fe02d405fdd7cc")
    version("1.0.1", sha256="e59fd5c0f7530dbe329aa01621f6ef5a6474ff3ec96de0c0d24018fc2f21ad7f")
    version("1.0.0", sha256="ab6134c97b3100613ba2a15792fde5341f485ba85432a81370c6270c73396e6a")
    version("0.4.12", sha256="2a26915738be120a56ec93e781bcb50ffa1031e11904544198b4a15c35029915")
    version("0.4.10", sha256="07530270c4c199f2b7efc5d57a476d99babd9d0c3388a02bb7d57fe312da3576")
    version("0.4.6", sha256="3a81b107765fd6ac0ad716c428d01878775ded9208ba125d43c890c73d2533ca")
    version("0.4.0", sha256="9748a4a217548bbe5631c18fd88c94811950446f798ff21fb327703aebaa150d")
    version("0.3.4", sha256="4e467f7b0dcbde91b60c292137d2c69cecaa713a6e4c9b7157ef6fd5453b7ade")
    version("0.3.1", sha256="30427b2be2288e88acd30c4ea348ee06043a649fd73623a63148b1ad96317151")
    version("0.3.0.1", sha256="29451db0a3cabd75761d32df47a5d43ccadbde07ecb693ffdd73f122a0b9f348")
    version("0.3.0", sha256="9ab10ea3e19b2d60a289602ebbefa83509f430db1c8161e523896c374241b893")
    version("0.2.2", sha256="c9119420ff0caeb6b0fcee8800e2fb1ec072e291e0e53b8acea3c4cf49420d33")
    version("0.1.4", sha256="8d9b6c962ae81b96c96ada9614c6a1ffb9eda12dd407e2aff634f7d335e7b9f4")
    version("0.1.2", sha256="90cfcd88cae6fff044fca64b24a8e6bdc09fc276163b518ff2d90268b0c785f9")
    version("0.1.1", sha256="5901f95d68728a7d9bb1c2373a20ce6e4ad222f66e397e7735e9eff987c73c3f")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r@3.2.0:", type=("build", "run"), when="@0.4.0:")
    depends_on("r@3.3.0:", type=("build", "run"), when="@0.4.10:")
    depends_on("r@3.4.0:", type=("build", "run"), when="@1.0.2:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@1.1.0:")
