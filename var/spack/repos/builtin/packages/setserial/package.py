# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Setserial(AutotoolsPackage):
    """A utility for configuring serial ports."""

    homepage = "https://setserial.sourceforge.net"
    url = (
        "https://udomain.dl.sourceforge.net/project/setserial/setserial/2.17/setserial-2.17.tar.gz"
    )

    license("GPL-2.0-only")

    version("2.17", sha256="7e4487d320ac31558563424189435d396ddf77953bb23111a17a3d1487b5794a")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        mkdirp(prefix.usr.man.man8)
        make("install", "DESTDIR={0}".format(prefix))
