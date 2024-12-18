# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

from spack.package import *


class NfWaveCli(Package):
    """Command line tool for Wave containers provisioning service."""

    homepage = "https://github.com/seqeralabs/wave-cli"
    maintainers("marcodelapierre")

    if platform.machine() == "x86_64":
        if platform.system() == "Darwin":
            version(
                "1.2.0",
                sha256="97152d86d6ffed9e97b4eea1dc369525bdbc9bb19f0fefca79a10cbcbb82c549",
                url="https://github.com/seqeralabs/wave-cli/releases/download/v1.2.0/wave-1.2.0-macos-x86_64",
                expand=False,
            )
            version(
                "1.1.3",
                sha256="8f57cfafaefe34a9aadb460e3ddfe911bdcf7a93296e7a00d29983c065366a2f",
                url="https://github.com/seqeralabs/wave-cli/releases/download/v1.1.3/wave-1.1.3-macos-x86_64",
                expand=False,
            )
        elif platform.system() == "Linux":
            version(
                "1.2.0",
                sha256="12c572ec3384ddc07a623dcff5262398e0f7d50306b9f2bd35f779c7264a1c38",
                url="https://github.com/seqeralabs/wave-cli/releases/download/v1.2.0/wave-1.2.0-linux-x86_64",
                expand=False,
            )
            version(
                "1.1.3",
                sha256="953935159a5581e3a078528792651c12212302a609dffafe5a007d36f75049c0",
                url="https://github.com/seqeralabs/wave-cli/releases/download/v1.1.3/wave-1.1.3-linux-x86_64",
                expand=False,
            )
    elif platform.machine() == "arm64":
        if platform.system() == "Darwin":
            version(
                "1.2.0",
                sha256="813867e931d19f2452a1b8eee52dc976e08f4146001beed755b12ef44de29050",
                url="https://github.com/seqeralabs/wave-cli/releases/download/v1.2.0/wave-1.2.0-macos-arm64",
                expand=False,
            )
            version(
                "1.1.3",
                sha256="1ffdf6ff9d49d14ba38f563a57412e9a408e25c273ae9b11575243a032d101ed",
                url="https://github.com/seqeralabs/wave-cli/releases/download/v1.1.3/wave-1.1.3-macos-arm64",
                expand=False,
            )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(self.stage.archive_file, join_path(prefix.bin, "wave"))
        set_executable(join_path(prefix.bin, "wave"))
