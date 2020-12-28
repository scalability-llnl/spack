# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Taskd(CMakePackage):
    """TaskWarrior task synchronization daemon"""

    homepage = "http://www.taskwarrior.org"
    url      = "http://taskwarrior.org/download/taskd-1.1.0.tar.gz"

    version('1.1.0', sha256='7b8488e687971ae56729ff4e2e5209ff8806cf8cd57718bfd7e521be130621b4')

    depends_on('libuuid')
    depends_on('gnutls')
    depends_on('cmake@2.8:', type='build')

    conflicts('%gcc@:4.7')
