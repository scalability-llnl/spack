# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libconfuse(AutotoolsPackage):
    """Small configuration file parser library for C."""

    homepage = "https://github.com/martinh/libconfuse"
    url = "https://github.com/martinh/libconfuse/archive/v3.2.2.tar.gz"

    license("0BSD")

    version("3.3", sha256="cb90c06f2dbec971792af576d5b9a382fb3c4ca2b1deea55ea262b403f4e641e")
    version("3.2.2", sha256="2cf7e032980aff8f488efba61510dc3fb95e9a4b9183f985dea457a5651b0e2c")
    version("3.2.1", sha256="2eff8e3c300c4ed1d67fdb13f9d31a72a68e31874b4640db15334305bc40cebd")

    depends_on("c", type="build")  # generated

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("gettext", type="build")
    depends_on("flex", type="build")

    def autoreconf(self, spec, prefix):
        bash = which("bash")
        bash("./autogen.sh")
