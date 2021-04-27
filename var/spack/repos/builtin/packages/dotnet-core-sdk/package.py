# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink
from spack import *


class DotnetCoreSdk(Package):
    """The .NET Core SDK is a powerful development environment to write
    applications for all types of infrastructure."""

    homepage = "https://www.microsoft.com/net/"

    version('5.0.4',
            url='https://download.visualstudio.microsoft.com/download/pr/73a9cb2a-1acd-4d20-b864-d12797ca3d40/075dbe1dc3bba4aa85ca420167b861b6/dotnet-sdk-5.0.201-linux-x64.tar.gz',
            sha256='9ff77087831e8ca32719566ec9ef537e136cfc02c5ff565e53f5509cc6e7b341')

    version('3.1.13',
            url='https://download.visualstudio.microsoft.com/download/pr/ab82011d-2549-4e23-a8a9-a2b522a31f27/6e615d6177e49c3e874d05ee3566e8bf/dotnet-sdk-3.1.407-linux-x64.tar.gz',
            sha256='a744359910206fe657c3a02dfa54092f288a44c63c7c86891e866f0678a7e911')

    version('2.1.300',
            url='https://download.microsoft.com/download/8/8/5/88544F33-836A-49A5-8B67-451C24709A8F/dotnet-sdk-2.1.300-linux-x64.tar.gz',
            sha256='fabca4c8825182ff18e5a2f82dfe75aecd10260ee9e7c85a8c4b3d108e5d8e1b')

    variant('telemetry', default=False,
            description='allow collection of telemetry data')

    def setup_build_environment(self, env):
        if '-telemetry' in self.spec:
            env.set('DOTNET_CLI_TELEMETRY_OPTOUT', 1)

    def install(self, spec, prefix):
        mkdirp('bin')
        symlink('../dotnet', 'bin/dotnet')
        install_tree(".", prefix)
