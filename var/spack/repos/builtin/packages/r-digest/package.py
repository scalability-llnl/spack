# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RDigest(RPackage):
    """Implementation of a function 'digest()' for the creation of hash digests
    of arbitrary R objects (using the md5, sha-1, sha-256, crc32, xxhash and
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

    homepage = "http://dirk.eddelbuettel.com/code/digest.html"
    url      = "https://cloud.r-project.org/src/contrib/digest_0.6.12.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/digest"

    version('0.6.25', sha256='15ccadb7b8bccaa221b6700bb549011719d0f4b38dbd3a1f29face3e019e2de5')
    version('0.6.20', sha256='05674b0b5d888461ff770176c67b10a11be062b0fee5dbd9298f25a9a49830c7')
    version('0.6.19', sha256='28d159bd589ecbd01b8da0826eaed417f5c1bf5a11b79e76bf67ce8d935cccf4')
    version('0.6.12', sha256='a479463f120037ad8e88bb1387170842e635a1f07ce7e3575316efd6e14d9eab')
    version('0.6.11', sha256='edab2ca2a38bd7ee19482c9d2531cd169d5123cde4aa2a3dd65c0bcf3d1d5209')
    version('0.6.9',  sha256='95fdc36011869fcfe21b40c3b822b931bc01f8a531e2c9260582ba79560dbe47')

    depends_on('r@2.4.1:', when='@:0.6.15', type=('build', 'run'))
    depends_on('r@3.1.0:', when='@0.6.16:', type=('build', 'run'))
