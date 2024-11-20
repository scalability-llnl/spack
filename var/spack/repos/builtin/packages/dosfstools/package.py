# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dosfstools(AutotoolsPackage):
    """dosfstools consists of the programs mkfs.fat, fsck.fat and fatlabel
    to create, check and label file systems of the FAT family."""

    homepage = "https://github.com/dosfstools/dosfstools"
    url = "https://github.com/dosfstools/dosfstools/archive/v4.1.tar.gz"

    license("GPL-3.0-or-later")

    version("4.2", sha256="355a6725524b50e64ae94060ed28579e0e004c519fc964f7085188cd87a99ba7")
    version("4.1", sha256="8ff9c2dcc01551fe9de8888cb41eb1051fd58bdf1ab3a93d3d88916f0a4ffd1b")
    version("4.0", sha256="77975e289e695cb8c984a3c0a15a3bbf3af90be83c26983d43abcde9ec48eea5")

    depends_on("c", type="build")

    depends_on("automake", type="build")
    depends_on("autoconf", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("gettext", when="@4.2:")  # for HAVE_ICONV

    @when("@4.2:")
    def autoreconf(self, spec, prefix):
        Executable("./autogen.sh")()

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
