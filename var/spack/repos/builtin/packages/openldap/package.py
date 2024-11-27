# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openldap(AutotoolsPackage):
    """
    OpenLDAP Software is an open source implementation of the Lightweight
    Directory Access Protocol. The suite includes:

    slapd - stand-alone LDAP daemon (server)
    libraries implementing the LDAP protocol, and
    utilities, tools, and sample clients.
    """

    homepage = "https://www.openldap.org/"
    url = "https://www.openldap.org/software/download/OpenLDAP/openldap-release/openldap-2.6.0.tgz"

    license("OLDAP-2.8")

    version("2.6.8", sha256="48969323e94e3be3b03c6a132942dcba7ef8d545f2ad35401709019f696c3c4e")
    version("2.6.4", sha256="d51704e50178430c06cf3d8aa174da66badf559747a47d920bb54b2d4aa40991")
    version("2.6.0", sha256="b71c580eac573e9aba15d95f33dd4dd08f2ed4f0d7fc09e08ad4be7ed1e41a4f")
    version("2.4.49", sha256="e3b117944b4180f23befe87d0dcf47f29de775befbc469dcf4ac3dab3311e56e")
    version("2.4.48", sha256="d9523ffcab5cd14b709fcf3cb4d04e8bc76bb8970113255f372bc74954c6074d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("client_only", default=True, description="Client only installation")
    variant("icu", default=False, description="Build with unicode support")
    # Below, tls=none is not an option from programming point of view
    # If +client_only, configure arguments for tls won't be enabled
    variant(
        "tls",
        default="gnutls",
        description="Build with TLS support",
        values=("gnutls", "openssl"),
        multi=False,
    )

    variant("perl", default=False, description="Perl backend to Slapd")
    variant("sasl", default=True, description="Build with Cyrus SASL support")
    variant("static", default=False, description="Build static libraries")
    variant("shared", default=True, description="Build shared libraries")
    variant("dynamic", default=True, description="Enable linking built binaries with dynamic libs")
    variant("wt", default=False, description="Enable WiredTiger backend", when="@2.5.0:")
    conflicts("~static", when="~shared")

    depends_on("icu4c", when="+icu")
    depends_on("gnutls", when="~client_only tls=gnutls")
    depends_on("openssl", when="~client_only tls=openssl")
    depends_on("openssl@1.1.1:", when="~client_only tls=openssl @2.6.0:")
    depends_on("unixodbc", when="~client_only")
    depends_on("postgresql", when="~client_only")
    depends_on("berkeley-db", when="~client_only")  # for slapd
    # Recommended dependencies by Linux From Scratch
    depends_on("cyrus-sasl", when="+sasl")
    # depends_on('openslp', when='~client_only') # not avail. in spack yet
    # depends_on('Pth', when='~client_only') # not avail. in spack yet
    depends_on("perl", when="~client_only+perl")  # for slapd
    depends_on("groff", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("wiredtiger", when="@2.6.0:")
    depends_on("findutils", type="build")
    # see https://github.com/openldap/openldap/blob/OPENLDAP_REL_ENG_2_4_48/libraries/liblunicode/Makefile.in

    # Newer C compilers (>= Clang 16 and >= GCC 14) reject some constructs removed in C99
    conflicts("%gcc@14:", when="@:2.6.4", msg="Newer C compilers required 2.6.5 or newer")

    # Ref: https://www.linuxfromscratch.org/blfs/view/svn/server/openldap.html
    @when("+client_only")
    def configure_args(self):
        args = ["CPPFLAGS=-D_GNU_SOURCE", "--disable-debug", "--disable-slapd"]
        args += self.with_or_without("cyrus-sasl", variant="sasl")
        args += self.enable_or_disable("static")
        args += self.enable_or_disable("shared")
        args += self.enable_or_disable("dynamic")
        return args

    @when("~client_only")
    def configure_args(self):
        # Ref: https://www.openldap.org/lists/openldap-technical/201009/msg00304.html
        args = [
            "CPPFLAGS=-D_GNU_SOURCE",  # fixes a build error, see Ref above
            "--disable-debug",
            "--enable-crypt",
            "--enable-spasswd",
            "--enable-slapd",
            "--enable-modules",
            "--enable-rlookups",
            "--enable-backends=mod",
            "--disable-sql",
            "--enable-overlays=mod",
        ]

        if self.spec.satisfies("@:2.5"):
            args.extend(("--disable-ndb", "--disable-shell", "--disable-bdb", "--disable-hdb"))

        args += self.enable_or_disable("static")
        args += self.enable_or_disable("shared")
        args += self.enable_or_disable("dynamic")
        args += self.with_or_without("cyrus-sasl", variant="sasl")
        args.append("--with-tls=" + self.spec.variants["tls"].value)
        if self.spec.satisfies("@2.6.0: tls=gnutls"):
            args += ["--disable-autoca"]

        if self.spec.satisfies("@2.5.0:"):
            args += self.enable_or_disable("wt")

        args += self.enable_or_disable("perl")

        return args

    def build(self, spec, prefix):
        make("depend")
        make()
