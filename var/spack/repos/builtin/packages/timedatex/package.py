# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Timedatex(MakefilePackage):
    """timedatex is a D-Bus service that implements the
    org.freedesktop.timedate1 interface. It can be used to
    read and set the system clock, the real-time clock (RTC),
    the system timezone, get a list of valid timezones, and
    enable or disable an NTP client installed on the system.
    It is a replacement for the systemd-timedated service."""

    homepage = "https://github.com/mlichvar/timedatex"
    url = "https://github.com/mlichvar/timedatex/archive/v0.6.tar.gz"

    license("GPL-2.0-or-later")

    version("0.6", sha256="6e24c015769ee49a92bde3b1f167e25119068a00e377f9e4187a425c262ce964")
    version("0.5", sha256="bc54960bb9554bb2b34985ba2b8a78480db568c3c6a9d26f2ab34de1bc0aab11")
    version("0.4", sha256="204285eb03c6cec9ae1c7fdb99e7c996259ec5a918d72bf6bc28564a6f738d4a")

    depends_on("c", type="build")  # generated

    depends_on("glib")

    def install(self, spec, prefix):
        make("install", "prefix={0}".format(prefix))
