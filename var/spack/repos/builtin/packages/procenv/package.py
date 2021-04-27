# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Procenv(AutotoolsPackage):
    """A command-line tool that displays as much detail about itself and
    its environment as possible.  It can be used as a test tool, to
    understand the type of environment a process runs in, and for
    comparing system environments."""

    homepage = "https://github.com/jamesodhunt/procenv/"
    url      = "https://github.com/jamesodhunt/procenv/archive/0.51.tar.gz"

    version('0.51', sha256='b831c14729e06a285cc13eba095817ce3b6d0ddf484b1264951b03ee4fe25bc9')

    # https://github.com/jamesodhunt/procenv/pull/16
    patch("7cafed1316ddb16fe0689d54ba10c05dd2edd347.patch", when="@:0.51")

    depends_on('expat')
    depends_on('libpcap')
    # Fixme: package these and use conditionally (on linux)
    # depends_on('libselinux')
    # depends_on('libapparmor')
    depends_on('numactl')
    depends_on('check', type='build')
