# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.build_systems.autotools
import spack.build_systems.cmake
from spack.package import *


class Libssh2(AutotoolsPackage, CMakePackage):
    """libssh2 is a client-side C library implementing the SSH2 protocol"""

    homepage = "https://www.libssh2.org/"
    url = "https://www.libssh2.org/download/libssh2-1.7.0.tar.gz"

    license("BSD-3-Clause")

    version("1.11.1", sha256="d9ec76cbe34db98eec3539fe2c899d26b0c837cb3eb466a56b0f109cabf658f7")
    version("1.11.0", sha256="3736161e41e2693324deb38c26cfdc3efe6209d634ba4258db1cecff6a5ad461")
    version("1.10.0", sha256="2d64e90f3ded394b91d3a2e774ca203a4179f69aebee03003e5a6fa621e41d51")
    version("1.9.0", sha256="d5fb8bd563305fd1074dda90bd053fb2d29fc4bce048d182f96eaa466dfadafd")
    version("1.8.0", sha256="39f34e2f6835f4b992cafe8625073a88e5a28ba78f83e8099610a7b3af4676d4")
    version("1.7.0", sha256="e4561fd43a50539a8c2ceb37841691baf03ecb7daf043766da1b112e4280d584")
    version(
        "1.4.3", sha256="eac6f85f9df9db2e6386906a6227eb2cd7b3245739561cad7d6dc1d5d021b96d"
    )  # CentOS7

    depends_on("c", type="build")

    build_system("autotools", "cmake", default="autotools")

    variant(
        "crypto",
        default="openssl",
        description="The backend to use for cryptography",
        values=("openssl", conditional("mbedtls", when="@1.8:")),
    )
    variant("shared", default=True, description="Build shared libraries")

    with when("build_system=cmake"):
        depends_on("cmake@2.8.11:", type="build")
        # on macOS ensure CMP0042 is on (default in cmake 3.0+)
        depends_on("cmake@3:", type="build", when="platform=darwin")

    with when("crypto=openssl"):
        depends_on("openssl")
        depends_on("openssl@:1", when="@:1.9")

    depends_on("mbedtls@:2 +pic", when="crypto=mbedtls")
    depends_on("zlib-api")
    depends_on("xz")

    # libssh2 adds its own deps in the pc file even when doing shared linking,
    # and fails to prepend the -L flags, which is causing issues in libgit2, as
    # it tries to locate e.g. libssl in the dirs of the pc file's -L flags, and
    # cannot find the lib.
    patch("pr-1114.patch", when="@1.7:1.11.0")


class CMakeBuilder(spack.build_systems.cmake.CMakeBuilder):
    def cmake_args(self):
        args = [
            self.define("BUILD_TESTING", False),
            self.define("RUN_DOCKER_TESTS", False),
            self.define("BUILD_EXAMPLES", False),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
        ]

        crypto = self.spec.variants["crypto"].value

        if crypto == "openssl":
            args.append(self.define("CRYPTO_BACKEND", "OpenSSL"))
        elif crypto == "mbedtls":
            args.append(self.define("CRYPTO_BACKEND", "mbedTLS"))

        return args


class AutotoolsBuilder(spack.build_systems.autotools.AutotoolsBuilder):
    def configure_args(self):
        args = [
            "--disable-tests",
            "--disable-docker-tests",
            "--disable-examples-build",
            "--without-libgcrypt",
            "--without-wincng",
            *self.enable_or_disable("shared"),
        ]

        crypto = self.spec.variants["crypto"].value

        if self.spec.satisfies("@1.9:"):
            # single flag for all crypto backends
            args.append(f"--with-crypto={crypto}")
        else:
            # one flag per crypto backend
            if crypto == "openssl":
                args.append(f"--with-libssl-prefix={self.spec['openssl'].prefix}")
                args.append("--without-mbedtls")
            elif crypto == "mbedtls":
                args.append(f"--with-libmbedcrypto-prefix={self.spec['mbedtls'].prefix}")
                args.append("--without-openssl")

        return args
