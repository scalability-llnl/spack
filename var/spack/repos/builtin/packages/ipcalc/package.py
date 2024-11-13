# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Ipcalc(MakefilePackage):
    """This is a modern tool to assist in network address calculations
    for IPv4 and IPv6. It acts both as a tool to output human readable
    information about a network or address, as well as a tool suitable
    to be used by scripts or other programs."""

    homepage = "https://gitlab.com/ipcalc/ipcalc"
    url = "https://github.com/nmav/ipcalc/archive/0.2.3.tar.gz"

    license("GPL-2.0-or-later")

    version("0.2.3", sha256="c416f34d381a7333ad8aa8982fcfc88434818b3cc35a33b62a75c10f2a6af3c9")
    version("0.2.2", sha256="bf1b95eca219e564c85fa4233fe65342963cf3e8a303a7e10b4dd7269c864794")
    version("0.2.0", sha256="c965c1296172a6acc50d54dfe81f7e5d589f9762b5d9ae459eee00349675336b")

    depends_on("c", type="build")  # generated

    depends_on("geoip-api-c")

    def setup_build_environment(self, env):
        env.prepend_path("LIBPATH", self.spec["geoip-api-c"].prefix.lib)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("ipcalc", prefix.bin)
