# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Multitail(MakefilePackage):
    """MultiTail allows you to monitor logfiles and command output
    in multiple windows in a terminal, colorize, filter and merge."""

    homepage = "https://www.vanheusden.com/multitail/index.php"
    url = "https://www.vanheusden.com/multitail/multitail-6.4.2.tgz"

    license("Apache-2.0")

    version("6.4.2", sha256="af1d5458a78ad3b747c5eeb135b19bdca281ce414cefdc6ea0cff6d913caa1fd")

    depends_on("ncurses")

    # It's counterintuitive, but use DESTDIR for the install because
    # the Makefile doesn't consistently use PREFIX with the things
    # it's installing...
    @property
    def install_targets(self):
        targets = []
        targets.append("PREFIX=")
        targets.append("DESTDIR={0}".format(self.prefix))
        targets.append("install")
        return targets

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")

        nc_include_flags = spec["ncurses"].headers.include_flags
        nc_ld_flags = spec["ncurses"].libs.ld_flags
        makefile.filter(r"CFLAGS\+=", "CFLAGS+={0} ".format(nc_include_flags))
        makefile.filter(r"LDFLAGS\+=", "LDFLAGS+={0} ".format(nc_ld_flags))

        # Copy the conf file directly into place (don't worry about
        # overwriting an existing file...)
        kwargs = {"ignore_absent": False, "backup": False, "string": True}
        makefile.filter(
            r"cp multitail.conf $(CONFIG_FILE).new", "cp multitail.conf $(CONFIG_FILE)", **kwargs
        )
