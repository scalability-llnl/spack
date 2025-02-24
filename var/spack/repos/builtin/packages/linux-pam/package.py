# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LinuxPam(AutotoolsPackage):
    """Linux PAM (Pluggable Authentication Modules for Linux) project."""

    homepage = "http://www.linux-pam.org/"
    url = "https://github.com/linux-pam/linux-pam/releases/download/v1.5.2/Linux-PAM-1.5.2.tar.xz"

    license("BSD-3-Clause")

    version("1.6.1", sha256="f8923c740159052d719dbfc2a2f81942d68dd34fcaf61c706a02c9b80feeef8e")
    version("1.6.0", sha256="fff4a34e5bbee77e2e8f1992f27631e2329bcbf8a0563ddeb5c3389b4e3169ad")
    version("1.5.3", sha256="7ac4b50feee004a9fa88f1dfd2d2fa738a82896763050cd773b3c54b0a818283")
    version("1.5.2", sha256="e4ec7131a91da44512574268f493c6d8ca105c87091691b8e9b56ca685d4f94d")
    version("1.5.1", sha256="201d40730b1135b1b3cdea09f2c28ac634d73181ccd0172ceddee3649c5792fc")
    version("1.5.0", sha256="02d39854b508fae9dc713f7733bbcdadbe17b50de965aedddd65bcb6cc7852c8")
    version("1.4.0", sha256="cd6d928c51e64139be3bdb38692c68183a509b83d4f2c221024ccd4bcddfd034")
    version("1.3.1", sha256="eff47a4ecd833fbf18de9686632a70ee8d0794b79aecb217ebd0ce11db4cd0db")

    variant("unix", default=True, description="Build pam_unix model")
    variant("selinux", default=False, description="Build with selinux support")
    variant("nls", default=False, description="Build with natural language support")
    variant("xauth", default=False, description="Build with xauth support")
    variant("openssl", default=False, description="Build with openssl support")
    variant("lastlog", default=False, description="Build pam_lastlog model")
    variant("regenerate-docu", default=False, description="Regenerate docs")

    depends_on("pkgconfig", type="build")
    depends_on("libtirpc")
    depends_on("libxcrypt")
    depends_on("xauth", when="+xauth")
    depends_on("c", type="build")

    with default_args(type="build"):
        depends_on("m4")
        depends_on("autoconf")
        depends_on("automake")
        depends_on("libtool")
        depends_on("gettext", when="+nls")
        with when("+regenerate-docu"):
            depends_on("bison")
            depends_on("flex")
            depends_on("yacc")

    def flag_handler(self, name, flags):
        if name == "ldflags" and self.spec.satisfies("+nls"):
            flags += ["-lintl"]  # Addresses https://github.com/spack/spack/issues/44637
        return (flags, None, None)

    def configure_args(self):
        args = [f"--includedir={self.prefix.include.security}"]

        args += self.enable_or_disable("nls")
        args += self.enable_or_disable("openssl")
        args += self.enable_or_disable("unix")
        args += self.enable_or_disable("lastlog")
        args += self.enable_or_disable("selinux")
        args += self.enable_or_disable("regenerate-docu")

        if self.spec.satisfies("+xauth"):
            xauth = self.spec["xauth"]
            args.append(f"--with-xauth={xauth.prefix.bin.xauth}")

        return args
