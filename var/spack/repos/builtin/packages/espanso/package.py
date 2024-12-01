# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Espanso(Package):
    """Cross-platform Text Expander written in Rust"""

    homepage = "https://github.com/federico-terzi/espanso"
    url = "https://github.com/federico-terzi/espanso/releases/download/v0.6.3/espanso-linux.tar.gz"

    maintainers("zicklag")

    version("0.6.3", sha256="eb9f9563ed0924d1494f0b406b6d3df9d7df00e81affaf15023d1c82dd8ac561")
    version("0.6.2", sha256="db2e53c8e0a17575f69739e53dd6a486dd0e912abbc7ac7c33d98567bd1f0e18")
    version("0.6.1", sha256="0917d4a990bfc5ced368ce9fbc3aa4bc4dac4d39ddea88359dc628fee16daf87")
    version("0.6.0", sha256="97689b734235224dde2fb4723bee24324a53355a6b549fb9d024a0c8ddb3cd98")
    version("0.5.5", sha256="94687a3049a43ed4c2ed3814afb4e32e09dec8ec396e54a7b012de936f0260e9")
    version("0.5.4", sha256="87e4c4a8a7bfb95a3ee987e34af3a37ca4d962bec3f863ef74be7fc8cdd1a9dd")
    version("0.5.3", sha256="1db21f74385b1eb94ac6d27def550d02dce8da34bce1f8f4a0c4eb9bfd80d135")
    version("0.5.2", sha256="69c8d3460ae497a2224cbf290c334c9151fc756053f65cbaf9ce8e9284ad50fd")
    version("0.5.1", sha256="e68d90256f9eb26b57085b5170e238752bfbfcf3d50ccaa5693974460cb19deb")
    version("0.5.0", sha256="f85c098a20b1022d8a6b751e3a56431caa01c796ce88ab95aae8950a1233da55")

    depends_on("xclip")
    depends_on("xdotool")

    def install(self, spec, prefix):
        mkdir(prefix.bin)
        install("espanso", prefix.bin)
