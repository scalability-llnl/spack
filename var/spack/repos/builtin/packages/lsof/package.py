# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lsof(Package):
    """Lsof displays information about files open to Unix processes."""

    homepage = "https://people.freebsd.org/~abe/"
    url = "https://www.mirrorservice.org/sites/lsof.itap.purdue.edu/pub/tools/unix/lsof/lsof_4.91.tar.gz"
    list_url = "https://www.mirrorservice.org/sites/lsof.itap.purdue.edu/pub/tools/unix/lsof/OLD/"

    license("custom")

    version("4.91", sha256="3ca57887470fdf223a8e8aae4559cd3a26787bea93b94336c90ee8062e29e352")
    version("4.90", sha256="27794d3d6499fd5f0f08710b4518b33aed8a4580951d1adf27f6c25898685c9e")
    version("4.89", sha256="5d08da7ebe049c9d9a6472d6afb81aa5af54c4733a3f8822cbc22b57867633c9")

    def install(self, spec, prefix):
        tar = which("tar")
        tar("xf", "lsof_{0}_src.tar".format(self.version))

        with working_dir("lsof_{0}_src".format(self.version)):
            configure = Executable("./Configure")
            configure("-n", "linux")

            make()

            mkdir(prefix.bin)
            install("lsof", prefix.bin)
