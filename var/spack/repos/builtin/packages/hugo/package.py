# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *
from spack.util.executable import which


class Hugo(Package):
    """The world's fastest framework for building websites."""

    homepage = "https://gohugo.io"
    url      = "https://github.com/gohugoio/hugo/archive/v0.53.tar.gz"

    executables = ['^hugo$']

    version('0.74.3', sha256='9b296fa0396c20956fa6a1f7afadaa78739af62c277b6c0cfae79a91b0fe823f')
    version('0.68.3', sha256='38e743605e45e3aafd9563feb9e78477e72d79535ce83b56b243ff991d3a2b6e')
    version('0.53', sha256='48e65a33d3b10527101d13c354538379d9df698e5c38f60f4660386f4232e65c')

    # Uses go modules.
    # See https://gohugo.io/getting-started/installing/#fetch-from-github
    depends_on('go@1.11:', when='@0.48:', type='build')

    variant('extended', default=False, description="Enable extended features")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)('version', output=str, error=str)
        match = re.search(r'Hugo Static Site Generator v(\S+)', output)
        return match.group(1) if match else None

    def setup_build_environment(self, env):
        env.prepend_path('GOPATH', self.stage.path)

    def install(self, spec, prefix):
        go_args = ['build']
        if self.spec.satisfies('+extended'):
            go_args.extend(['--tags', 'extended'])

        go = which('go')
        go(*go_args)
        mkdir(prefix.bin)
        install('hugo', prefix.bin)
