# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class GuacamoleClient(MavenPackage):
    """Apache Guacamole is a clientless remote desktop gateway. It
    supports standard protocols like VNC, RDP, and SSH."""

    homepage = "https://guacamole.apache.org/"
    url      = "https://github.com/apache/guacamole-client/archive/1.2.0.tar.gz"

    version('1.2.0', sha256='2327368a32e61cf82032311be79ded4e5eefbc59ac9fb6e0a054b4f49168843e')

    depends_on('java@8', type=('build', 'run'))
