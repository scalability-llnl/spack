# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lazydocker(GoPackage):
    """The lazier way to manage everything docker."""

    homepage = "https://github.com/jesseduffield/lazydocker"
    url      = "https://github.com/jesseduffield/lazydocker/archive/v0.7.6.tar.gz"

    version('0.7.6', sha256='4f25042036409a1ff675a937a1074d25d8185b056c27f19d164d94b8cdeb446c')

    depends_on('go@1.12:', type='build')  # go.mod overrides default

    executables = ['lazydocker']
