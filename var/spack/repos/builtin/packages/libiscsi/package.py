# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libiscsi(AutotoolsPackage):
    """Libiscsi is a client-side library to implement the iSCSI protocol that can
    be used to access the resources of an iSCSI target."""

    homepage = "https://github.com/sahlberg/libiscsi"
    url = "https://github.com/sahlberg/libiscsi/archive/1.19.0.tar.gz"

    version("1.19.0", sha256="c7848ac722c8361d5064654bc6e926c2be61ef11dd3875020a63931836d806df")
    version("1.18.0", sha256="464d104e12533dc11f0dd7662cbc2f01c132f94aa4f5bd519e3413ef485830e8")
    version("1.17.0", sha256="80a7f75bfaffc8bec9920ba7af3f1d14cd862c35c3c5f2c9617b45b975232112")
    version("1.16.0", sha256="35c7be63a8c3a7cee7b697901b6d2dd464e098e1881671eb67462983053b3c7b")
    version("1.15.0", sha256="489e625e58c1e6da2fa3536f9c4b12290f2d3fb4ce14edc0583b8ba500605c34")

    depends_on("c", type="build")  # generated

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    def autoreconf(self, spec, prefix):
        autoreconf("--install", "--force")
