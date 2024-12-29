# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Keepalived(AutotoolsPackage):
    """
    Keepalived implements a set of checkers to dynamically and adaptively
    maintain and manage loadbalanced server pool according their health
    """

    homepage = "https://www.keepalived.org"
    url = "https://www.keepalived.org/software/keepalived-1.2.0.tar.gz"

    license("GPL-2.0-only")

    version("2.3.1", sha256="92f4b69bfd998e2306d1995ad16fdad1b59e70be694c883385c5f55e02c62aa3")
    version("2.0.19", sha256="0e2f8454765bc6a5fa26758bd9cec18aae42882843cdd24848aff0ae65ce4ca7")
    version("2.0.18", sha256="1423a2b1b8e541211029b9e1e1452e683bbe5f4b0b287eddd609aaf5ff024fd0")
    version("2.0.17", sha256="8965ffa2ffe243014f9c0245daa65f00a9930cf746edf33525d28a86f97497b4")
    version("2.0.16", sha256="f0c7dc86147a286913c1c2c918f557735016285d25779d4d2fce5732fcb888df")
    version("2.0.15", sha256="933ee01bc6346aa573453b998f87510d3cce4aba4537c9642b24e6dbfba5c6f4")
    version("2.0.14", sha256="1bf586e56ee38b47b82f2a27b27e04d0e5b23f1810db6a8e801bde9d3eb8617b")
    version("2.0.13", sha256="c7fb38e8a322fb898fb9f6d5d566827a30aa5a4cd1774f474bb4041c85bcbc46")
    version("2.0.12", sha256="fd50e433d784cfd948de5726752cf89ab7001f587fe10a5110c6c7cbda4b7b5e")
    version("2.0.11", sha256="a298b0c02a20959cfc365b62c14f45abd50d5e0595b2869f5bce10ec2392fa48")

    depends_on("c", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("openssl")

    def configure_args(self):
        args = ["--with-systemdsystemunitdir=" + self.spec["keepalived"].prefix.lib.systemd.system]
        return args
