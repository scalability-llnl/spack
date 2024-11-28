# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gnutls(AutotoolsPackage):
    """GnuTLS is a secure communications library implementing the SSL, TLS
    and DTLS protocols and technologies around them. It provides a simple C
    language application programming interface (API) to access the secure
    communications protocols as well as APIs to parse and write X.509, PKCS
    #12, OpenPGP and other required structures. It is aimed to be portable
    and efficient with focus on security and interoperability."""

    homepage = "https://www.gnutls.org"
    url = "https://www.gnupg.org/ftp/gcrypt/gnutls/v3.5/gnutls-3.5.19.tar.xz"

    maintainers("alecbcs")

    license("LGPL-2.1-or-later")

    version("3.8.3", sha256="f74fc5954b27d4ec6dfbb11dea987888b5b124289a3703afcada0ee520f4173e")
    version("3.7.8", sha256="c58ad39af0670efe6a8aee5e3a8b2331a1200418b64b7c51977fb396d4617114")
    version("3.6.15", sha256="0ea8c3283de8d8335d7ae338ef27c53a916f15f382753b174c18b45ffd481558")
    version("3.6.14", sha256="5630751adec7025b8ef955af4d141d00d252a985769f51b4059e5affa3d39d63")
    version("3.6.8", sha256="aa81944e5635de981171772857e72be231a7e0f559ae0292d2737de475383e83")
    version("3.6.7.1", sha256="881b26409ecd8ea4c514fd3fbdb6fae5fab422ca7b71116260e263940a4bbbad")
    version("3.5.19", sha256="1936eb64f03aaefd6eb16cef0567457777618573826b94d03376bb6a4afadc44")
    version("3.5.13", sha256="79f5480ad198dad5bc78e075f4a40c4a315a1b2072666919d2d05a08aec13096")
    version("3.5.10", sha256="af443e86ba538d4d3e37c4732c00101a492fe4b56a55f4112ff0ab39dbe6579d")
    version("3.5.9", sha256="82b10f0c4ef18f4e64ad8cef5dbaf14be732f5095a41cf366b4ecb4050382951")
    version("3.3.9", sha256="39166de5293a9d30ef1cd0a4d97f01fdeed7d7dbf8db95392e309256edcb13c1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("zlib", default=True, description="Enable zlib compression support")
    variant("guile", default=False, description="Enable Guile bindings")
    variant(
        "brotli", default=True, description="Enable brotli compression support", when="@3.7.4:"
    )

    # gnutls+guile is currently broken on MacOS.  See Issue #11668
    conflicts("+guile", when="platform=darwin")

    # -Wimplicit-int is an error in newer clang
    conflicts("%clang@16:", when="@:3.7")
    conflicts("%apple-clang@15:", when="@:3.7")

    # Note that version 3.3.9 of gnutls doesn't support nettle 3.0.
    depends_on("nettle@3.4.1:", when="@3.6.7.1:")
    depends_on("guile", when="+guile")
    depends_on("nettle@:2.9", when="@3.3.9")
    depends_on("nettle", when="@3.5:")
    depends_on("libidn2@:2.0", when="@:3.5")
    depends_on("libidn2")
    depends_on("zlib-api", when="+zlib")
    depends_on("brotli", when="+brotli")
    depends_on("gettext")

    depends_on("pkgconfig", type="build")

    build_directory = "spack-build"

    def url_for_version(self, version):
        url = "https://www.gnupg.org/ftp/gcrypt/gnutls/v{0}/gnutls-{1}.tar.xz"
        return url.format(version.up_to(2), version)

    def setup_build_environment(self, env):
        spec = self.spec
        if spec.satisfies("+guile"):
            env.set("GUILE", spec["guile"].prefix.bin.guile)

    def configure_args(self):
        spec = self.spec
        args = ["--enable-static"]

        if spec.satisfies("@3.5:"):
            # use shipped libraries, might be turned into variants
            args.append("--with-included-libtasn1")
            args.append("--with-included-unistring")
            args.append("--without-p11-kit")  # p11-kit@0.23.1: ...

        args += self.with_or_without("zlib")
        args += self.with_or_without("brotli")
        args += self.enable_or_disable("guile")

        if self.run_tests:
            args.extend(["--enable-tests", "--enable-valgrind-tests", "--enable-full-test-suite"])
        else:
            args.extend(
                ["--disable-tests", "--disable-valgrind-tests", "--disable-full-test-suite"]
            )

        return args

    @property
    def headers(self):
        headers = find_all_headers(self.prefix.include)
        headers.directories = [self.prefix.include]
        return headers
