# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cryptopp(MakefilePackage):
    """Crypto++ is an open-source C++ library of cryptographic schemes. The
    library supports a number of different cryptography algorithms, including
    authenticated encryption schemes (GCM, CCM), hash functions (SHA-1, SHA2),
    public-key encryption (RSA, DSA), and a few obsolete/historical encryption
    algorithms (MD5, Panama)."""

    homepage = "https://github.com/weidai11/cryptopp"
    urls = [
        "https://github.com/weidai11/cryptopp/releases/download/CRYPTOPP_8_9_0/cryptopp890.zip",
        "https://www.cryptopp.com/cryptopp700.zip",
    ]

    license("BSL-1.0")

    version("8.9.0", sha256="4cc0ccc324625b80b695fcd3dee63a66f1a460d3e51b71640cdbfc4cd1a3779c")
    version("8.7.0", sha256="d0d3a28fcb5a1f6ed66b3adf57ecfaed234a7e194e42be465c2ba70c744538dd")
    version("7.0.0", sha256="a4bc939910edd3d29fb819a6fc0dfdc293f686fa62326f61c56d72d0a366ceb0")
    version("6.1.0", sha256="21289d2511101a9350c87c8eb1f4982d4a266e8037b19dab79a32cc13ea108c7")
    version("6.0.0", sha256="64ac2db96b3f1b7a23675e2be95d16c96055edffa2d5e2de6245fdb6baa92dda")
    version("5.6.5", sha256="a75ef486fe3128008bbb201efee3dcdcffbe791120952910883b26337ec32c34")
    version("5.6.4", sha256="be430377b05c15971d5ccb6e44b4d95470f561024ed6d701fe3da3a188c84ad7")
    version("5.6.3", sha256="9390670a14170dd0f48a6b6b06f74269ef4b056d4718a1a329f6f6069dc957c9")
    version("5.6.2", sha256="5cbfd2fcb4a6b3aab35902e2e0f3b59d9171fee12b3fc2b363e1801dfec53574")
    version("5.6.1", sha256="98e74d8cb17a38033354519ac8ba9c5d98a6dc00bf5d1ec3c533c2e8ec86f268")

    variant("shared", default=True, description="Build shared object versions of libraries.")

    depends_on("gmake", type="build")

    def url_for_version(self, version):
        return f"https://github.com/weidai11/cryptopp/releases/download/CRYPTOPP_{version.underscored}/cryptopp{version.joined}.zip"

    def build(self, spec, prefix):
        cxx_flags = []

        if spec.satisfies("+shared"):
            cxx_flags.append(self.compiler.cxx_pic_flag)

        target = self.spec.target
        if "sse4.1" not in target:
            cxx_flags.append("-DCRYPTOPP_DISABLE_SSE4")
        if "ssse3" not in target:
            cxx_flags.append("-DCRYPTOPP_DISABLE_SSSE3")
        if "sse2" not in target:
            cxx_flags.append("-DCRYPTOPP_DISABLE_SSE2")

        make_target = "dynamic" if "+shared" in spec else "static"
        make(make_target, f"CXXFLAGS={' '.join(cxx_flags)}")

    def install(self, spec, prefix):
        make("install", f"PREFIX={prefix}")
