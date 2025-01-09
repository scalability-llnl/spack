# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------
from spack.package import *


class AoclCrypto(CMakePackage):
    """
    AOCL-Crypto is a library consisting of basic cryptographic functions
    optimized and tuned for AMD Zen™ based microarchitecture.

    This library provides a unified solution for Cryptographic routines such
    as AES (Advanced Encryption Standard) encryption/decryption routines
    (CFB, CTR, CBC, CCM, GCM, OFB, SIV, XTS), SHA (Secure Hash Algorithms)
    routines (SHA2, SHA3, SHAKE), Message Authentication Code (CMAC, HMAC),
    ECDH (Elliptic-curve Diffie–Hellman) and RSA (Rivest, Shamir, and Adleman)
    key generation functions, etc. AOCL Crypto supports a dynamic dispatcher
    feature that executes the most optimal function variant implemented using
    Function Multi-versioning thereby offering a single optimized library
    portable across different x86 CPU architectures.

    AOCL Crypto framework is developed in C / C++ for Unix and Windows based
    systems.

    LICENSING INFORMATION: By downloading, installing and using this software,
    you agree to the terms and conditions of the AMD AOCL-Cryptography license
    agreement.  You may obtain a copy of this license agreement from
    https://www.amd.com/en/developer/aocl/cryptography/eula/cryptography-4-2-eula.html
    """

    _name = "aocl-crypto"
    homepage = "https://www.amd.com/en/developer/aocl/cryptography.html"
    url = "https://github.com/amd/aocl-crypto/archive/4.2.tar.gz"
    git = "https://github.com/amd/aocl-crypto/"

    maintainers("amd-toolchain-support")

    version(
        "5.0",
        sha256="b15e609943f9977e13f2d5839195bb7411c843839a09f0ad47f78f57e8821c23",
        preferred=True,
    )
    version("4.2", sha256="2bdbedd8ab1b28632cadff237f4abd776e809940ad3633ad90fc52ce225911fe")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    variant("examples", default=False, description="Build examples")
    variant("ipp", default=False, description="Build Intel IPP library")

    # Removed dependency on lsb_release
    patch(
        "lsb_release.patch",
        sha256="b61d6d2518276c56d37e8c64d18488081af70f29a62f315ecbd23664e0e440b9",
        when="@5.0",
    )

    depends_on("cmake@3.22:", type="build")
    depends_on("openssl@3.1.5:")
    depends_on("intel-oneapi-ippcp@2021.12.0:", when="+ipp")
    depends_on("p7zip", type="build")
    for vers in ["4.2", "5.0"]:
        with when(f"@={vers}"):
            depends_on(f"aocl-utils@={vers}")

    @property
    def build_directory(self):
        """Returns the directory to use when building the package

        :return: directory where to build the package
        """

        build_directory = self.stage.source_path

        if self.spec.variants["build_type"].value == "Debug":
            build_directory = join_path(build_directory, "build", "debug")
        else:
            build_directory = join_path(build_directory, "build", "release")

        return build_directory

    def cmake_args(self):
        """Runs ``cmake`` in the build directory"""
        spec = self.spec

        args = [
            self.define_from_variant("ALCP_ENABLE_EXAMPLES", "examples"),
            self.define("ENABLE_AOCL_UTILS", True),
            self.define("AOCL_UTILS_INSTALL_DIR", spec["aocl-utils"].prefix),
            self.define("CMAKE_INSTALL_LIBDIR", "lib"),
            self.define("ALCP_ENABLE_DYNAMIC_COMPILER_PICK", False),
        ]

        compat_libs = ["openssl"]
        args.append(self.define("OPENSSL_INSTALL_DIR", spec["openssl"].prefix))

        if "+ipp" in spec:
            compat_libs.append("ipp")
            args.append(self.define("IPP_INSTALL_DIR", spec["intel-oneapi-ippcp"].prefix))

        args.append(self.define("AOCL_COMPAT_LIBS", ",".join(compat_libs)))

        return args
