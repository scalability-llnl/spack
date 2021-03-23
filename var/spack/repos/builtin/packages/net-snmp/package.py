# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class NetSnmp(AutotoolsPackage):
    """A SNMP application library, tools and daemon."""

    homepage = "http://www.net-snmp.org/"
    url      = "https://sourceforge.net/projects/net-snmp/files/net-snmp/5.9/net-snmp-5.9.tar.gz"

    version('5.9', sha256='04303a66f85d6d8b16d3cc53bde50428877c82ab524e17591dfceaeb94df6071')

    depends_on('perl-extutils-makemaker')
    depends_on('ncurses')

    def configure_args(self):
        args = ['--with-defaults', 'LIBS=-ltinfo']
        return args
