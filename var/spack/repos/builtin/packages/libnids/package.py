# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libnids(AutotoolsPackage):
    """Libnids is a library that provides a functionality of one of
    NIDS (Network Intrusion Detection System) components, namely
    E-component."""

    homepage = "http://libnids.sourceforge.net/"
    url      = "https://github.com/MITRECND/libnids/archive/1.25.tar.gz"
    git      = "https://github.com/MITRECND/libnids.git"

    version('master', branch='master')
    version('1.25', sha256='47aa634bd0cdad81e092fac3aef6f12ee346c2f536a1eff4d3d5dacdb6dfcec1')

    depends_on('libpcap')
    depends_on('libnet')
    depends_on('glib@2.2.0:')
