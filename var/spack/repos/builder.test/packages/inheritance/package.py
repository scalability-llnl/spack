# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

import spack.pkg.builder.test.callbacks
from spack.package import *


class Inheritance(spack.pkg.builder.test.callbacks.Callbacks):
    """Package used to verify that inheritance among packages work as expected"""

    pass


class GenericBuilder(spack.pkg.builder.test.callbacks.GenericBuilder):
    def install(self, pkg, spec, prefix):
        super().install(pkg, spec, prefix)
        os.environ["INHERITANCE_INSTALL_CALLED"] = "1"
        os.environ["INSTALL_VALUE"] = "INHERITANCE"

    @run_before("install")
    def derived_before_install(self):
        os.environ["DERIVED_BEFORE_INSTALL_CALLED"] = "1"
        os.environ["TEST_VALUE"] = "0"
