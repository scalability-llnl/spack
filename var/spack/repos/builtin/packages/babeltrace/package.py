# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Babeltrace(AutotoolsPackage):
    """Babeltrace is a trace viewer and converter reading and writing the
    Common Trace Format (CTF). Its main use is to pretty-print CTF traces
    into a human-readable text output ordered by time."""

    homepage = "http://www.efficios.com/babeltrace"
    url      = "https://www.efficios.com/files/babeltrace/babeltrace-1.2.4.tar.bz2"

    version('1.2.4', sha256='666e3a1ad2dc7d5703059963056e7800f0eab59c8eeb6be2efe4f3acc5209eb1')

    depends_on('glib@2.22:', type=('build', 'link'))
    depends_on('libuuid')
    depends_on('popt')
