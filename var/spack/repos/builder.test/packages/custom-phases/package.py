# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import spack.build_systems.generic
from spack.package import *


class CustomPhases(Package):
    """Package used to verify that we can set custom phases on builders"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/a-1.0.tar.gz"

    version("2.0", md5="abcdef0123456789abcdef0123456789")
    version("1.0", md5="0123456789abcdef0123456789abcdef")


class GenericBuilder(spack.build_systems.generic.GenericBuilder):
    phases = ["configure", "install"]

    def configure(self, pkg, spec, prefix):
        os.environ["CONFIGURE_CALLED"] = "1"
        os.environ["LAST_PHASE"] = "CONFIGURE"

    def install(self, pkg, spec, prefix):
        os.environ["INSTALL_CALLED"] = "1"
        os.environ["LAST_PHASE"] = "INSTALL"
        mkdirp(prefix.bin)
