# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ssmtp(AutotoolsPackage):
    """A program that replaces sendmail on workstations that should send their
    mail via the departmental mailhub from which they pick up their mail."""

    homepage = "https://salsa.debian.org/debian/ssmtp"
    url = "https://deb.debian.org/debian/pool/main/s/ssmtp/ssmtp_2.64.orig.tar.bz2"

    license("GPL-2.0")

    version("2.64", sha256="22c37dc90c871e8e052b2cab0ad219d010fa938608cd66b21c8f3c759046fa36")

    depends_on("c", type="build")  # generated

    variant("ssl", default=True, description="Enable support for secure connection to mail server")
    variant("inet6", default=True, description="Enable support for IPv6 transport")
    variant("md5auth", default=True, description="Enable support for MD5 authentication")

    depends_on("libnsl")
    depends_on("openssl", when="+ssl")

    patch("install.patch")

    @when("+ssl")
    def setup_build_environment(self, env):
        # The configure script is generated with a very old version of
        # autoconf, which cannot accept LIBS as a command-line argument
        env.set("LIBS", self.spec["openssl"].libs.link_flags)

    def configure_args(self):
        args = self.enable_or_disable("ssl")
        args += self.enable_or_disable("inet6")
        args += self.enable_or_disable("md5auth")
        return args

    def install(self, spec, prefix):
        install_answers = [
            # Please enter the mail name of your system.
            # This is the hostname portion of the address to be shown
            # on outgoing news and mail messages headers.
            # The default is your system's host name.
            #
            # Mail name [system.host.name]:
            "\n",
            # Please enter the SMTP port number [25]:
            "\n",
        ]
        install_answers_filename = "spack-install.in"
        with working_dir(self.build_directory):
            with open(install_answers_filename, "w") as f:
                f.writelines(install_answers)
            make("install-sendmail", input=install_answers_filename)
