# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import re
import sys

from llnl.util.filesystem import windows_sfn

from spack.build_systems.autotools import AutotoolsBuilder
from spack.build_systems.nmake import NMakeBuilder
from spack.package import *

is_windows = sys.platform == "win32"


class Curl(NMakePackage, AutotoolsPackage):
    """cURL is an open source command line tool and library for
    transferring data with URL syntax"""

    homepage = "https://curl.se/"
    url = "https://curl.haxx.se/download/curl-7.78.0.tar.bz2"

    executables = ["^curl$"]
    tags = ["build-tools", "windows"]

    maintainers("alecbcs")

    license("curl")

    version("8.10.1", sha256="3763cd97aae41dcf41950d23e87ae23b2edb2ce3a5b0cf678af058c391b6ae31")

    # Deprecated versions due to CVEs
    version(
        "8.8.0",
        sha256="40d3792d38cfa244d8f692974a567e9a5f3387c547579f1124e95ea2a1020d0d",
        deprecated=True,
    )
    version(
        "8.7.1",
        sha256="05bbd2b698e9cfbab477c33aa5e99b4975501835a41b7ca6ca71de03d8849e76",
        deprecated=True,
    )
    version(
        "8.6.0",
        sha256="b4785f2d8877fa92c0e45d7155cf8cc6750dbda961f4b1a45bcbec990cf2fa9b",
        deprecated=True,
    )
    version(
        "8.4.0",
        sha256="e5250581a9c032b1b6ed3cf2f9c114c811fc41881069e9892d115cc73f9e88c6",
        deprecated=True,
    )
    version(
        "8.1.2",
        sha256="b54974d32fd610acace92e3df1f643144015ac65847f0a041fdc17db6f43f243",
        deprecated=True,
    )
    version(
        "8.0.1",
        sha256="9b6b1e96b748d04b968786b6bdf407aa5c75ab53a3d37c1c8c81cdb736555ccf",
        deprecated=True,
    )
    # needed by r@:4.2
    version(
        "7.88.1",
        sha256="8224b45cce12abde039c12dc0711b7ea85b104b9ad534d6e4c5b4e188a61c907",
        deprecated=True,
    )
    # needed by old r-curl
    version(
        "7.63.0",
        sha256="9bab7ed4ecff77020a312d84cc5fb7eb02d58419d218f267477a724a17fd8dd8",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    default_tls = "openssl"
    if sys.platform == "darwin":
        default_tls = "secure_transport"
    elif sys.platform == "win32":
        default_tls = "sspi"

    # TODO: add dependencies for other possible TLS backends
    variant(
        "tls",
        default=default_tls,
        description="TLS backend",
        values=(
            # 'amissl',
            # 'bearssl',
            "gnutls",
            conditional("mbedtls", when="@7.46:"),
            # 'mesalink',
            conditional("nss", when="@:7.81"),
            "openssl",
            # 'rustls',
            # 'schannel',
            "secure_transport",
            # 'wolfssl',
            conditional("sspi", when="platform=windows"),
        ),
        multi=True,
    )
    variant("nghttp2", default=True, description="build nghttp2 library (requires C++11)")
    variant("libssh2", default=False, description="enable libssh2 support")
    variant("libssh", default=False, description="enable libssh support", when="@7.58:")
    variant("gssapi", default=False, description="enable Kerberos support")
    variant("librtmp", default=False, description="enable Rtmp support")
    variant("ldap", default=False, description="enable ldap support")
    variant("libidn2", default=False, description="enable libidn2 support")
    variant(
        "libs",
        default="shared,static" if not is_windows else "shared",
        values=("shared", "static"),
        multi=not is_windows,
        description="Build shared libs, static libs or both",
    )

    conflicts("platform=linux", when="tls=secure_transport", msg="Only supported on macOS")

    depends_on("pkgconfig", type="build", when="platform=darwin")
    depends_on("pkgconfig", type="build", when="platform=linux")
    depends_on("pkgconfig", type="build", when="platform=freebsd")

    depends_on("gnutls", when="tls=gnutls")

    with when("tls=mbedtls"):
        depends_on("mbedtls +pic")
        depends_on("mbedtls@:2", when="@:7.78")
        depends_on("mbedtls@:3.5", when="@:8.7")
        depends_on("mbedtls@2:", when="@7.79:")
        depends_on("mbedtls@3.2:", when="@8.8")  # https://github.com/curl/curl/issues/13748

    depends_on("nss", when="tls=nss")

    with when("tls=openssl"):
        depends_on("openssl")
        # Since https://github.com/curl/curl/commit/ee36e86ce8f77a017c49b8312814c33f4b969565
        # there is OpenSSL 3 detection.
        depends_on("openssl@:1", when="@:7.76")

    depends_on("libidn2", when="+libidn2")
    depends_on("zlib-api")
    depends_on("nghttp2", when="+nghttp2")
    depends_on("libssh2", when="+libssh2")
    depends_on("libssh", when="+libssh")
    depends_on("krb5", when="+gssapi")
    depends_on("rtmpdump", when="+librtmp")

    # https://github.com/curl/curl/issues/12832
    # https://github.com/curl/curl/issues/13508
    depends_on("perl", type="build", when="@8.6:8.7.1")

    # https://github.com/curl/curl/pull/9054
    patch("easy-lock-sched-header.patch", when="@7.84.0")

    build_system("autotools", conditional("nmake", when="platform=windows"), default="autotools")

    @classmethod
    def determine_version(cls, exe):
        curl = Executable(exe)
        output = curl("--version", output=str, error=str)
        match = re.match(r"curl ([\d.]+)", output)
        return match.group(1) if match else None

    @classmethod
    def determine_variants(cls, exes, version):
        for exe in exes:
            variants = ""
            curl = Executable(exe)
            output = curl("--version", output=str, error=str)
            if "nghttp2" in output:
                variants += "+nghttp2"
            protocols_match = re.search(r"Protocols: (.*)\n", output)
            if protocols_match:
                protocols = protocols_match.group(1).strip().split(" ")
                if "ldap" in protocols:
                    variants += "+ldap"
            features_match = re.search(r"Features: (.*)\n", output)
            if features_match:
                features = features_match.group(1).strip().split(" ")
                if "GSS-API" in features:
                    variants += "+gssapi"
            # TODO: Determine TLS backend if needed.
            # TODO: Determine more variants.
            return variants

    @property
    def command(self):
        return Executable(self.prefix.bin.join("curl-config"))

    def flag_handler(self, name, flags):
        build_system_flags = []
        spec = self.spec
        if name == "cflags" and (spec.satisfies("%intel") or spec.satisfies("%oneapi")):
            build_system_flags = ["-we147"]
        return flags, None, build_system_flags


class BuildEnvironment:
    def setup_dependent_build_environment(self, env, dependent_spec):
        if self.spec.satisfies("libs=static"):
            env.append_flags("CFLAGS", "-DCURL_STATICLIB")
            env.append_flags("CXXFLAGS", "-DCURL_STATICLIB")


class AutotoolsBuilder(AutotoolsBuilder):
    def configure_args(self):
        spec = self.spec

        args = [
            "--with-zlib=" + spec["zlib-api"].prefix,
            # Prevent unintentional linking against system libraries: we could
            # add variants for these in the future
            "--without-brotli",
            "--without-libgsasl",
            "--without-libpsl",
            "--without-zstd",
            "--disable-manual",
        ]

        if spec.satisfies("@8.7:"):
            args.append("--disable-docs")

        args += self.enable_or_disable("libs")

        # Make gnutls / openssl decide what certs are trusted.
        # TODO: certs for other tls options.
        if spec.satisfies("tls=gnutls") or spec.satisfies("tls=openssl"):
            args.extend(["--without-ca-bundle", "--without-ca-path", "--with-ca-fallback"])

        # https://daniel.haxx.se/blog/2021/06/07/bye-bye-metalink-in-curl/
        # We always disable it explicitly, but the flag is gone in newer
        # versions.
        if spec.satisfies("@:7.77"):
            args.append("--without-libmetalink")

        if spec.satisfies("+gssapi"):
            args.append("--with-gssapi=" + spec["krb5"].prefix)
        else:
            args.append("--without-gssapi")

        args += self.with_or_without("tls")
        args += self.with_or_without("libidn2", activation_value="prefix")
        args += self.with_or_without("librtmp")
        args += self.with_or_without("nghttp2", activation_value="prefix")
        args += self.with_or_without("libssh2", activation_value="prefix")
        args += self.with_or_without("libssh", activation_value="prefix")
        args += self.enable_or_disable("ldap")

        return args

    def with_or_without_gnutls(self, activated):
        if activated:
            return "--with-gnutls=" + self.spec["gnutls"].prefix
        else:
            return "--without-gnutls"

    def with_or_without_mbedtls(self, activated):
        if self.spec.satisfies("@7.46:"):
            if activated:
                return "--with-mbedtls=" + self.spec["mbedtls"].prefix
            else:
                return "--without-mbedtls"

    def with_or_without_nss(self, activated):
        if activated:
            return "--with-nss=" + self.spec["nss"].prefix
        else:
            return "--without-nss"

    def with_or_without_openssl(self, activated):
        if self.spec.satisfies("@7.77:"):
            if activated:
                return "--with-openssl=" + self.spec["openssl"].prefix
            else:
                return "--without-openssl"
        else:
            if activated:
                return "--with-ssl=" + self.spec["openssl"].prefix
            else:
                return "--without-ssl"

    def with_or_without_secure_transport(self, activated):
        if self.spec.satisfies("@7.65:"):
            if activated:
                return "--with-secure-transport"
            else:
                return "--without-secure-transport"
        else:
            if activated:
                return "--with-darwinssl"
            else:
                return "--without-darwinssl"


class NMakeBuilder(BuildEnvironment, NMakeBuilder):
    phases = ["install"]

    def nmake_args(self):
        args = []
        mode = "dll" if self.spec.satisfies("libs=shared") else "static"
        args.append("mode=%s" % mode)
        args.append("WITH_ZLIB=%s" % mode)
        args.append("ZLIB_PATH=%s" % self.spec["zlib-api"].prefix)
        if self.spec.satisfies("+libssh"):
            args.append("WITH_SSH=%s" % mode)
        if self.spec.satisfies("+libssh2"):
            args.append("WITH_SSH2=%s" % mode)
            args.append("SSH2_PATH=%s" % self.spec["libssh2"].prefix)
        if self.spec.satisfies("+nghttp2"):
            args.append("WITH_NGHTTP2=%s" % mode)
            args.append("NGHTTP2=%s" % self.spec["nghttp2"].prefix)
        if self.spec.satisfies("tls=openssl"):
            args.append("WITH_SSL=%s" % mode)
            args.append("SSL_PATH=%s" % self.spec["openssl"].prefix)
        elif self.spec.satisfies("tls=mbedtls"):
            args.append("WITH_MBEDTLS=%s" % mode)
            args.append("MBEDTLS_PATH=%s" % self.spec["mbedtls"].prefix)
        elif self.spec.satisfies("tls=sspi"):
            args.append("ENABLE_SSPI=%s" % mode)

        # The trailing path seperator is REQUIRED for cURL to install
        # otherwise cURLs build system will interpret the path as a file
        # and the install will fail with ambiguous errors
        inst_prefix = self.prefix + "\\"
        args.append(f"WITH_PREFIX={windows_sfn(inst_prefix)}")
        return args

    def install(self, pkg, spec, prefix):
        # Spack's env CC and CXX values will cause an error
        # if there is a path in the space, and escaping with
        # double quotes raises a syntax issues, instead
        # cURLs nmake will automatically invoke proper cl.exe if
        # no env value for CC, CXX is specified
        # Unset the value to allow for cURLs heuristics (derive via VCVARS)
        # to derive the proper compiler
        env = os.environ
        env["CC"] = ""
        env["CXX"] = ""
        winbuild_dir = os.path.join(self.stage.source_path, "winbuild")
        winbuild_dir = windows_sfn(winbuild_dir)
        with working_dir(winbuild_dir):
            nmake("/f", "Makefile.vc", *self.nmake_args(), ignore_quotes=True)
        with working_dir(os.path.join(self.stage.source_path, "builds")):
            install_dir = glob.glob("libcurl-**")[0]
            install_tree(install_dir, self.prefix)
        if spec.satisfies("libs=static"):
            # curl is named libcurl_a when static on Windows
            # Consumers look for just libcurl
            # make a symlink to make consumers happy
            libcurl_a = os.path.join(prefix.lib, "libcurl_a.lib")
            libcurl = os.path.join(self.prefix.lib, "libcurl.lib")
            # safeguard against future curl releases that do this for us
            if os.path.exists(libcurl_a) and not os.path.exists(libcurl):
                symlink(libcurl_a, libcurl)
