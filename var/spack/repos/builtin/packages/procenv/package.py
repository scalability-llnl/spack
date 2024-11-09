# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Procenv(AutotoolsPackage):
    """A command-line tool that displays as much detail about itself and
    its environment as possible.  It can be used as a test tool, to
    understand the type of environment a process runs in, and for
    comparing system environments."""

    homepage = "https://github.com/jamesodhunt/procenv/"
    url = "https://github.com/jamesodhunt/procenv/archive/0.51.tar.gz"

    license("GPL-3.0-or-later")

    version("0.60", sha256="fac0438bf08ed73b10ace78d85acb83cf81ade5ecf866762c2c6e92e41dbde43")
    version("0.51", sha256="b831c14729e06a285cc13eba095817ce3b6d0ddf484b1264951b03ee4fe25bc9")

    depends_on("c", type="build")  # generated

    # https://github.com/jamesodhunt/procenv/pull/16
    patch("7cafed1316ddb16fe0689d54ba10c05dd2edd347.patch", when="@:0.51")

    depends_on("expat")
    depends_on("libpcap")
    # Fixme: package these and use conditionally (on linux)
    # depends_on('libselinux')
    # depends_on('libapparmor')
    depends_on("numactl")
    depends_on("check", type="build")
