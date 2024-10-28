# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Iproute2(AutotoolsPackage):
    """This is a set of utilities for Linux networking."""

    homepage = "https://wiki.linuxfoundation.org/networking/iproute2"
    url = "https://github.com/iproute2/iproute2/archive/v5.9.0.tar.gz"

    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("libmnl")

    license("GPL-2.0-or-later")

    version("6.11.0", sha256="e5ad1c86aa788a979ba1b68cd6ee948b37983d99efabf6a0bf556b061569cc4d")
    version("6.10.0", sha256="060ee42dfcdf8b9daf9f986eee26d16ac5bdf39c8784702957b13bebec538541")
    version("6.2.0", sha256="813d41443d4ee0b189531e0d63f955ce94367ef80b184bcd27a30be86ae715e0")
    version("6.1.0", sha256="63b6057041be86fee8af3468d86fdc1eb2afe1d56500f298413baf89575eff1e")
    version("6.0.0", sha256="0a92b8d04710ab4e649ec25eb919768ba44d3047f26e80621368689d0f3c5a59")
    version("5.17.0", sha256="ab5ed83d901d42a8dd5ec539ab8de35c65f921f002331fc7adfd359def33158d")
    version("5.15.0", sha256="e10161fabe68714b34d565b6efff41b987ffec077f79beec497688c155881ea6")
    version("5.11.0", sha256="16b79e6ce65d4d5fd425cef2fd92a58c403a93faeeed0e0a3202b36a8e857d1f")
    version("5.10.0", sha256="164f1de457eefbdadb98d82c309a0977542b34e7a2dfe81e497a0b93675cb3d2")
    version("5.9.0", sha256="1afde56d416f136b1236ac2f8276e4edbe114ca3c2ab12f11af11b84cf0992e4")
    version("5.8.0", sha256="78c73ed49c35fae59ab4e9d88220dcc70da924de3838e13a3cdc7c09496e5a45")
    version("5.7.0", sha256="12a3861f463c6bbd1bb3b213ac734f75c89172b74104140dd0bbfcb1e13ee798")
    version("5.6.0", sha256="be41c35eddb02e736a2040b66ccfacee41fe7ee454580588f8959568d8a3c5b3")
    version("5.5.0", sha256="5bc88876a3140f640e3318453382be5be4c673ccc17a518c05a5ce2ef9aa9a7f")

    depends_on("c", type="build")  # generated

    def install(self, spec, prefix):
        make("install", "DESTDIR={0}".format(prefix), "PREFIX=")

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix.sbin)
