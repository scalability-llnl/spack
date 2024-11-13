# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Gnupg(AutotoolsPackage):
    """GNU Pretty Good Privacy (PGP) package."""

    homepage = "https://gnupg.org/index.html"
    url = "https://gnupg.org/ftp/gcrypt/gnupg/gnupg-2.3.4.tar.bz2"

    maintainers("alalazo")

    license("GPL-3.0-or-later")

    version("2.4.5", sha256="f68f7d75d06cb1635c336d34d844af97436c3f64ea14bcb7c869782f96f44277")
    version("2.4.4", sha256="67ebe016ca90fa7688ce67a387ebd82c6261e95897db7b23df24ff335be85bc6")
    version("2.4.3", sha256="a271ae6d732f6f4d80c258ad9ee88dd9c94c8fdc33c3e45328c4d7c126bd219d")
    version("2.4.2", sha256="97eb47df8ae5a3ff744f868005a090da5ab45cb48ee9836dbf5ee739a4e5cf49")
    version("2.4.1", sha256="76b71e5aeb443bfd910ce9cbc8281b617c8341687afb67bae455877972b59de8")
    version("2.4.0", sha256="1d79158dd01d992431dd2e3facb89fdac97127f89784ea2cb610c600fb0c1483")
    version("2.3.8", sha256="540b7a40e57da261fb10ef521a282e0021532a80fd023e75fb71757e8a4969ed")
    version("2.3.7", sha256="ee163a5fb9ec99ffc1b18e65faef8d086800c5713d15a672ab57d3799da83669")
    version("2.2.40", sha256="1164b29a75e8ab93ea15033300149e1872a7ef6bdda3d7c78229a735f8204c28")

    # Versions up to 2.2.27, and 2.3.6 deprecated over CVE-2022-34903
    version(
        "1.4.23",
        sha256="c9462f17e651b6507848c08c430c791287cd75491f8b5a8b50c6ed46b12678ba",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    depends_on("npth@1.2:", when="@2:")

    depends_on("libgpg-error@1.24:", when="@2:")
    depends_on("libgpg-error@1.41:", when="@2.3:")
    depends_on("libgpg-error@1.46:", when="@2.4:")

    depends_on("libgcrypt@1.7.0:", when="@2:")
    depends_on("libgcrypt@1.9.1:", when="@2.3:")

    depends_on("libksba@1.3.4:", when="@2:")
    depends_on("libksba@1.6.3:", when="@2.4:")

    depends_on("libassuan@2.5:", when="@2.2.15:")
    depends_on("libassuan@:2", when="@:2.4.3")

    depends_on("pinentry", type="run", when="@2:")
    depends_on("iconv", when="@2:")
    depends_on("zlib-api")

    depends_on("gawk", type="build", when="@:1")
    # note: perl and curl are gnupg1 dependencies when keyserver support is
    # requested, but we disable that.

    # Getting some linking error.
    conflicts("%gcc@10:", when="@:1")

    executables = ["^gpg$", "^gpg-agent$"]

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"gpg \(GnuPG\) (\S+)", output)
        return match.group(1) if match else None

    @run_after("install")
    def add_gpg2_symlink(self):
        if self.spec.satisfies("@2.0:2"):
            symlink("gpg", self.prefix.bin.gpg2)

    def configure_args(self):
        args = [
            "--disable-nls",
            "--disable-bzip2",
            "--disable-ldap",
            "--disable-regex",
            f"--with-zlib={self.spec['zlib-api'].prefix}",
            "--without-tar",
            "--without-readline",
        ]

        if self.spec.satisfies("@2:"):
            args.extend(
                [
                    "--disable-sqlite",
                    "--disable-ntbtls",
                    "--disable-gnutls",
                    f"--with-pinentry-pgm={self.spec['pinentry'].command.path}",
                    f"--with-libgpg-error-prefix={self.spec['libgpg-error'].prefix}",
                    f"--with-libgcrypt-prefix={self.spec['libgcrypt'].prefix}",
                    f"--with-libassuan-prefix={self.spec['libassuan'].prefix}",
                    f"--with-ksba-prefix={self.spec['libksba'].prefix}",
                    f"--with-npth-prefix={self.spec['npth'].prefix}",
                ]
            )
            if self.spec["iconv"].name == "libiconv":
                args.append(f"--with-libiconv-prefix={self.spec['iconv'].prefix}")
            else:
                args.append("--without-libiconv-prefix")

        if self.spec.satisfies("@:1"):
            args.extend(
                [
                    "--disable-agent-support",
                    "--disable-card-support",
                    "--disable-photo-viewers",
                    "--disable-exec",
                    "--disable-keyserver-path",
                    "--disable-keyserver-helpers",
                    "--disable-gnupg-iconv",
                    "--disable-dns-srv",
                    "--disable-dns-cert",
                    "--disable-gnupg-iconv",
                ]
            )

        if self.run_tests:
            args.append("--enable-all-tests")

        return args
