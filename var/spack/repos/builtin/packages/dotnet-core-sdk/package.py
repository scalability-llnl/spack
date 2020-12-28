# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from os import symlink

from spack.package import *


class DotnetCoreSdk(Package):
    """The .NET Core SDK is a powerful development environment to write
    applications for all types of infrastructure."""

    homepage = "https://www.microsoft.com/net/"

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
