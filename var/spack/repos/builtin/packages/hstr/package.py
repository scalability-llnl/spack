# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Hstr(AutotoolsPackage):
    """hstr(hh) is a shell history suggest box for Bash and Zsh,
    which enables easy viewing, searching and using
    your command history."""

    homepage = "https://github.com/dvorka/hstr"
    url = "https://github.com/dvorka/hstr/archive/1.22.tar.gz"

    license("Apache-2.0")

    version("1.22", sha256="384fee04e4c80a1964dcf443131c1da4a20dd474fb48132a51d3de0a946ba996")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("ncurses@5.9")
    depends_on("readline")
