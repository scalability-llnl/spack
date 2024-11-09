# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pass(MakefilePackage):
    """A minimal password manager following the UNIX philosphy."""

    homepage = "https://www.passwordstore.org/"
    git = "https://git.zx2c4.com/password-store.git"

    maintainers("alecbcs", "taliaferro")

    license("GPL-2.0", checked_by="taliaferro")

    version("1.7.4", tag="1.7.4", commit="1078f2514d579178d5df7042c6a790e9c9b731ad")

    variant("xclip", default=False, description="install the X11 clipboard provider")

    depends_on("bash")
    depends_on("gnupg")
    depends_on("git")
    depends_on("tree")
    depends_on("util-linux")  # for GNU getopt
    depends_on("libqrencode")
    depends_on("openssl")  # used for base64 only

    depends_on("xclip", when="+xclip")

    def setup_build_environment(self, env):
        env.set("PREFIX", prefix)
        env.set("WITH_ALLCOMP", "yes")

    def edit(self, spec, prefix):
        """
        Pass's install process involves slotting in a small script snippet at
        the start of the file, defining certain platform-specific behaviors
        including the paths where some of its key dependencies are likely to
        be found. Most of this logic still works when installed with Spack,
        but the paths to the dependencies are wrong (for example, on MacOS
        it looks for getopt in /opt/homebrew.) We can hardcode those paths here.
        """

        bash_exec = self.spec["bash"].command
        gpg_exec = self.spec["gnupg"].prefix.bin.gpg
        getopt_exec = self.spec["util-linux"].prefix.bin.getopt
        openssl_exec = self.spec["openssl"].command

        platform_files = FileFilter(
            "src/password-store.sh",
            "src/platform/darwin.sh",
            "src/platform/freebsd.sh",
            "src/platform/openbsd.sh",
            "src/platform/cygwin.sh",
        )

        platform_files.filter("^#!.*$", f"#! {bash_exec}")
        platform_files.filter('^GPG="gpg"$', f'GPG="{gpg_exec}"')
        platform_files.filter('^GETOPT=".*"$', f'GETOPT="{getopt_exec}"')
        platform_files.filter('^BASE64=".*"$', f'BASE64="{openssl_exec} base64"')
