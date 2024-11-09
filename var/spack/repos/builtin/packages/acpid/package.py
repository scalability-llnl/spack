# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Acpid(AutotoolsPackage):
    """ACPID used to try to handle events internally.  Rather than try to climb
    an ever-growing mountain, ACPID now lets YOU define what events to handle.
    Any event that publishes itself to /proc/acpi/event can be handled.
    ACPID reads a set of configuration files which define event->action pairs.
    This is how you make it do stuff. See the man page for details."""

    homepage = "http://www.tedfelix.com"
    url = "https://github.com/Distrotech/acpid/archive/2.0.28.tar.gz"

    license("GPL-2.0-or-later")

    version("2.0.28", sha256="cb5709b96f85e1bfee7a3fc17e56bef7244caa1b0ad762a4813fe731ef3c8438")
    version("2.0.27", sha256="da4691f408d9ef201937eaab7c894072ee8aa0ba35794f2388b606b3208fab07")
    version("2.0.26", sha256="ac7238dc5ecc9a915e95d5b54be12b6221d0a0ad09109f9024e50946ecd3c602")
    version("2.0.25", sha256="947d2e4f9b2d61a728ce5d6139901f1b666dcef5e2a48833cb33d82895e261cf")
    version("2.0.24", sha256="05903901369c4ebea1d24e445b4a1d516dd3b07e7864cc752a2d09b4147e1985")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
