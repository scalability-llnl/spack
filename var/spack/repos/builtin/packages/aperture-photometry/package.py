# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class AperturePhotometry(Package):
    """Aperture Photometry Tool APT is software for astronomical research"""

    homepage = "https://www.aperturephotometry.org/"
    url = "https://web.ipac.caltech.edu/staff/laher/apt/APT_v2.8.4.tar.gz"
    maintainers("snehring")

    version("3.0.2", sha256="8ac430079825ba274567fb998dd693bb6f99490f5b896d4746178ba796bfdead")
    version("2.8.4", sha256="28ae136c708a3ebcb83632230e119a03ca1a65499006ab69dc76e21b4921f465")
    version(
        "2.8.2",
        sha256="cb29eb39a630dc5d17c02fb824c69571fe1870a910a6acf9115c5f76fd89dd7e",
        deprecated=True,
    )

    depends_on("java")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("APT.jar", prefix.bin)
        java = join_path(self.spec["java"].prefix, "bin", "java")
        script_sh = join_path(os.path.dirname(__file__), "APT.sh")
        script = join_path(prefix.bin, "apt")
        install(script_sh, script)
        set_executable(script)
        filter_file("^java", java, script)
        filter_file("APT.jar", join_path(prefix.bin, "APT.jar"), script)
