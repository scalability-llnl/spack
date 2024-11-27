# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Apktool(Package):
    """A tool for reverse engineering 3rd party, closed, binary
    Android apps."""

    homepage = "https://ibotpeaches.github.io/Apktool/"
    url = "https://github.com/iBotPeaches/Apktool/archive/refs/tags/v2.6.0.tar.gz"

    license("Apache-2.0")

    version("2.7.0", sha256="17d12a2955a46c48afb9b6855651016ac17626512216c91e8b2adab0013d3056")
    version("2.6.1", sha256="8932e77d963b9e0e07227422d82ed4a355e8aa268bad1361e5cfaffa8e4d52ee")
    version("2.6.0", sha256="74739cdb1434ca35ec34e51ca7272ad3f378ae3ed0a2d5805d9a2fab5016037f")

    depends_on("java@8:", type=("build", "run"))

    def setup_build_environment(self, env):
        env.set("LC_ALL", "en_US.UTF-8")

    def install(self, spec, prefix):
        gradlew = Executable("./gradlew")
        gradlew("--info", "--debug", "build", "shadowJar")
        ln = which("ln")
        mkdir(join_path(prefix, "bin"))
        install(
            join_path("brut.apktool", "apktool-cli", "build", "libs", "apktool-cli-all.jar"),
            join_path(prefix, "bin"),
        )
        install(join_path("scripts", "linux", "apktool"), join_path(prefix, "bin"))
        ln(
            "-s",
            join_path(prefix, "bin", "apktool-cli-all.jar"),
            join_path(prefix, "bin", "apktool.jar"),
        )
