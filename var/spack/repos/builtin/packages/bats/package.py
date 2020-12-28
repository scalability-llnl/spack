# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bats(Package):
    """Bats is a TAP-compliant testing framework for Bash."""

    homepage = "https://github.com/sstephenson/bats"
    url      = "https://github.com/sstephenson/bats/archive/v0.4.0.tar.gz"

    version('0.4.0', sha256='480d8d64f1681eee78d1002527f3f06e1ac01e173b761bc73d0cf33f4dc1d8d7')

    def install(self, spec, prefix):
        bash = which("bash")
        bash('install.sh', prefix)
