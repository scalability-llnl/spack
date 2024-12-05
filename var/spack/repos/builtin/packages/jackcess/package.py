# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jackcess(Package):
    """Jackcess is a pure Java library for reading from and writing to
    MS Access databases (currently supporting versions 2000-2016)."""

    homepage = "https://jackcess.sourceforge.net/"
    url = "https://sourceforge.net/projects/jackcess/files/jackcess/2.1.12/jackcess-2.1.12.jar"

    version(
        "2.1.12",
        sha256="347e666d8f6abf382a0e1a7597421911423f20cf71237225f9eb53626f377f22",
        expand=False,
    )
    version(
        "1.2.14.3",
        sha256="a6fab0c4b5daf23dcf7fd309ee4ffc6df12ff982510c094e45442adf88712787",
        expand=False,
        url="https://sourceforge.net/projects/jackcess/files/jackcess/Older%20Releases/1.2.14.3/jackcess-1.2.14.3.jar",
    )

    extends("openjdk")
    depends_on("java", type="run")
    depends_on("commons-lang@2.6", when="@2.1.12", type="run")
    depends_on("commons-lang@2.4", when="@1.2.14.3", type="run")
    depends_on("commons-logging@1.1.3", when="@2.1.12", type="run")
    depends_on("commons-logging@1.1.1", when="@1.2.14.3", type="run")

    def install(self, spec, prefix):
        install("jackcess-{0}.jar".format(self.version), prefix)
