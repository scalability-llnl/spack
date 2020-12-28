# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bat(Package):
    """A cat(1) clone with wings."""

    homepage = 'https://github.com/sharkdp/bat'
    url = 'https://github.com/sharkdp/bat/archive/v0.13.0.tar.gz'

    version('0.13.0', sha256='f4aee370013e2a3bc84c405738ed0ab6e334d3a9f22c18031a7ea008cd5abd2a')
    version('0.12.1', sha256='1dd184ddc9e5228ba94d19afc0b8b440bfc1819fef8133fe331e2c0ec9e3f8e2')

    depends_on('rust')

    def install(self, spec, prefix):
        cargo = which('cargo')
        cargo('install', '--root', prefix, '--path', '.')
