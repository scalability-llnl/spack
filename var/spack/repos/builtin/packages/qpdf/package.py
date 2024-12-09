# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Qpdf(CMakePackage):
    """
    QPDF is a command-line tool and C++ library that performs
    content-preserving transformations on PDF files.
    """

    homepage = "https://qpdf.sourceforge.io/"
    url = "https://github.com/qpdf/qpdf/releases/download/v11.9.0/qpdf-11.9.0.tar.gz"

    maintainers("taliaferro")

    license("Apache-2.0", checked_by="taliaferro")

    version("11.9.1", sha256="2ba4d248f9567a27c146b9772ef5dc93bd9622317978455ffe91b259340d13d1")
    version("11.9.0", sha256="9f5d6335bb7292cc24a7194d281fc77be2bbf86873e8807b85aeccfbff66082f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "crypto",
        values=["openssl", "gnutls", "native", "implicit"],
        default="implicit",
        multi=False,
        description="Provider of cryptographic functions.",
    )

    depends_on("zlib-api")
    depends_on("jpeg")
    depends_on("openssl", when="crypto=openssl")
    depends_on("gnutls", when="crypto=gnutls")

    def cmake_args(self):
        args = []
        if not self.spec.satisfies("crypto=implicit"):
            crypto_type = self.spec.variants["crypto"].value.upper()
            args.append("USE_IMPLICIT_CRYPTO=0")
            args.append(f"REQUIRE_CRYPTO_{crypto_type}=1")

        return args
