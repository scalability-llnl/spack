# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDataTable(RPackage):
    """Extension of `data.frame`.

    Fast aggregation of large data (e.g. 100GB in RAM), fast ordered joins,
    fast add/modify/delete of columns by group using no copies at all, list
    columns and a fast file reader (fread). Offers a natural and flexible
    syntax, for faster development."""

    cran = "data.table"

    license("MPL-2.0-no-copyleft-exception")

    version("1.15.4", sha256="ab8065ff946d59ecaaf5eaf91a975495c07c30caad97a71205c72e41a740cb53")
    version("1.14.8", sha256="14b2ce5367df9c9bb58f373555066f5dcb629c156149b5565de36d69557139fd")
    version("1.14.4", sha256="4862a7c26e8309108fd1f5296616407b9ff9e4e1be5cdedcb717f114c2e348f0")
    version("1.14.2", sha256="f741b951e5937440139514aedbae78dbd6862d825066848bdb006aa02c2f3d2b")
    version("1.13.6", sha256="d50cdd4c4f89cabf83baa9114e49a3b8179f403c499d6e0be7791a44ffcd3e9b")
    version("1.12.8", sha256="d3a75f3a355ff144cc20a476041617e21fcf2a9f79265fd9bbd4693f3671f9dc")
    version("1.12.2", sha256="db55c18f0d703a8bc1c806dd1f7551bb405cb867717f52ef9dd64405394d22f5")
    version("1.12.0", sha256="611b112123dbd4ebd5200770fcdfaaeaab622adeb2b290d36018d3092742e3f7")
    version("1.11.8", sha256="dc427465599cadd848b28a78e2fce3362867847b44148252054385999fe566d9")
    version("1.11.6", sha256="ac6783c18e94d1bc05702ddec9fd87c542c744f640132f5ffc373348be84d9e9")
    version("1.11.4", sha256="fdccf1dec3f38bb344163163decf3ffa0c0f8e2c70daa1bec8aac422716e81d5")
    version("1.11.2", sha256="44f548517426c0444f7ce993bf93350be9f31e214d3dad39f9a680a53f9e6e64")
    version("1.11.0", sha256="ae81e07a39ef0cb65751c8987df21246d57ebc5e4ef7e9c511225a9d58193758")
    version("1.10.4-3", sha256="ba8b4f1b96b16e7f9765fc49c5028f21ef2210fc46cf962f4f7ea7901f9d8a89")
    version("1.10.4-2", sha256="27d703e0746b25cab0229285013e955f676ab9d8460d7f7c3c01df4c257b2d95")
    version("1.10.4-1", sha256="1ea6f9d45c94974f69b6918a248853ba24cbd80cdd1309b1be43eca65d6e7a75")
    version("1.10.4", sha256="865fdf6aad389071ad063ec1c75a78ffc86eeb88bba011f3ea5281d243966b7a")
    version("1.10.2", sha256="95a3ae6b273910571e25400a5cab1f7542cf589272c012c268f4b4724216f658")
    version("1.10.0", sha256="cf61732ef9b38ecb6579055d1cd145198ad23a5a9ae4378f94a1494e6c56c884")
    version("1.9.8", sha256="dadb21a14a7f4d60955cdd8fb9779136833498be97b1625914e9a6b580646f4d")
    version("1.9.6", sha256="6f74c349c1731823aef6899edcf18418454167d04eba983e3a6fe17ee9fd236e")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("zlib-api")
