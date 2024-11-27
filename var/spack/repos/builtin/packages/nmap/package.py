# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nmap(AutotoolsPackage):
    """Nmap ("Network Mapper") is a free and open source (license)
    utility for network discovery and security auditing.
    It also provides ncat an updated nc"""

    homepage = "https://nmap.org"
    url = "https://nmap.org/dist/nmap-7.70.tar.bz2"
    list_url = "https://nmap.org/dist-old/"

    license("custom")

    version("7.93", sha256="55bcfe4793e25acc96ba4274d8c4228db550b8e8efd72004b38ec55a2dd16651")
    version("7.92", sha256="a5479f2f8a6b0b2516767d2f7189c386c1dc858d997167d7ec5cfc798c7571a1")
    version("7.91", sha256="18cc4b5070511c51eb243cdd2b0b30ff9b2c4dc4544c6312f75ce3a67a593300")
    version("7.90", sha256="5557c3458275e8c43e1d0cfa5dad4e71dd39e091e2029a293891ad54098a40e8")
    version("7.80", sha256="fcfa5a0e42099e12e4bf7a68ebe6fde05553383a682e816a7ec9256ab4773faa")
    version("7.70", sha256="847b068955f792f4cc247593aca6dc3dc4aae12976169873247488de147a6e18")
    version("7.60", sha256="a8796ecc4fa6c38aad6139d9515dc8113023a82e9d787e5a5fb5fa1b05516f21")
    version("7.50", sha256="e9a96a8e02bfc9e80c617932acc61112c23089521ee7d6b1502ecf8e3b1674b2")
    version("7.40", sha256="9e14665fffd054554d129d62c13ad95a7b5c7a046daa2290501909e65f4d3188")
    version("7.31", sha256="cb9f4e03c0771c709cd47dc8fc6ac3421eadbdd313f0aae52276829290583842")
    version("7.30", sha256="ba38a042ec67e315d903d28a4976b74999da94c646667c0c63f31e587d6d8d0f")
    version("7.12", sha256="63df082a87c95a189865d37304357405160fc6333addcf5b84204c95e0539b04")
    version("7.01", sha256="cf1fcd2643ba2ef52f47acb3c18e52fa12a4ae4b722804da0e54560704627705")
    version("6.40", sha256="491f77d8b3fb3bb38ba4e3850011fe6fb43bbe197f9382b88cb59fa4e8f7a401")
    version("6.01", sha256="77f6635b677d28b546cbef97e4ead6c2d4a5aebcaa108fe3a3c135db6448617a")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("liblua", default=True, description="Enable lua (required by all of NSE)")
    variant("ncat", default=True, description="Enable ncat")
    variant("nping", default=True, description="Enable nping")
    variant("nmap-update", default=False, description="Enable nmap-update")

    # Release notes for 7.3: "Ensure Nmap builds with OpenSSL 3.0 using no
    # deprecated API functions."
    depends_on("openssl@3.0.7:", when="@7.93:")

    # previous verisons use a few deprecated openssl apis
    depends_on("openssl@1.1:", when="@7.50:7.92")
    depends_on("openssl@:1.0.9", when="@:7.49")

    # nmap vendors a few libraries, but we should build against spack's
    # versions where appropriate. See their build guide at
    # https://nmap.org/book/inst-source.html#inst-configure. Also see:
    # https://github.com/nmap/nmap/issues/1602
    #
    # Any that are included "for convenience" we should provide.
    #
    # The recursive builds for vendored dependencies is also broken on
    # darwin (something races); using our own deps works around that issue.
    #
    # Specifically, something is touching libpcre/configure during the build,
    # which causes the recursive `make`'s configure.status --recheck pass to
    # attempt to rerun configure. Rerunning configure fails and asks you to run
    # `make distclean`.

    depends_on("libssh2@1.10")
    depends_on("pcre@8")
    depends_on("zlib-api")

    def configure_args(self):
        args = []

        # https://github.com/nmap/nmap/issues/2144
        args.append("--disable-rdma")

        # ndiff and zenmap both require python2, which is deprecated in spack.
        # The next nmap release will fix this, so, disable these features
        # completely for now. We will add flags for these features again
        # when they can be supported without a dependency on python2
        args.append("--disable-ndiff")
        args.append("--disable-zenmap")

        args += self.with_or_without("liblua")
        args += self.with_or_without("ncat")
        args += self.with_or_without("nping")
        args += self.with_or_without("nmap-update")

        return args
