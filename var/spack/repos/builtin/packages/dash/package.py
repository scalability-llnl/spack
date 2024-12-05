# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dash(AutotoolsPackage):
    """The Debian Almquist Shell."""

    homepage = "https://git.kernel.org/pub/scm/utils/dash/dash.git"
    url = "https://git.kernel.org/pub/scm/utils/dash/dash.git/snapshot/dash-0.5.9.1.tar.gz"
    list_url = homepage

    license("BSD-3-Clause AND GPL-2.0-or-later")

    version("0.5.12", sha256="0d632f6b945058d84809cac7805326775bd60cb4a316907d0bd4228ff7107154")
    version("0.5.9.1", sha256="3f747013a20a3a9d2932be1a6dd1b002ca5649849b649be0af8a8da80bd8a918")

    depends_on("c", type="build")  # generated

    depends_on("libedit", type="link")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    def configure_args(self):
        # Compile with libedit support
        # This allows the use of arrow keys at the command line
        # See https://askubuntu.com/questions/704688
        return ["--with-libedit"]
