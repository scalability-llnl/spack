# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FdFind(Package):
    """A simple, fast and user-friendly alternative to 'find'."""

    homepage = "https://github.com/sharkdp/fd"
    url      = "https://github.com/sharkdp/fd/archive/v7.3.0.tar.gz"

    version('7.4.0', sha256='33570ba65e7f8b438746cb92bb9bc4a6030b482a0d50db37c830c4e315877537')

    depends_on('rust')

    def install(self, spec, prefix):
        cargo = which('cargo')
        cargo('install', '--root', prefix, '--path', '.')
