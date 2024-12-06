# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rrdtool(AutotoolsPackage):
    """RA tool for data logging and analysis."""

    homepage = "https://oss.oetiker.ch/rrdtool"
    url = "https://oss.oetiker.ch/rrdtool/pub/rrdtool-1.7.0.tar.gz"

    license("GPL-2.0-or-later")

    version("1.7.2", sha256="a199faeb7eff7cafc46fac253e682d833d08932f3db93a550a4a5af180ca58db")
    version("1.7.1", sha256="989b778eda6967aa5192c73abafe43e7b10e6100776971a7e79d249942781aae")
    version("1.7.0", sha256="f97d348935b91780f2cd80399719e20c0b91f0a23537c0a85f9ff306d4c5526b")

    depends_on("libxml2")
    depends_on("pango")
    depends_on("lua@5.3.0:5.3.5")
    depends_on("perl-extutils-makemaker")

    def configure_args(self):
        return ["--with-systemdsystemunitdir=" + self.spec["rrdtool"].prefix.lib.systemd.system]

    def flag_handler(self, name, flags):
        if name == "ldlibs" and "intl" in self.spec["gettext"].libs.names:
            flags.append("-lintl")
        return self.build_system_flags(name, flags)
