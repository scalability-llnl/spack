# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import llnl.util.tty as tty

from spack.package import *


class Freeipmi(AutotoolsPackage):
    """FreeIPMI provides in-band and out-of-band IPMI software based on the IPMI
    v1.5/2.0 specification. The IPMI specification defines a set of interfaces
    for platform management and is implemented by a number vendors for system
    management. The features of IPMI that most users will be interested in are
    sensor monitoring, system event monitoring, power control, and
    serial-over-LAN (SOL). The FreeIPMI tools and libraries listed below should
    provide users with the ability to access and utilize these and many other
    features. A number of useful features for large HPC or cluster environments
    have also been implemented into FreeIPMI. See the README or FAQ for more
    info."""

    homepage = "https://www.gnu.org/software/freeipmi/"
    url = "https://ftp.gnu.org/gnu/freeipmi/freeipmi-1.6.4.tar.gz"

    license("GPL-3.0-or-later")

    version("1.6.9", sha256="f25e1c35f3d0f1b5a99cc31ecc2353ca83ed46a15163842fba870127dc9c8206")
    version("1.6.4", sha256="65dfbb95a30438ba247f01a58498862a37d2e71c8c950bcfcee459d079241a3c")

    depends_on("c", type="build")  # generated

    depends_on("libgcrypt")

    parallel = False

    def configure_args(self):
        # FIXME: If root checking of root installation is added fix this:
        # Discussed in issue  #4432
        tty.warn(
            "Requires 'root' for bmc-watchdog.service installation to" " /lib/systemd/system/ !"
        )

        args = [
            "--prefix={0}".format(prefix),
            "--with-systemdsystemunitdir=" + self.spec["freeipmi"].prefix.lib.systemd.system,
        ]

        return args
