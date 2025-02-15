# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGmp(RPackage):
    """Multiple Precision Arithmetic.

    Multiple Precision Arithmetic (big integers and rationals, prime number
    tests, matrix computation), "arithmetic without limitations" using the C
    library GMP (GNU Multiple Precision Arithmetic)."""

    cran = "gmp"

    license("GPL-2.0-or-later")

    version("0.7-4", sha256="a7d6b40f77d2619c11db5170b8f47336f7c5fa1db7eed0ac9d8a432e41053919")
    version("0.7-1", sha256="a6873dc65218905cb7615cb8e2522258f3740e29c0632473d58a1cb409835db6")
    version("0.6-7", sha256="6333fe691f267aa29f8078f7f738dda50c496f660357276fd33e28d607363f85")
    version("0.6-6", sha256="87fa95a8084855d2137b3863b6b8f3c277280dbe3a6a230e359cf32c3bed2793")
    version("0.6-5", sha256="8ae76f3d17542eab3e7468341dabeebe28b11da8c1b4b3f7bbdb00d379689e52")
    version("0.6-2.1", sha256="c458026346c12093a22e627e2d5707a929fe95f4de3281894db4ab988d8747d6")
    version("0.6-2", sha256="6bfcb45b3f1e7da27d8773f911027355cab371d150c3dabf7dbaf8fba85b7f0e")
    version("0.5-13.5", sha256="f681ab2ff3d1e379ba8ac44a8abddd08d08170723e885abc0b469b6fa8fe5510")
    version("0.5-13.4", sha256="f05605b40fc39fc589e3a4d2f526a591a649faa45eef7f95c096e1bff8775196")
    version("0.5-13.1", sha256="2f805374a26742cd43f6b2054130d8670eda1940070aabb9971e9e48226d0976")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@0.6-2:")
    depends_on("gmp@4.2.3:")
