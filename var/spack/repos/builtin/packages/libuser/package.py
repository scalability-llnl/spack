# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libuser(AutotoolsPackage):
    """A user and group account administration library."""

    homepage = "https://pagure.io/libuser"
    url = "https://releases.pagure.org/libuser/libuser-0.62.tar.xz"

    license("LGPL-2.0-or-later")

    version("0.62", sha256="a58ff4fabb01a25043b142185a33eeea961109dd60d4b40b6a9df4fa3cace20b")
    version("0.61", sha256="0a114a52446e12781e2ffdf26f59df0d14e7809c7db5e551d3cf61c4e398751d")
    version("0.60", sha256="b1f73408ebfee79eb01a47c5879a2cdef6a00b75ee24870de7df1b816ff483eb")

    depends_on("c", type="build")  # generated

    depends_on("glib")
    depends_on("linux-pam")
    depends_on("popt")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
