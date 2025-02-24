# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class CassiniHeaders(Package):
    """This package provides hardware definitions and C headers for use by the
    Linux driver and by user-space applications for the Cassini/Slingshot
    +high-speed network interconnect made by HPE (formerly Cray)"""

    homepage = "https://github.com/HewlettPackard/shs-cassini-headers"
    git = "https://github.com/HewlettPackard/shs-cassini-headers.git"

    license("GPL-2.0-only or BSD-2-Clause")

    version("main", branch="main")

    def install(self, spec, prefix):
        with working_dir(self.stage.source_path):
            copy_tree("include", prefix.include)
            copy_tree("share", prefix.share)
