# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libpcap(AutotoolsPackage):
    """libpcap is a portable library in C/C++ for packet capture."""
    homepage = "http://www.tcpdump.org/"
    list_url = "http://www.tcpdump.org/release/"
    url      = "http://www.tcpdump.org/release/libpcap-1.8.1.tar.gz"

    version('1.8.1', sha256='673dbc69fdc3f5a86fb5759ab19899039a8e5e6c631749e48dcd9c6f0c83541e')

    depends_on('flex', type='build')
    depends_on('bison', type='build')
