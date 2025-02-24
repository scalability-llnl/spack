# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ROpenssl(RPackage):
    """Toolkit for Encryption, Signatures and Certificates Based on OpenSSL.

    Bindings to OpenSSL libssl and libcrypto, plus custom SSH pubkey parsers.
    Supports RSA, DSA and EC curves P-256, P-384 and P-521.  Cryptographic
    signatures can either be created and verified manually or via x509
    certificates. AES can be used in cbc, ctr or gcm mode for symmetric
    encryption; RSA for asymmetric (public key) encryption or EC for Diffie
    Hellman. High-level envelope functions combine RSA and AES for encrypting
    arbitrary sized data. Other utilities include key generators, hash
    functions (md5, sha1, sha256, etc), base64 encoder, a secure random number
    generator, and 'bignum' math methods for manually performing crypto
    calculations on large multibyte integers."""

    cran = "openssl"

    license("MIT")

    version("2.2.1", sha256="25a12328d584212d8d4c095b3d2a71152c5d2bc4adda7a9addb25da01136f78d")
    version("2.0.6", sha256="77f3032a16270f0d1734f269b8d348eedc75b277812854386091143082c1b3f3")
    version("2.0.4", sha256="a1a5c65127c20c0ca3b46f2c4f4d3817276a887a231569537c1373e7740a5cec")
    version("2.0.3", sha256="7cde98520bec857f043fb6aae92334e2ae0dcd86108adc9b18ca298ec16286aa")
    version("2.0.2", sha256="862d3dc9bb69d92e36e83a7506be83443d4a4957f5f08f6617d7873c67a1f1c4")
    version("1.4.6", sha256="43b832af70e71770168b997107c52c8f406f8c33e9ef9b289610bccea2f34359")
    version("1.4.5", sha256="4fc141aba8e94e9f5ecce6eda07e45a5e7048d8609ba909ede4f7f4933e0c1f7")
    version("1.4.3", sha256="342001df8ecff5df2cdf757f123d35ea4b449751045f708b91f27c1be0d48269")
    version("1.4.1", sha256="f7fbecc75254fc43297a95a4338c674ab9ba2ec056b59e027d16d23122161fc6")
    version("1.3", sha256="1c83f4d529adc1f5ec40e477c690a8d5b0a42422f3e542f1fc39062dcfaca4bf")
    version("0.9.7", sha256="697d9e86f99270163744538dc3dc4d19d00af89a8570a1d304b110e1d2650e9d")
    version("0.9.6", sha256="6dd6d1cade4004962d516ad761fff0812beec0232318b385d286761423a5dc39")
    version("0.9.4", sha256="cb7349defa5428acc0907629a4f53f82d2519af219e5d6a41f852cf55b1feb66")

    depends_on("r-askpass", type=("build", "run"), when="@1.2:")
    depends_on("openssl@1.0.1:")
    depends_on("openssl@1.0.2:", when="@2.0.2:")

    def flag_handler(self, name, flags):
        if name == "cflags":
            flags.append(self.compiler.c99_flag)
        return (flags, None, None)
