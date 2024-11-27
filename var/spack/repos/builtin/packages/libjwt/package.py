# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libjwt(AutotoolsPackage):
    """libjwt JSON Web Token C Library"""

    homepage = "https://github.com/benmcollins/libjwt"
    git = "https://github.com/benmcollins/libjwt"
    url = "https://github.com/benmcollins/libjwt/archive/v1.12.0.tar.gz"

    maintainers("bollig")

    license("MPL-2.0")

    version("1.15.3", sha256="cb2fd95123689e7d209a3a8c060e02f68341c9a5ded524c0cd881a8cd20d711f")
    version("1.15.2", sha256="a366531ad7d5d559b1f8c982e7bc7cece7eaefacf7e91ec36d720609c01dc410")
    version("1.13.1", sha256="4df55ac89c6692adaf3badb43daf3241fd876612c9ab627e250dfc4bb59993d9")
    version("1.12.1", sha256="d29e4250d437340b076350e910e69fd5539ef8b92528d0306745cec0e343cc17")
    version("1.12.0", sha256="eaf5d8b31d867c02dde767efa2cf494840885a415a3c9a62680bf870a4511bee")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")
    # Needs openssl at runtime to ensure we can generate keys
    depends_on("openssl", type=("build", "run"))
    depends_on("jansson")

    def configure_args(self):
        return ["--without-examples"]
