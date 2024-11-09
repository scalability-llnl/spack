# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Nbdkit(AutotoolsPackage):
    """NBD(Network Block Device) is a protocol for accessing Block Devices
    (hard disks and disk-like things) over a Network. nbdkit is a toolkit
    for creating NBD servers."""

    homepage = "https://github.com/libguestfs/nbdkit"
    url = "https://github.com/libguestfs/nbdkit/archive/v1.23.7.tar.gz"

    license("Ruby")

    version("1.23.7", sha256="70909721f60f06abadfac8646b37f942ceeaf73ce88909ab48402175ae1b6391")
    version("1.23.6", sha256="5a62cbcc41143a90c204d4a48ebe13225f21776fbc4e8fe8ca59531bb1c751fc")
    version("1.23.5", sha256="d07aa309b7d6f088a491fbbe645f23d56cd6e68995c4b73fb5bb609fc6b0de53")
    version("1.23.4", sha256="6581e6cc6dbcb42451abad096efd4e1016b3a0f0d1c7a1724d0a76259ab96429")
    version("1.23.3", sha256="78f14b00c771733047abcf882e715f62bb19820a6571cae0ccb5f965054697c6")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("pkgconfig", type="build")

    def configure_args(self):
        args = ["bashcompdir={0}".format(prefix)]
        return args
