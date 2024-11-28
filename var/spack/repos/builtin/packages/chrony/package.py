# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Chrony(AutotoolsPackage):
    """chrony is a versatile implementation of the Network Time
    Protocol (NTP). It can synchronise the system clock with NTP
    servers, reference clocks(e.g. GPS receiver), and manual
    input using wristwatch and keyboard."""

    homepage = "https://chrony.tuxfamily.org/"
    url = "https://github.com/mlichvar/chrony/archive/3.5.1.tar.gz"

    license("GPL-2.0-or-later")

    version("3.5.1", sha256="881085b944a14853402e1c5cff4de5d815ff104ec6e12eea51c12e42f32f71bd")
    version("3.5", sha256="145a270fe4df42931f175e37dd3771a7e714122ae361921a4b93082e648a08c5")
    version("3.4", sha256="85fbe433f5a3ee961a20c47a72367760b074448587a9e2d3a6788a95750ed77e")
    version("3.3", sha256="0dd7323b5ed9e3208236c1b39fcabf2ad03469fa07ac516ba9c682206133f66d")

    depends_on("c", type="build")  # generated

    depends_on("ruby-asciidoctor")
    depends_on("bison", type="build")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
