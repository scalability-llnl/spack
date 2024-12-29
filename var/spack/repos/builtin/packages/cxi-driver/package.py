# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CxiDriver(Package):
    """This are the Linux driver headers for the Cray/HPE Cassini 1 and 2
    high-speed network interconnect (aka. Slingshot), and its Ethernet driver."""

    homepage = "https://github.com/HewlettPackard/shs-cxi-driver"
    git = "https://github.com/HewlettPackard/shs-cxi-driver.git"

    license("GPL-2.0")

    version("main", branch="main")

    def install(self, spec, prefix):
        with working_dir(self.stage.source_path):
            copy_tree("include", prefix.include)
