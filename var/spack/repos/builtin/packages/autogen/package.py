# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Autogen(AutotoolsPackage, GNUMirrorPackage):
    """AutoGen is a tool designed to simplify the creation and maintenance of
    programs that contain large amounts of repetitious text. It is especially
    valuable in programs that have several blocks of text that must be kept
    synchronized."""

    homepage = "https://www.gnu.org/software/autogen/index.html"
    gnu_mirror_path = "autogen/rel5.18.12/autogen-5.18.12.tar.gz"
    list_url = "https://ftp.gnu.org/gnu/autogen"
    list_depth = 1

    license("GPL-3.0-only")

    version("5.18.12", sha256="805c20182f3cb0ebf1571d3b01972851c56fb34348dfdc38799fd0ec3b2badbe")

    depends_on("c", type="build")  # generated

    variant("xml", default=True, description="Enable XML support")

    depends_on("pkgconfig", type="build")

    depends_on("guile@1.8:2.0")
    depends_on("libxml2", when="+xml")

    def configure_args(self):
        spec = self.spec

        args = [
            # `make check` fails without this
            # Adding a gettext dependency does not help
            "--disable-nls"
        ]

        if spec.satisfies("+xml"):
            args.append(f"--with-libxml2={spec['libxml2'].prefix}")
        else:
            args.append("--without-libxml2")

        return args
