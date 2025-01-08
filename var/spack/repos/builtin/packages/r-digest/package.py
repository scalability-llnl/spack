# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDigest(RPackage):
    """Create Compact Hash Digests of R Objects.

    Implementation of a function 'digest()' for the creation of hash digests of
    arbitrary R objects (using the md5, sha-1, sha-256, crc32, xxhash and
    murmurhash algorithms) permitting easy comparison of R language objects, as
    well as a function 'hmac()' to create hash-based message authentication
    code. The md5 algorithm by Ron Rivest is specified in RFC 1321, the sha-1
    and sha-256 algorithms are specified in FIPS-180-1 and FIPS-180-2, and the
    crc32 algorithm is described in
    ftp://ftp.rocksoft.com/cliens/rocksoft/papers/crc_v3.txt. For md5, sha-1,
    sha-256 and aes, this package uses small standalone implementations that
    were provided by Christophe Devine. For crc32, code from the zlib library
    is used. For sha-512, an implementation by Aaron D. Gifford is used. For
    xxhash, the implementation by Yann Collet is used. For murmurhash, an
    implementation by Shane Day is used. Please note that this package is not
    meant to be deployed for cryptographic purposes for which more
    comprehensive (and widely tested) libraries such as OpenSSL should be
    used."""

    cran = "digest"

    license("GPL-2.0-or-later")

    version("0.6.37", sha256="82c4d149994b8a4a9af930f5a8e47420829935abed41f3f9030e94b6a48f0321")
    version("0.6.31", sha256="5a284f490eaca6750f695f00a584cfca3f180ca1046ac1107202141149d431b9")
    version("0.6.30", sha256="7b8059943be7dba6053268dfcc229de1bb0b55db497b2943541a6abace076aa7")
    version("0.6.29", sha256="792c1f14a4c8047745152f5e45ce7351978af8d770c29d2ea39c7acd5d619cd9")
    version("0.6.28", sha256="4a328c75e95f8522fc07390d1dd00c19fb643f558e761a8aed04f99c1dc7db00")
    version("0.6.27", sha256="f485f75122907da24c41d4a62c91a232f0c371befd2f77e973342a1bef00253f")
    version("0.6.25", sha256="15ccadb7b8bccaa221b6700bb549011719d0f4b38dbd3a1f29face3e019e2de5")
    version("0.6.20", sha256="05674b0b5d888461ff770176c67b10a11be062b0fee5dbd9298f25a9a49830c7")
    version("0.6.19", sha256="28d159bd589ecbd01b8da0826eaed417f5c1bf5a11b79e76bf67ce8d935cccf4")
    version("0.6.12", sha256="a479463f120037ad8e88bb1387170842e635a1f07ce7e3575316efd6e14d9eab")
    version("0.6.11", sha256="edab2ca2a38bd7ee19482c9d2531cd169d5123cde4aa2a3dd65c0bcf3d1d5209")
    version("0.6.9", sha256="95fdc36011869fcfe21b40c3b822b931bc01f8a531e2c9260582ba79560dbe47")

    depends_on("r@2.4.1:", type=("build", "run"))
    depends_on("r@3.1.0:", type=("build", "run"), when="@0.6.16:")
    depends_on("r@3.3.0:", type=("build", "run"), when="@0.6.27:")
