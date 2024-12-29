# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform
from os import symlink

from spack.package import *


class DotnetCoreSdk(Package):
    """The .NET Core SDK is a powerful development environment to write
    applications for all types of infrastructure."""

    homepage = "https://www.microsoft.com/net/"

    license("MIT")

    if platform.system() == "Linux" and platform.machine() == "x86_64":
        version(
            "8.0.4",
            url="https://download.visualstudio.microsoft.com/download/pr/0a1b3cbd-b4af-4d0d-9ed7-0054f0e200b4/4bcc533c66379caaa91770236667aacb/dotnet-sdk-8.0.204-linux-x64.tar.gz",
            sha256="0ec834dc0f11a994057cd05d84c6250db726457f2fe308091d50543a5285dd15",
            preferred=True,
        )

        version(
            "7.0.18",
            url="https://download.visualstudio.microsoft.com/download/pr/a256265b-0ec6-4b63-b943-bc27bcfc98c0/47c8bbd54d7f6dbfe0ca4985c410282e/dotnet-sdk-7.0.408-linux-x64.tar.gz",
            sha256="e72beb77f59d5c55de46f52cce01b68f244e28058f646f1ea4ecf8a35b177e58",
        )

        version(
            "6.0.25",
            url="https://download.visualstudio.microsoft.com/download/pr/1cac4d08-3025-4c00-972d-5c7ea446d1d7/a83bc5cbedf8b90495802ccfedaeb2e6/dotnet-sdk-6.0.417-linux-x64.tar.gz",
            sha256="1b7c5ea04ccb817e1a411c9e1f89d7a4e54c0842b01b457e141bbc254ce97ba2",
        )

        version(
            "6.0.2",
            url="https://download.visualstudio.microsoft.com/download/pr/e7acb87d-ab08-4620-9050-b3e80f688d36/e93bbadc19b12f81e3a6761719f28b47/dotnet-sdk-6.0.102-linux-x64.tar.gz",
            sha256="9bdd4dacdf9a23d386f207ec19260afd36a7fb7302233c9abc0b47e65ffc3119",
            deprecated=True,
        )

        version(
            "5.0.4",
            url="https://download.visualstudio.microsoft.com/download/pr/73a9cb2a-1acd-4d20-b864-d12797ca3d40/075dbe1dc3bba4aa85ca420167b861b6/dotnet-sdk-5.0.201-linux-x64.tar.gz",
            sha256="9ff77087831e8ca32719566ec9ef537e136cfc02c5ff565e53f5509cc6e7b341",
            deprecated=True,
        )

        version(
            "3.1.13",
            url="https://download.visualstudio.microsoft.com/download/pr/ab82011d-2549-4e23-a8a9-a2b522a31f27/6e615d6177e49c3e874d05ee3566e8bf/dotnet-sdk-3.1.407-linux-x64.tar.gz",
            sha256="a744359910206fe657c3a02dfa54092f288a44c63c7c86891e866f0678a7e911",
            deprecated=True,
        )

        version(
            "2.1.300",
            url="https://download.microsoft.com/download/8/8/5/88544F33-836A-49A5-8B67-451C24709A8F/dotnet-sdk-2.1.300-linux-x64.tar.gz",
            sha256="fabca4c8825182ff18e5a2f82dfe75aecd10260ee9e7c85a8c4b3d108e5d8e1b",
            deprecated=True,
        )
    elif platform.system() == "Linux" and platform.machine() == "aarch64":
        version(
            "8.0.4",
            url="https://download.visualstudio.microsoft.com/download/pr/1e449990-2934-47ee-97fb-b78f0e587c98/1c92c33593932f7a86efa5aff18960ed/dotnet-sdk-8.0.204-linux-arm64.tar.gz",
            sha256="c6ecb0c1897e217e8d20153a0119276ee1091c0600aecf2aca8e674c3575942e",
            preferred=True,
        )

        version(
            "7.0.18",
            url="https://download.visualstudio.microsoft.com/download/pr/460f951f-0944-442b-8474-555e20394ca8/5fcf6b1845d87d772f919737b3dd5f55/dotnet-sdk-7.0.408-linux-arm64.tar.gz",
            sha256="dd9a8794561a8b9c658a2ba832328449a34b0dd0cdcb79e31d6efc2d0c9a8efc",
        )

        version(
            "6.0.25",
            url="https://download.visualstudio.microsoft.com/download/pr/03972b46-ddcd-4529-b8e0-df5c1264cd98/285a1f545020e3ddc47d15cf95ca7a33/dotnet-sdk-6.0.417-linux-arm64.tar.gz",
            sha256="c071e936442b90b80a941ab177b8c7851bc5377cf842cc1e61922b3d7fefeb0e",
        )

    variant("telemetry", default=False, description="allow collection of telemetry data")

    def setup_run_environment(self, env):
        if self.spec.satisfies("~telemetry"):
            env.set("DOTNET_CLI_TELEMETRY_OPTOUT", "1")

    def install(self, spec, prefix):
        mkdirp("bin")
        symlink("../dotnet", "bin/dotnet")
        install_tree(".", prefix)
