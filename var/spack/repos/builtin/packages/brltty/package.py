# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Brltty(AutotoolsPackage):
    """BRLTTY is a background process (daemon) providing access to the
    Linux/Unix console (when in text mode) for a blind person using
    a refreshable braille display."""

    homepage = "https://brltty.app/"
    url = "https://github.com/brltty/brltty/archive/BRLTTY-6.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("6.0", sha256="acfea5274bdc9230b0ea1a87f8796e241615d4d2c1ba08d87601b9d116c7804c")
    version("5.6", sha256="74f35043943525396b340b9f65f0d73c3cc4054a8f63d1c685f27ccf59f46c5d")
    version("5.5", sha256="cd80a0d225f13779791dc3a72d7f137c06c48e5f2c9600e80a565d2378422207")
    version("5.4", sha256="9ad5a540d29438a755f8b8f1f1534e0eba601c604f3d8223fa00b802959ec636")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("expat")
    depends_on("alsa-lib", when="platform=linux", type="link")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("autogen")
