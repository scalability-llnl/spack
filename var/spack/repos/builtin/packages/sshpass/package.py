# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sshpass(AutotoolsPackage):
    """Sshpass is a tool for non-interactivly performing password
    authentication with SSH's so called "interactive keyboard
    password authentication". Most user should use SSH's more
    secure public key authentiaction instead."""

    homepage = "https://sourceforge.net/projects/sshpass/"
    url = "https://sourceforge.net/projects/sshpass/files/sshpass/1.06/sshpass-1.06.tar.gz"

    license("GPL-2.0-or-later")

    version("1.06", sha256="c6324fcee608b99a58f9870157dfa754837f8c48be3df0f5e2f3accf145dee60")
    version("1.05", sha256="c3f78752a68a0c3f62efb3332cceea0c8a1f04f7cf6b46e00ec0c3000bc8483e")
    version("1.04", sha256="e8abb9a409f25928722251a5855a74854f6d64af3eb136b804a04fd630d70c80")
    version("1.03", sha256="5e8082343f5eae43598bb5723fa11bf49d3c9864dc58c7513fe1a90658e52b2f")
    version("1.02", sha256="e580d999eefbd847c5cd0b36315cb6cd187315c4e7d1cb182b9f94c12c7c6a86")
    version("1.01", sha256="e2adc378d61b72e63b4381fe123de3c63bd4093c9553d3219e83878f379754f4")
    version("1.00", sha256="71d4be85a464a8ce2ae308bc04dcb342918f3989b6a81c74217b5df7f11471f8")

    depends_on("c", type="build")  # generated

    depends_on("m4", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
