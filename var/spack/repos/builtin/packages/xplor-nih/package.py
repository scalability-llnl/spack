# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class XplorNih(Package):
    """XPLOR-NIH is a structure determination program.

    Note: A manual download is required for XPLOR-NIH.
    Spack will search your current directory for the download file.
    Alternatively, add this file to a mirror so that Spack can find it.
    For instructions on how to set up a mirror, see
    https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://nmr.cit.nih.gov/xplor-nih/"
    manual_download = True

    version("2.45", md5="ab3e046604beb0effc89a1adb7bab438")

    depends_on("python", type=("build", "run"))

    def url_for_version(self, version):
        return "file://{0}/xplor-nih-{1}-Linux_x86_64.tar.gz".format(os.getcwd(), version)

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix.bin)
