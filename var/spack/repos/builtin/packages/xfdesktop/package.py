# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Xfdesktop(AutotoolsPackage):
    """Xfdesktop is a desktop manager for the Xfce Desktop Environment."""

    homepage = "https://docs.xfce.org/xfce/xfdesktop/start"
    url = "https://archive.xfce.org/xfce/4.16/src/xfdesktop-4.16.0.tar.bz2"
    list_url = "https://archive.xfce.org/xfce/"
    list_depth = 2

    maintainers("teaguesterling")

    license("GPLv2", checked_by="teaguesterling")  # https://wiki.xfce.org/licenses/audit

    version("4.18.0", sha256="661783e7e6605459926d80bca46d25ce2197c221456457a863ea9d0252120d14")
    version("4.16.0", sha256="934ba5affecff21e62d9fac1dd50c50cd94b3a807fefa5f5bff59f3d6f155bae")

    variant("libnotify", default=True, description="Build with libnotify support")
    variant("thunarx", default=False, description="Build with thunarx support")  # TODO

    # Base requirements
    depends_on("intltool@0.35.0:", type="build")
    with default_args(type=("build", "link", "run")):
        depends_on("xfconf")
        depends_on("libxfce4ui")
        depends_on("libwnck")
        depends_on("exo")
        depends_on("garcon")
        depends_on("glib@2:")
        depends_on("gtkplus@3:")

        depends_on("libnotify", when="+libnotify")

        with when("@4.18.0:"):
            depends_on("glib@2.66:")
            depends_on("gtkplus@3.24:")
        with when("@4.16.0:"):
            depends_on("glib@2.50:")
            depends_on("gtkplus@3.22:")

    def configure_args(self):
        args = []

        args += self.enable_or_disable("libnotify")

        return args
