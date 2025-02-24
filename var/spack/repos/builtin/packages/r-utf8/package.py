# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RUtf8(RPackage):
    """Unicode Text Processing.

    Process and print 'UTF-8' encoded international text (Unicode). Input,
    validate, normalize, encode, format, and display."""

    cran = "utf8"

    license("Apache-2.0 OR custom")

    version("1.2.4", sha256="418f824bbd9cd868d2d8a0d4345545c62151d321224cdffca8b1ffd98a167b7d")
    version("1.2.3", sha256="c0a88686591f4ad43b52917d0964e9df4c62d8858fe25135a1bf357dfcbd6347")
    version("1.2.2", sha256="a71aee87d43a9bcf29249c7a5a2e9ca1d2a836e8d5ee3a264d3062f25378d8f4")
    version("1.1.4", sha256="f6da9cadfc683057d45f54b43312a359cf96ec2731c0dda18a8eae31d1e31e54")
    version("1.1.3", sha256="43b394c3274ba0f66719d28dc4a7babeb87187e766de8d8ca716e0548091440f")
    version("1.1.2", sha256="148517aadb75d82aba61f63afe2a30d254abebbdc7e32dd0830e12ff443915b9")
    version("1.1.1", sha256="0e30c824e43cdc0a3339f4688e3271737d02ea10768a46137e0e41936051cb3d")
    version("1.1.0", sha256="6a8ae2c452859800c3ef12993a55892588fc35df8fa1360f3d182ed97244dc4f")
    version("1.0.0", sha256="7562a80262cbc2017eee76c0d3c9575f240fab291f868a11724fa04a116efb80")

    depends_on("r@2.10:", type=("build", "run"))
