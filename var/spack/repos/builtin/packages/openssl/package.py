# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

import llnl.util.tty as tty

from spack.package import *


class Openssl(Package):  # Uses Fake Autotools, should subclass Package
    """OpenSSL is an open source project that provides a robust, commercial-grade, and
    full-featured toolkit for the Transport Layer Security (TLS) and Secure Sockets Layer (SSL)
    protocols. It is also a general-purpose cryptography library."""

    homepage = "https://www.openssl.org"

    url = "https://www.openssl.org/source/openssl-1.1.1d.tar.gz"
    list_url = "https://www.openssl.org/source/old/"
    list_depth = 1

    maintainers("AlexanderRichert-NOAA")

    tags = ["core-packages", "windows"]

    executables = ["openssl"]

    license("Apache-2.0")

    version("3.3.1", sha256="777cd596284c883375a2a7a11bf5d2786fc5413255efab20c50d6ffe6d020b7e")
    version("3.2.2", sha256="197149c18d9e9f292c43f0400acaba12e5f52cacfe050f3d199277ea738ec2e7")
    version("3.1.6", sha256="5d2be4036b478ef3cb0a854ca9b353072c3a0e26d8a56f8f0ab9fb6ed32d38d7")
    version("3.0.14", sha256="eeca035d4dd4e84fc25846d952da6297484afa0650a6f84c682e39df3a4123ca")

    version(
        "3.3.0",
        sha256="53e66b043322a606abf0087e7699a0e033a37fa13feb9742df35c3a33b18fb02",
        deprecated=True,
    )
    version(
        "3.2.1",
        sha256="83c7329fe52c850677d75e5d0b0ca245309b97e8ecbcfdc1dfdc4ab9fac35b39",
        deprecated=True,
    )
    version(
        "3.1.5",
        sha256="6ae015467dabf0469b139ada93319327be24b98251ffaeceda0221848dc09262",
        deprecated=True,
    )
    version(
        "3.0.13",
        sha256="88525753f79d3bec27d2fa7c66aa0b92b3aa9498dafd93d7cfa4b3780cdae313",
        deprecated=True,
    )

    version(
        "1.1.1w",
        sha256="cf3098950cb4d853ad95c0841f1f9c6d3dc102dccfcacd521d93925208b76ac8",
        deprecated=True,
    )
    version(
        "1.0.2u",
        sha256="ecd0c6ffb493dd06707d38b14bb4d8c2288bb7033735606569d8f90f89669d16",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    # On Cray DVS mounts, we can't make symlinks to /etc/ssl/openssl.cnf,
    # either due to a bug or because DVS is not intended to be POSIX compliant.
    # Therefore, stick to system agnostic certs=mozilla.
    variant(
        "certs",
        default="mozilla",
        values=("mozilla", "system", "none"),
        multi=False,
        description=(
            "Use certificates from the ca-certificates-mozilla package, symlink system "
            "certificates, or use none, respectively. The default is `mozilla`, since it is "
            "system agnostic. Instead of picking certs=system, one can mark openssl as an "
            "external package, to avoid compiling openssl entirely."
        ),
    )
    variant("docs", default=False, description="Install docs and manpages")
    variant("shared", default=True, description="Build shared library version")
    with when("platform=windows"):
        variant("dynamic", default=False, description="Link with MSVC's dynamic runtime library")

    depends_on("zlib-api")
    depends_on("perl@5.14.0:", type=("build", "test"))
    depends_on("ca-certificates-mozilla", type="build", when="certs=mozilla")
    depends_on("nasm", when="platform=windows")

    depends_on("gmake", type="build", when="platform=linux")
    depends_on("gmake", type="build", when="platform=darwin")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("version", output=str, error=str)
        match = re.search(r"OpenSSL.(\S+)*", output)
        return match.group(1) if match else None

    @property
    def libs(self):
        return find_libraries(
            ["libssl", "libcrypto"],
            root=self.prefix,
            recursive=True,
            shared=self.spec.variants["shared"].value,
            runtime=False,
        )

    def handle_fetch_error(self, error):
        tty.warn(
            "Fetching OpenSSL failed. This may indicate that OpenSSL has "
            "been updated, and the version in your instance of Spack is "
            "insecure. Consider updating to the latest OpenSSL version."
        )

    def install(self, spec, prefix):
        # OpenSSL uses these variables in its Makefile or config scripts. If any of them
        # happen to be set in the environment, then this will override what is set in
        # the script or Makefile, leading to build errors.
        for v in ("APPS", "BUILD", "RELEASE", "MACHINE", "SYSTEM"):
            env.pop(v, None)

        if str(spec.target.family) in ("x86_64", "ppc64"):
            # This needs to be done for all 64-bit architectures (except Linux,
            # where it happens automatically?)
            env["KERNEL_BITS"] = "64"

        options = ["zlib"]
        if spec.satisfies("@1.0"):
            options.append("no-krb5")
        # clang does not support the .arch directive in assembly files.
        if "clang" in self.compiler.cc and spec.target.family == "aarch64":
            options.append("no-asm")
        elif "%nvhpc" in spec:
            # Last tested on nvidia@22.3 for x86_64:
            # nvhpc segfaults NVC++-F-0000-Internal compiler error.
            # gen_llvm_expr(): unknown opcode       0  (crypto/rsa/rsa_oaep.c: 248)
            options.append("no-asm")
        elif spec.satisfies("@3: %oneapi"):
            # Last tested on oneapi@2023.1.0 for x86_64:
            # crypto/md5/md5-x86_64.s:684:31: error: expected string
            options.append("no-asm")

        # The default glibc provided by CentOS 7 does not provide proper
        # atomic support when using the NVIDIA compilers
        if self.spec.satisfies("%nvhpc os=centos7"):
            options.append("-D__STDC_NO_ATOMICS__")

        # Make a flag for shared library builds
        base_args = [
            "--prefix=%s" % prefix,
            "--openssldir=%s" % join_path(prefix, "etc", "openssl"),
        ]
        if spec.satisfies("platform=windows"):
            if spec.satisfies("@:1"):
                base_args.extend([f'CC="{self.compiler.cc}"', f'CXX="{self.compiler.cxx}"'])
            else:
                base_args.extend([f"CC={self.compiler.cc}", f"CXX={self.compiler.cxx}"])
            base_args.append("VC-WIN64A")
        else:
            base_args.extend(
                [
                    "-I{0}".format(self.spec["zlib-api"].prefix.include),
                    "-L{0}".format(self.spec["zlib-api"].prefix.lib),
                ]
            )
            base_args.extend(options)

        if spec.satisfies("~shared"):
            base_args.append("no-shared")
        else:
            base_args.append("shared")

        # On Windows, we use perl for configuration and build through MSVC
        # nmake.
        if spec.satisfies("platform=windows"):
            # The configure executable requires that paths with spaces
            # on Windows be wrapped in quotes
            Executable("perl")("Configure", *base_args, ignore_quotes=True)
        else:
            Executable("./config")(*base_args)

        # Remove non-standard compiler options if present. These options are
        # present e.g. on Darwin. They are non-standard, i.e. most compilers
        # (e.g. gcc) will not accept them.
        filter_file(r"-arch x86_64", "", "Makefile")

        if spec.satisfies("platform=windows"):
            host_make = nmake
        else:
            host_make = make

        host_make()

        if self.run_tests:
            host_make("test", parallel=False)  # 'VERBOSE=1'

        install_tgt = "install" if self.spec.satisfies("+docs") else "install_sw"

        # See https://github.com/openssl/openssl/issues/7466#issuecomment-432148137
        host_make(install_tgt, parallel=False)

    @run_after("install")
    def link_system_certs(self):
        if self.spec.variants["certs"].value != "system":
            return

        system_dirs = [
            # CentOS, Fedora, RHEL
            "/etc/pki/tls",
            # Ubuntu
            "/usr/lib/ssl",
            # OpenSUSE
            "/etc/ssl",
        ]

        pkg_dir = join_path(self.prefix, "etc", "openssl")

        mkdirp(pkg_dir)

        for directory in system_dirs:
            # Link configuration file
            sys_conf = join_path(directory, "openssl.cnf")
            pkg_conf = join_path(pkg_dir, "openssl.cnf")
            if os.path.exists(sys_conf) and not os.path.exists(pkg_conf):
                os.symlink(sys_conf, pkg_conf)

            sys_cert = join_path(directory, "cert.pem")
            pkg_cert = join_path(pkg_dir, "cert.pem")
            # If a bundle exists, use it. This is the preferred way on Fedora,
            # where the certs directory does not work.
            if os.path.exists(sys_cert) and not os.path.exists(pkg_cert):
                os.symlink(sys_cert, pkg_cert)

            sys_certs = join_path(directory, "certs")
            pkg_certs = join_path(pkg_dir, "certs")
            # If the certs directory exists, symlink it into the package.
            # We symlink the whole directory instead of all files because
            # the directory contents might change without Spack noticing.
            if os.path.isdir(sys_certs) and not os.path.islink(pkg_certs):
                if os.path.isdir(pkg_certs):
                    os.rmdir(pkg_certs)
                os.symlink(sys_certs, pkg_certs)

    @run_after("install")
    def copy_mozilla_certs(self):
        if self.spec.variants["certs"].value != "mozilla":
            return

        pkg_dir = join_path(self.prefix, "etc", "openssl")
        mkdirp(pkg_dir)

        mozilla_pem = self.spec["ca-certificates-mozilla"].pem_path
        pkg_cert = join_path(pkg_dir, "cert.pem")
        install(mozilla_pem, pkg_cert)

    def patch(self):
        if self.spec.satisfies("%nvhpc"):
            # Remove incompatible preprocessor flags
            filter_file("-MF ", "", "Configurations/unix-Makefile.tmpl", string=True)
            filter_file(r"-MT \$\@ ", "", "Configurations/unix-Makefile.tmpl", string=True)

    def setup_build_environment(self, env):
        env.set("PERL", self.spec["perl"].prefix.bin.perl)
