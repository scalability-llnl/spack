# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gengetopt(AutotoolsPackage):
    """Tool to write command line option parsing code for C programs"""

    homepage = "https://www.gnu.org/software/gengetopt/gengetopt.html"
    url = "ftp://ftp.gnu.org/gnu/gengetopt/gengetopt-2.23.tar.xz"

    maintainers("rblake-llnl")

    license("GPL-3.0-or-later")

    version("2.23", sha256="b941aec9011864978dd7fdeb052b1943535824169d2aa2b0e7eae9ab807584ac")
    version("2.22.6", sha256="30b05a88604d71ef2a42a2ef26cd26df242b41f5b011ad03083143a31d9b01f7")
    version("2.22.5", sha256="3b6fb3240352b0eb0c5b8583b58b62cbba58167cef5a7e82fa08a7f968ed2137")
    version("2.22.4", sha256="4edf6b24ec8085929c86835c51d5bf904052cc671530c15f9314d9b87fe54421")
    version("2.22.3", sha256="8ce6b3df49cefea97bd522dc054ede2037939978bf23754d5c17311e5a1df3dc")
    version("2.22.2", sha256="4bf96bea9f80ac85c716cd07f5fe68602db7f380f6dc2d025f17139aa0b56455")
    version("2.22.1", sha256="e8d1de4f8c102263844886a2f2b57d82c291c1eae6307ea406fb96f29a67c3a7")
    version("2.22", sha256="b605555e41e9bf7e852a37b051e6a49014e561f21290680e3a60c279488d417e")
    version("2.21", sha256="355a32310b2fee5e7289d6d6e89eddd13275a7c85a243dc5dd293a6cb5bb047e")
    version("2.20", sha256="4c8b3b42cecff579f5f9de5ccad47e0849e0245e325a04ff5985c248141af1a4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("texinfo", type="build")

    parallel = False

    def url_for_version(self, version):
        url = "ftp://ftp.gnu.org/gnu/gengetopt/gengetopt-{0}.tar.{1}"
        if version >= Version("2.23"):
            suffix = "xz"
        else:
            suffix = "gz"
        return url.format(version, suffix)

    def setup_dependent_package(self, module, dependent_spec):
        setattr(module, "gengetopt", Executable(join_path(self.prefix.bin, "gengetopt")))
