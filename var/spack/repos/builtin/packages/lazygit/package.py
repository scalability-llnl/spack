# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lazygit(GoPackage):
    """Simple terminal UI for git commands."""

    homepage = "https://github.com/jesseduffield/lazygit"
    url      = "https://github.com/jesseduffield/lazygit/archive/v0.11.3.tar.gz"

    version('0.11.3', sha256='b3c503de6b34fd4284fd70655e7f42feafc07f090e7f7cc00db261f56c583c46')

    depends_on('go@1.13:', type='build')  # go.mod value overrides default

    executables = ['lazygit']
